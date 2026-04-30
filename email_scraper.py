import re
import sys
import os
import time
import json
import sqlite3
import logging
from datetime import datetime
from urllib.parse import urljoin, urlparse
from collections import deque

import requests
from bs4 import BeautifulSoup


def clean_summary(text: str, max_len: int = 300) -> str:
    """Strip HTML tags, decode entities, collapse whitespace."""
    if not text:
        return ""
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text(separator=" ")
    text = re.sub(r"[\r\n\t]+", " ", text)
    text = re.sub(r" {2,}", " ", text)
    return text.strip()[:max_len]


def enrich_summaries(events: list[dict], emit=None) -> list[dict]:
    """Replace raw summaries with clean 2-3 sentence AI descriptions (Romanian).
    Falls back to clean_summary if ANTHROPIC_API_KEY is not set or API fails."""
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        if emit:
            emit({"type": "log", "msg": "⚠ ANTHROPIC_API_KEY not set — using raw summaries.", "cls": "warn"})
        return events

    try:
        import anthropic
    except ImportError:
        if emit:
            emit({"type": "log", "msg": "⚠ anthropic package missing — using raw summaries.", "cls": "warn"})
        return events

    client = anthropic.Anthropic(api_key=api_key)

    # Build a compact list of events to summarize
    items = []
    for i, ev in enumerate(events):
        raw = clean_summary(ev.get("summary", ""))
        items.append({
            "i": i,
            "name": ev.get("event_name", ""),
            "city": ev.get("city", ""),
            "date": ev.get("date", ""),
            "raw": raw[:400],
        })

    # Send in chunks of 40 to stay within token limits
    CHUNK = 40
    updated = list(events)
    for start in range(0, len(items), CHUNK):
        chunk = items[start:start + CHUNK]
        if emit:
            emit({"type": "log", "msg": f"✨ Generating summaries {start+1}–{start+len(chunk)} / {len(items)}…", "cls": "info"})

        payload = json.dumps(chunk, ensure_ascii=False)
        prompt = (
            "Ești un redactor pentru un ghid de evenimente din România. "
            "Primești o listă JSON de evenimente. Pentru fiecare, scrie un rezumat de 2-3 propoziții în română, "
            "la persoana a treia, în stil natural și prietenos — ce este evenimentul, pentru cine este și când/unde are loc. "
            "Returnează DOAR un JSON array cu obiectele: [{\"i\": <index>, \"summary\": \"<text>\"}]. "
            "Nu adăuga text în afara JSON-ului.\n\n"
            f"Evenimente:\n{payload}"
        )

        try:
            resp = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}],
            )
            raw_text = resp.content[0].text.strip()
            # Strip markdown code fences if present
            raw_text = re.sub(r"^```(?:json)?\s*", "", raw_text)
            raw_text = re.sub(r"\s*```$", "", raw_text)
            results = json.loads(raw_text)
            for r in results:
                idx = r.get("i")
                summary = r.get("summary", "").strip()
                if idx is not None and summary:
                    updated[idx] = {**updated[idx], "summary": summary}
        except Exception as e:
            if emit:
                emit({"type": "log", "msg": f"⚠ Summary generation failed for chunk: {e}", "cls": "warn"})

        time.sleep(0.5)

    return updated

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Database lives next to the script
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scraper.db")


