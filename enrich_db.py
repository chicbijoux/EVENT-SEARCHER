"""One-shot script: generate proper AI summaries for all DB events, update DB, re-export CSV."""
import os, sys, json, re, csv, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"), override=True)
except ImportError:
    pass

from email_scraper import init_db, clean_summary, CSV_PATH

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
if not ANTHROPIC_API_KEY:
    sys.exit("ERROR: ANTHROPIC_API_KEY not set in .env")

import anthropic
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

con = init_db()
rows = con.execute(
    "SELECT id, event_name, city, date, summary FROM events ORDER BY id"
).fetchall()

if not rows:
    sys.exit("No events in DB.")

print(f"Found {len(rows)} events. Generating summaries...")

items = [
    {"i": i, "id": r[0], "name": r[1], "city": r[2], "date": r[3], "raw": clean_summary(r[4] or "")[:400]}
    for i, r in enumerate(rows)
]

CHUNK = 40
updated_summaries = {}

for start in range(0, len(items), CHUNK):
    chunk = items[start:start + CHUNK]
    print(f"  Chunk {start+1}–{start+len(chunk)} / {len(items)}...")

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
        raw_text = re.sub(r"^```(?:json)?\s*", "", raw_text)
        raw_text = re.sub(r"\s*```$", "", raw_text)
        results = json.loads(raw_text)
        for r in results:
            idx = r.get("i")
            summary = r.get("summary", "").strip()
            if idx is not None and summary:
                db_id = items[idx]["id"]
                updated_summaries[db_id] = summary
    except Exception as e:
        print(f"  WARNING: chunk failed — {e}")

    time.sleep(0.5)

# Update DB
print(f"\nUpdating {len(updated_summaries)} records in DB...")
for db_id, summary in updated_summaries.items():
    con.execute("UPDATE events SET summary = ? WHERE id = ?", (summary, db_id))
con.commit()

# Re-export CSV
rows_all = con.execute(
    "SELECT event_name, city, date, webpage, email, phone, summary, timestamp "
    "FROM events ORDER BY city, date"
).fetchall()
con.close()

with open(CSV_PATH, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["event_name", "city", "date", "webpage", "email", "phone", "summary", "saved_at"])
    w.writerows(rows_all)

print(f"Done. CSV written to: {CSV_PATH}")
print("Sample summaries:")
for row in rows_all[:3]:
    print(f"  [{row[0][:40]}] {row[6][:120]}")