class Scraper:
    """Extract emails and events from webpages."""

    EMAIL_RE = re.compile(
        r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"
    )

    OBFUSCATED_RE = re.compile(
        r"[a-zA-Z0-9._%+\-]+\s*[\[\(]?\s*(?:at|AT)\s*[\]\)]?\s*"
        r"[a-zA-Z0-9.\-]+\s*[\[\(]?\s*(?:dot|DOT)\s*[\]\)]?\s*[a-zA-Z]{2,}"
    )

    PHONE_RE = re.compile(
        r"(?:\+40\s?|0)(?:7[0-9]{2}|3[0-9]{2}|2[0-9]{2})"
        r"[\s.\-]?\d{3}[\s.\-]?\d{3}"
    )

    # Matches dates like "3 aprilie 2026", "2026-04-03", "03.04.2026", "April 3, 2026"
    DATE_2026_RE = re.compile(
        r"(?:"
        r"\d{1,2}[\s./\-](?:ianuarie|februarie|martie|aprilie|mai|iunie|iulie|august|septembrie|octombrie|noiembrie|decembrie)[\s./\-]202[6-9]"
        r"|(?:ianuarie|februarie|martie|aprilie|mai|iunie|iulie|august|septembrie|octombrie|noiembrie|decembrie)\s+\d{1,2},?\s+202[6-9]"
        r"|202[6-9][\-/]\d{1,2}[\-/]\d{1,2}"
        r"|\d{1,2}[./]\d{1,2}[./]202[6-9]"
        r"|\d{1,2}[\s.\-](?:january|february|march|april|may|june|july|august|september|october|november|december)[\s.\-]202[6-9]"
        r")",
        re.IGNORECASE
    )

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }

    SKIP_EXTENSIONS = {
        ".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp",
        ".pdf", ".zip", ".tar", ".gz", ".mp3", ".mp4",
        ".avi", ".mov", ".css", ".js", ".woff", ".woff2", ".ttf",
    }

    CITIES = [
        "București", "Cluj-Napoca", "Timișoara", "Iași", "Constanța",
        "Brașov", "Craiova", "Galați", "Oradea", "Sibiu",
    ]

    EVENT_QUERIES = [
        "evenimente copii {city} 2026",
        "activitati copii familie {city} 2026",
        "ateliere copii {city} 2026",
        "spectacole teatru copii {city} 2026",
        "cursuri copii {city} 2026",
        "festivaluri familie copii {city} 2026",
        "tabara copii {city} 2026",
        "parenting workshop {city} 2026",
    ]

    def __init__(self, timeout=15, delay=1.0, max_retries=2, use_playwright=True):
        self.timeout = timeout
        self.delay = delay
        self.max_retries = max_retries
        self.use_playwright = use_playwright
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)

    # ── Fetch ──────────────────────────────────────────────
    def fetch(self, url: str) -> str | None:
        if self.use_playwright:
            try:
                from playwright.sync_api import sync_playwright
                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=True)
                    page = browser.new_page(extra_http_headers=self.HEADERS)
                    page.goto(url, timeout=self.timeout * 1000, wait_until="networkidle")
                    html = page.content()
                    browser.close()
                    return html
            except ImportError:
                logger.warning("Playwright not installed, falling back to requests.")
                self.use_playwright = False
            except Exception as e:
                logger.warning(f"Playwright failed for {url}: {e}, falling back to requests.")

        for attempt in range(1, self.max_retries + 1):
            try:
                resp = self.session.get(url, timeout=self.timeout)
                resp.raise_for_status()
                return resp.text
            except requests.RequestException as e:
                logger.warning(f"Attempt {attempt} failed for {url}: {e}")
                if attempt < self.max_retries:
                    time.sleep(self.delay * attempt)
        return None

    # ── Email extraction ───────────────────────────────────
    def extract_emails(self, html: str) -> set[str]:
        emails = set()
        emails.update(self.EMAIL_RE.findall(html))

        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()

        text = soup.get_text(separator=" ")
        emails.update(self.EMAIL_RE.findall(text))

        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            if href.startswith("mailto:"):
                raw = href.replace("mailto:", "").split("?")[0].strip()
                if self.EMAIL_RE.fullmatch(raw):
                    emails.add(raw)

        for match in self.OBFUSCATED_RE.findall(text):
            cleaned = re.sub(r"\s*[\[\(]?\s*(?:at|AT)\s*[\]\)]?\s*", "@", match)
            cleaned = re.sub(r"\s*[\[\(]?\s*(?:dot|DOT)\s*[\]\)]?\s*", ".", cleaned)
            if self.EMAIL_RE.fullmatch(cleaned):
                emails.add(cleaned)

        return self._filter_emails(emails)

    def _filter_emails(self, emails: set[str]) -> set[str]:
        blocked_domains = {"example.com", "example.org", "test.com", "sentry.io"}
        blocked_patterns = {"noreply@", "no-reply@", "mailer-daemon@"}
        filtered = set()
        for email in emails:
            lower = email.lower()
            domain = lower.split("@")[1] if "@" in lower else ""
            if domain in blocked_domains:
                continue
            if any(lower.startswith(p) for p in blocked_patterns):
                continue
            if re.search(r"@\d+x?\.(png|jpg|jpeg|gif|svg|webp|css|js)$", lower):
                continue
            if re.search(r"\.(png|jpg|jpeg|gif|svg|webp|css|js|woff|ttf)$", lower):
                continue
            filtered.add(email)
        return filtered

    # ── Phone extraction ───────────────────────────────────
    def extract_phones(self, text: str) -> set[str]:
        return set(self.PHONE_RE.findall(text))

    # Words that EXPLICITLY reference children, family, or parenting — at least one required
    FAMILY_KEYWORDS = re.compile(
        r"\bcopii\b|\bcopil\b|\bcopiilor\b|\bcopilului\b|"
        r"\bfamilie\b|\bfamilii\b|\bfamiliilor\b|"
        r"\bparinti\b|\bpărinți\b|\bparinți\b|\bpărinti\b|"
        r"\bjunior\b|\bbaby\b|\bbebe\b|\bkids\b|\bchildren\b|\bfamily\b|\btoddler\b|"
        r"\bziua copil|\b1 iunie\b|"
        r"\bscoala de vara\b|\bșcoală de vară\b|"
        r"\bpapusi\b|\bpăpuși\b|\bmagician\b|\bpinocchio\b|"
        r"\bscufita\b|\bcenusareasa\b|\bfrozen\b|\bdisney\b|"
        r"\begg hunt\b|\bpărinte\b|\bparinte\b",
        re.IGNORECASE
    )

    # Kept for backward compatibility in card-based extraction
    EVENT_KEYWORDS = FAMILY_KEYWORDS

    # ── Event extraction from HTML ─────────────────────────
    def extract_events(self, html: str, url: str, target_city: str = "", family_filter: bool = True) -> list[dict]:
        """Extract events from a page. Returns list of event dicts."""
        soup = BeautifulSoup(html, "html.parser")
        events = []

        # 1. Try JSON-LD structured data first
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(script.string)
                items = data if isinstance(data, list) else [data]
                for item in items:
                    if not isinstance(item, dict):
                        continue
                    if item.get("@type") == "Event":
                        events.append(self._parse_jsonld_event(item, url, target_city))
                    elif isinstance(item.get("@graph"), list):
                        for sub in item["@graph"]:
                            if isinstance(sub, dict) and sub.get("@type") == "Event":
                                events.append(self._parse_jsonld_event(sub, url, target_city))
            except (json.JSONDecodeError, TypeError):
                continue

        # 2. Get page text and contact info
        for tag in soup(["script", "style"]):
            tag.decompose()
        text = soup.get_text(separator=" ")

        page_emails = self.extract_emails(html)
        page_phones = self.extract_phones(text)
        page_email = "; ".join(sorted(page_emails)[:3]) if page_emails else ""
        page_phone = "; ".join(sorted(page_phones)[:3]) if page_phones else ""

        # If JSON-LD found events, enrich and filter
        if events:
            for ev in events:
                if not ev["email"]:
                    ev["email"] = page_email
                if not ev["phone"]:
                    ev["phone"] = page_phone
            return self._filter_events(events, family_filter)

        # 3. Fallback: scan for event cards with 2026 dates
        dates_found = self.DATE_2026_RE.findall(text)
        if not dates_found:
            return []

        cards = soup.find_all(["article", "div", "li"], class_=re.compile(
            r"event|card|item|listing|spectacol|activitat", re.IGNORECASE
        ))

        if cards:
            for card in cards:
                card_text = card.get_text(separator=" ", strip=True)
                card_dates = self.DATE_2026_RE.findall(card_text)
                if not card_dates:
                    continue
                heading = card.find(["h1", "h2", "h3", "h4", "h5", "a"])
                name = heading.get_text(strip=True) if heading else card_text[:80]
                if not self._is_valid_event_name(name):
                    continue
                if family_filter and not self.EVENT_KEYWORDS.search(card_text):
                    continue
                events.append({
                    "event_name": name,
                    "city": target_city,
                    "date": card_dates[0],
                    "webpage": url,
                    "email": page_email,
                    "phone": page_phone,
                    "summary": clean_summary(card_text),
                })

        return self._filter_events(events, family_filter)

    def _is_valid_event_name(self, name: str) -> bool:
        """Reject names that are just dates, timestamps, or too short/generic."""
        name = name.strip()
        if len(name) < 5:
            return False
        # Reject if it's mostly a date/time
        cleaned = re.sub(r"[\d\s:./,\-TZ+]+", "", name).strip()
        if len(cleaned) < 4:
            return False
        # Reject generic labels
        skip = {"evenimente viitoare", "detalii eveniment", "mai mult", "citeste mai mult",
                "vezi toate", "load more", "next", "previous"}
        if name.lower().strip() in skip:
            return False
        return True

    def _is_family_event(self, ev: dict) -> bool:
        """Return True only if the event is explicitly about children/family/parenting."""
        searchable = " ".join([
            ev.get("event_name", ""),
            ev.get("summary", ""),
        ])
        return bool(self.FAMILY_KEYWORDS.search(searchable))

    def _filter_events(self, events: list[dict], family_filter: bool = True) -> list[dict]:
        seen = set()
        unique = []
        for ev in events:
            name = ev["event_name"].strip()
            if not self._is_valid_event_name(name):
                continue
            if family_filter and not self._is_family_event(ev):
                continue
            key = re.sub(r"\s+", " ", name.lower().strip())
            if key in seen:
                continue
            seen.add(key)
            date = ev.get("date", "")
            if re.match(r"^\d{4}-\d{1,2}-\d{1,2}T", date):
                date = date.split("T")[0]
            ev["date"] = date
            ev["event_name"] = name
            unique.append(ev)
        return unique

    def _parse_jsonld_event(self, item: dict, url: str, city: str) -> dict:
        name = item.get("name", "")
        start = item.get("startDate", "")
        location = item.get("location", {})
        if isinstance(location, dict):
            loc_name = location.get("name", "")
            addr = location.get("address", {})
            if isinstance(addr, dict):
                loc_city = addr.get("addressLocality", city)
            else:
                loc_city = city
        else:
            loc_name = str(location)
            loc_city = city

        desc = item.get("description", "")
        summary = clean_summary(desc) if desc else clean_summary(f"{name} - {loc_name}")

        organizer = item.get("organizer", {})
        email = ""
        if isinstance(organizer, dict):
            email = organizer.get("email", "")

        return {
            "event_name": name,
            "city": loc_city or city,
            "date": start[:10] if start else "",
            "webpage": url,
            "email": email,
            "phone": "",
            "summary": summary,
        }

    # ── DuckDuckGo search ──────────────────────────────────
    def ddg_search(self, query: str, num_results: int = 10) -> list[str]:
        try:
            from ddgs import DDGS
        except ImportError:
            print("ddgs not installed. Run: pip install ddgs")
            return []
        urls = []
        try:
            with DDGS() as ddgs:
                for r in ddgs.text(query, max_results=num_results):
                    urls.append(r["href"])
        except Exception as e:
            logger.error(f"Search failed: {e}")
        return urls

    # ── Email search ───────────────────────────────────────
    def search_emails(self, query: str, num_results: int = 10) -> dict[str, set[str]]:
        print(f"\nSearching for: {query}")
        urls = self.ddg_search(query, num_results)
        for u in urls:
            print(f"  Found: {u}")

        if not urls:
            print("No search results found.")
            return {}

        print(f"\nScraping {len(urls)} pages...\n")
        results = {}
        for url in urls:
            emails = self.scrape_page_emails(url)
            if emails:
                results[url] = emails
                print(f"\n[{url}]")
                for e in sorted(emails):
                    print(f"  {e}")
            else:
                print(f"[{url}] -- no emails found")
            time.sleep(self.delay)
        return results

    def scrape_page_emails(self, url: str) -> set[str]:
        logger.info(f"Scraping: {url}")
        html = self.fetch(url)
        if not html:
            logger.error(f"Could not fetch: {url}")
            return set()
        return self.extract_emails(html)

    # ── Event search across cities ─────────────────────────
    def search_events(self, cities: list[str], queries_per_city: int = 2,
                      results_per_query: int = 5) -> list[dict]:
        all_events = []
        seen_names = set()

        for city in cities:
            print(f"\n{'='*50}")
            print(f"  Searching events in: {city}")
            print(f"{'='*50}")

            city_urls = set()
            queries = self.EVENT_QUERIES[:queries_per_city]
            for q_template in queries:
                query = q_template.format(city=city)
                urls = self.ddg_search(query, results_per_query)
                for u in urls:
                    if u not in city_urls:
                        city_urls.add(u)
                        print(f"  {u}")
                time.sleep(0.5)

            print(f"\n  Scraping {len(city_urls)} pages for {city}...\n")
            for url in city_urls:
                html = self.fetch(url)
                if not html:
                    continue
                events = self.extract_events(html, url, city)
                for ev in events:
                    key = ev["event_name"].lower().strip()
                    if key not in seen_names and len(key) > 3:
                        seen_names.add(key)
                        all_events.append(ev)
                        print(f"  + {ev['event_name']} ({ev['date']})")
                time.sleep(self.delay)

        return all_events


# ── Database ───────────────────────────────────────────────

def init_db():
    con = sqlite3.connect(DB_PATH)
    con.execute("""
        CREATE TABLE IF NOT EXISTS searches (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            query     TEXT,
            mode      TEXT,
            timestamp TEXT
        )
    """)
    con.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            search_id INTEGER REFERENCES searches(id),
            url       TEXT,
            email     TEXT,
            timestamp TEXT
        )
    """)
    con.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name TEXT,
            city       TEXT,
            date       TEXT,
            webpage    TEXT,
            email      TEXT,
            phone      TEXT,
            summary    TEXT,
            timestamp  TEXT,
            UNIQUE(event_name, city, date)
        )
    """)
    # Add unique constraint to existing DBs that predate this schema
    try:
        con.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_event_unique ON events(event_name, city, date)")
    except Exception:
        pass
    con.commit()
    return con


def save_email_results(con, query: str, mode: str, results: dict[str, set[str]]):
    ts = datetime.now().isoformat(sep=" ", timespec="seconds")
    cur = con.execute(
        "INSERT INTO searches (query, mode, timestamp) VALUES (?, ?, ?)",
        (query, mode, ts)
    )
    search_id = cur.lastrowid
    rows = [
        (search_id, url, email, ts)
        for url, emails in results.items()
        for email in emails
    ]
    con.executemany(
        "INSERT INTO emails (search_id, url, email, timestamp) VALUES (?, ?, ?, ?)",
        rows
    )
    con.commit()
    print(f"\n[DB] Saved {len(rows)} email(s) to database (search #{search_id})")


CSV_PATH = os.path.join(os.path.dirname(DB_PATH), "events_export.csv")
CSV_HEADERS = ["event_name", "city", "date", "webpage", "email", "phone", "summary", "saved_at"]


def _append_events_csv(rows):
    import csv
    write_header = not os.path.exists(CSV_PATH) or os.path.getsize(CSV_PATH) == 0
    try:
        with open(CSV_PATH, "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            if write_header:
                writer.writerow(CSV_HEADERS)
            writer.writerows(rows)
    except PermissionError:
        print(f"[CSV] Skipped — file is open in another program. Close it and use Export CSV to refresh.")


def save_events(con, events: list[dict]):
    ts = datetime.now().isoformat(sep=" ", timespec="seconds")
    rows = [
        (ev["event_name"], ev["city"], ev["date"], ev["webpage"],
         ev["email"], ev["phone"], ev["summary"], ts)
        for ev in events
    ]
    con.executemany(
        "INSERT OR IGNORE INTO events (event_name, city, date, webpage, email, phone, summary, timestamp) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        rows
    )
    con.commit()
    saved = con.execute("SELECT changes()").fetchone()[0]
    _append_events_csv(rows)
    print(f"\n[DB] Saved {saved} new event(s) (skipped {len(rows)-saved} duplicates)")


def export_events_xlsx(con):
    try:
        import openpyxl
    except ImportError:
        print("openpyxl not installed. Run: pip install openpyxl")
        return

    rows = con.execute("""
        SELECT event_name, city, date, webpage, email, phone, summary, timestamp
        FROM events ORDER BY city, date
    """).fetchall()

    if not rows:
        print("No events in database.")
        return

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Events"
    headers = ["event_name", "city", "date", "webpage", "email", "phone", "summary", "saved_at"]
    ws.append(headers)

    # Bold headers
    for cell in ws[1]:
        cell.font = openpyxl.styles.Font(bold=True)

    for row in rows:
        ws.append(list(row))

    # Auto-width columns
    for col in ws.columns:
        max_len = max(len(str(cell.value or "")) for cell in col)
        ws.column_dimensions[col[0].column_letter].width = min(max_len + 2, 60)

    filepath = os.path.join(os.path.dirname(DB_PATH), "events_export.xlsx")
    wb.save(filepath)
    print(f"\nExported {len(rows)} events to: {filepath}")


def export_events_csv(con):
    import csv
    rows = con.execute("""
        SELECT event_name, city, date, webpage, email, phone, summary, timestamp
        FROM events ORDER BY city, date
    """).fetchall()

    if not rows:
        print("No events in database.")
        return

    filepath = os.path.join(os.path.dirname(DB_PATH), "events_export.csv")
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["event_name", "city", "date", "webpage", "email", "phone", "summary", "saved_at"])
        writer.writerows(rows)

    print(f"\nExported {len(rows)} events to: {filepath}")


def visualize_events(con):
    import json
    import webbrowser

    rows = con.execute("""
        SELECT event_name, city, date, webpage, email, phone, summary, timestamp
        FROM events ORDER BY city, date
    """).fetchall()

    if not rows:
        print("No events in database.")
        return

    events_json = json.dumps([
        {"name": r[0], "city": r[1], "date": r[2], "url": r[3],
         "email": r[4] or "", "phone": r[5] or "", "summary": r[6] or "", "saved": r[7]}
        for r in rows
    ], ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="ro">
<head>
<meta charset="UTF-8">
<title>Evenimente Scraper</title>
<style>
  body {{ font-family: Arial, sans-serif; margin: 0; background: #f4f6f9; color: #333; }}
  header {{ background: #2c3e50; color: #fff; padding: 18px 30px; }}
  header h1 {{ margin: 0; font-size: 1.4rem; }}
  .controls {{ display: flex; gap: 12px; flex-wrap: wrap; padding: 14px 30px; background: #fff; border-bottom: 1px solid #ddd; }}
  .controls input, .controls select {{ padding: 7px 11px; border: 1px solid #ccc; border-radius: 5px; font-size: 0.9rem; }}
  .controls input[type=text] {{ flex: 1; min-width: 180px; }}
  .stats {{ display: flex; gap: 16px; padding: 14px 30px; flex-wrap: wrap; }}
  .stat {{ background: #fff; border-radius: 8px; padding: 12px 20px; box-shadow: 0 1px 4px rgba(0,0,0,.08); min-width: 130px; text-align: center; }}
  .stat .n {{ font-size: 2rem; font-weight: bold; color: #2980b9; }}
  .stat .l {{ font-size: 0.8rem; color: #666; }}
  table {{ width: calc(100% - 60px); margin: 0 30px 30px; border-collapse: collapse; background: #fff; box-shadow: 0 1px 4px rgba(0,0,0,.08); border-radius: 8px; overflow: hidden; }}
  th {{ background: #2c3e50; color: #fff; padding: 10px 12px; text-align: left; font-size: 0.85rem; cursor: pointer; user-select: none; }}
  th:hover {{ background: #3d5166; }}
  td {{ padding: 9px 12px; border-bottom: 1px solid #eee; font-size: 0.85rem; vertical-align: top; max-width: 260px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
  tr:last-child td {{ border-bottom: none; }}
  tr:hover td {{ background: #f0f7ff; }}
  a {{ color: #2980b9; text-decoration: none; }} a:hover {{ text-decoration: underline; }}
  .badge {{ display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; background: #e8f4fd; color: #2980b9; }}
  #count {{ color: #666; font-size: 0.85rem; padding: 0 30px 8px; }}
</style>
</head>
<body>
<header><h1>Evenimente Scraper Dashboard</h1></header>
<div class="stats" id="stats"></div>
<div class="controls">
  <input type="text" id="search" placeholder="Caută eveniment, oraș...">
  <select id="cityFilter"><option value="">Toate orașele</option></select>
  <select id="sortBy">
    <option value="date">Sortare: Dată</option>
    <option value="city">Sortare: Oraș</option>
    <option value="name">Sortare: Nume</option>
  </select>
</div>
<div id="count"></div>
<table>
  <thead><tr>
    <th onclick="sortCol('name')">Eveniment</th>
    <th onclick="sortCol('city')">Oraș</th>
    <th onclick="sortCol('date')">Dată</th>
    <th>URL</th>
    <th>Email</th>
    <th>Telefon</th>
  </tr></thead>
  <tbody id="tbody"></tbody>
</table>
<script>
const ALL = {events_json};
let sortKey = 'date', sortDir = 1;

const citySet = [...new Set(ALL.map(e => e.city).filter(Boolean))].sort();
const sel = document.getElementById('cityFilter');
citySet.forEach(c => {{ const o = document.createElement('option'); o.value = c; o.textContent = c; sel.appendChild(o); }});

function sortCol(k) {{
  if (sortKey === k) sortDir *= -1; else {{ sortKey = k; sortDir = 1; }}
  render();
}}

function render() {{
  const q = document.getElementById('search').value.toLowerCase();
  const city = document.getElementById('cityFilter').value;
  let data = ALL.filter(e =>
    (!city || e.city === city) &&
    (!q || e.name.toLowerCase().includes(q) || (e.city||'').toLowerCase().includes(q) || (e.summary||'').toLowerCase().includes(q))
  );
  data.sort((a,b) => (a[sortKey]||'') > (b[sortKey]||'') ? sortDir : -sortDir);

  document.getElementById('count').textContent = `${{data.length}} evenimente afișate`;

  const cities = {{}};
  ALL.forEach(e => cities[e.city] = (cities[e.city]||0)+1);
  const topCity = Object.entries(cities).sort((a,b)=>b[1]-a[1])[0];
  document.getElementById('stats').innerHTML = `
    <div class="stat"><div class="n">${{ALL.length}}</div><div class="l">Total evenimente</div></div>
    <div class="stat"><div class="n">${{citySet.length}}</div><div class="l">Orașe</div></div>
    <div class="stat"><div class="n">${{ALL.filter(e=>e.email).length}}</div><div class="l">Cu email</div></div>
    <div class="stat"><div class="n">${{topCity ? topCity[0] : '-'}}</div><div class="l">Cel mai activ oraș</div></div>
  `;

  document.getElementById('tbody').innerHTML = data.map(e => `
    <tr>
      <td title="${{e.name}}">${{e.name}}</td>
      <td><span class="badge">${{e.city||''}}</span></td>
      <td>${{e.date||''}}</td>
      <td>${{e.url ? `<a href="${{e.url}}" target="_blank">link</a>` : ''}}</td>
      <td>${{e.email || ''}}</td>
      <td>${{e.phone || ''}}</td>
    </tr>
  `).join('');
}}

document.getElementById('search').addEventListener('input', render);
document.getElementById('cityFilter').addEventListener('change', render);
document.getElementById('sortBy').addEventListener('change', e => {{ sortKey = e.target.value; render(); }});
render();
</script>
</body></html>"""

    filepath = os.path.join(os.path.dirname(DB_PATH), "events_dashboard.html")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\nDashboard saved to: {filepath}")
    webbrowser.open(f"file:///{filepath.replace(chr(92), '/')}")


def print_email_summary(results: dict[str, set[str]]):
    all_emails = set()
    for emails in results.values():
        all_emails.update(emails)
    print(f"\n--- Total unique emails: {len(all_emails)} ---")
    for e in sorted(all_emails):
        print(e)


def show_email_history(con):
    rows = con.execute("""
        SELECT s.id, s.query, s.mode, s.timestamp, COUNT(e.id) as total
        FROM searches s
        LEFT JOIN emails e ON e.search_id = s.id
        GROUP BY s.id
        ORDER BY s.id DESC
        LIMIT 20
    """).fetchall()
    if not rows:
        print("No history yet.")
        return
    print(f"\n{'#':<5} {'Query':<40} {'Mode':<8} {'Emails':<7} Timestamp")
    print("-" * 75)
    for r in rows:
        print(f"{r[0]:<5} {r[1][:38]:<40} {r[2]:<8} {r[4]:<7} {r[3]}")


def show_search_emails(con):
    search_id = input("Enter search # to view emails: ").strip()
    if not search_id.isdigit():
        print("Invalid input.")
        return
    rows = con.execute(
        "SELECT url, email FROM emails WHERE search_id = ? ORDER BY url, email",
        (search_id,)
    ).fetchall()
    if not rows:
        print("No emails found for that search.")
        return
    current_url = None
    for url, email in rows:
        if url != current_url:
            print(f"\n[{url}]")
            current_url = url
        print(f"  {email}")


def show_events_summary(con):
    rows = con.execute("""
        SELECT city, COUNT(*) FROM events GROUP BY city ORDER BY city
    """).fetchall()
    if not rows:
        print("No events in database.")
        return
    total = sum(r[1] for r in rows)
    print(f"\n--- Events in database: {total} ---")
    for city, count in rows:
        print(f"  {city}: {count}")


# ── Interactive menu ───────────────────────────────────────
if __name__ == "__main__":
    scraper = Scraper(timeout=15, delay=1.0)
    con = init_db()

    while True:
        print("\n=== Scraper Tool ===")
        print("1. Paste URLs (extract emails)")
        print("2. Search emails (DuckDuckGo)")
        print("3. Search events (10 Romanian cities)")
        print("4. Search events (custom query)")
        print("5. View email history")
        print("6. View events summary")
        print("7. Export events to Excel")
        print("8. Export events to CSV")
        print("9. Visualize events (HTML dashboard)")
        print("10. Exit")
        choice = input("\nChoose an option (1-10): ").strip()

        if choice == "1":
            print("\nPaste URLs (one per line). Blank line to start:")
            urls = []
            while True:
                line = input().strip()
                if not line:
                    break
                urls.append(line)
            if not urls:
                print("No URLs provided.")
                continue
            results = {}
            for url in urls:
                emails = scraper.scrape_page_emails(url)
                if emails:
                    results[url] = emails
                    print(f"\n[{url}]")
                    for e in sorted(emails):
                        print(f"  {e}")
                else:
                    print(f"\n[{url}] -- no emails found")
            if results:
                print_email_summary(results)
                save_email_results(con, ", ".join(urls), "manual", results)

        elif choice == "2":
            query = input("\nEnter search query: ").strip()
            if not query:
                continue
            num = input("How many results? (default 10, 'all' for max): ").strip().lower()
            num = 100 if num == "all" else (int(num) if num.isdigit() else 10)
            results = scraper.search_emails(query, num_results=num)
            if results:
                print_email_summary(results)
                save_email_results(con, query, "search", results)

        elif choice == "3":
            print("\nCities:", ", ".join(Scraper.CITIES))
            print("Select cities (comma-separated numbers, or 'all'):")
            for i, c in enumerate(Scraper.CITIES, 1):
                print(f"  {i}. {c}")
            sel = input("\nYour selection (default: all): ").strip().lower()
            if sel == "" or sel == "all":
                cities = list(Scraper.CITIES)
            else:
                indices = [int(x.strip()) - 1 for x in sel.split(",") if x.strip().isdigit()]
                cities = [Scraper.CITIES[i] for i in indices if 0 <= i < len(Scraper.CITIES)]

            if not cities:
                print("No cities selected.")
                continue

            qpc = input("Queries per city (default 2, max 4): ").strip()
            qpc = int(qpc) if qpc.isdigit() else 2
            qpc = min(qpc, 4)
            rpq = input("Results per query (default 5): ").strip()
            rpq = int(rpq) if rpq.isdigit() else 5

            print(f"\nSearching {len(cities)} cities x {qpc} queries x {rpq} results...")
            events = scraper.search_events(cities, queries_per_city=qpc, results_per_query=rpq)

            if events:
                print(f"\n{'='*50}")
                print(f"  TOTAL EVENTS FOUND: {len(events)}")
                print(f"{'='*50}")
                for ev in events:
                    print(f"  [{ev['city']}] {ev['event_name']} ({ev['date']})")
                save_events(con, events)
            else:
                print("\nNo events found.")

        elif choice == "4":
            query = input("\nEnter event search query: ").strip()
            if not query:
                continue
            city = input("City name (for tagging): ").strip()
            num = input("How many results? (default 10): ").strip()
            num = int(num) if num.isdigit() else 10

            print(f"\nSearching: {query}")
            urls = scraper.ddg_search(query, num)
            for u in urls:
                print(f"  {u}")

            events = []
            seen = set()
            for url in urls:
                html = scraper.fetch(url)
                if not html:
                    continue
                page_events = scraper.extract_events(html, url, city)
                for ev in page_events:
                    key = ev["event_name"].lower().strip()
                    if key not in seen:
                        seen.add(key)
                        events.append(ev)
                        print(f"  + {ev['event_name']} ({ev['date']})")
                time.sleep(scraper.delay)

            if events:
                save_events(con, events)
                print(f"\nFound {len(events)} event(s)")
            else:
                print("\nNo events found.")

        elif choice == "5":
            show_email_history(con)
            view = input("\nView emails from a search? (enter # or blank to skip): ").strip()
            if view.isdigit():
                rows = con.execute(
                    "SELECT url, email FROM emails WHERE search_id = ? ORDER BY url, email",
                    (view,)
                ).fetchall()
                current_url = None
                for url, email in rows:
                    if url != current_url:
                        print(f"\n[{url}]")
                        current_url = url
                    print(f"  {email}")

        elif choice == "6":
            show_events_summary(con)
            view = input("\nView events for a city? (enter city name or blank): ").strip()
            if view:
                rows = con.execute(
                    "SELECT event_name, date, webpage, email, phone FROM events WHERE city LIKE ? ORDER BY date",
                    (f"%{view}%",)
                ).fetchall()
                for r in rows:
                    print(f"\n  {r[0]}")
                    print(f"    Date: {r[1]}")
                    print(f"    URL:  {r[2]}")
                    print(f"    Email: {r[3]}")
                    print(f"    Phone: {r[4]}")

        elif choice == "7":
            export_events_xlsx(con)

        elif choice == "8":
            export_events_csv(con)

        elif choice == "9":
            visualize_events(con)

        elif choice == "10":
            con.close()
            print("Bye!")
            break

        else:
            print("Invalid choice.")
