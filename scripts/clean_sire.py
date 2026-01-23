#scraper - gets raw text
#cleaner - makes it rag ready

from pathlib import Path

# ---------- File paths ----------
# Always resolve paths relative to this script (robust approach)
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_FILE = BASE_DIR / "data" / "sire_page.txt"
CLEAN_FILE = BASE_DIR / "data" / "sire_clean.txt"

# ---------- Read raw scraped text ----------
raw_text = RAW_FILE.read_text(encoding="utf-8")

# ---------- Trim obvious junk (top & bottom) ----------
start_marker = "International Research Experience (SIRE)"
end_marker = "Copyright ©"

# Keep only the meaningful part of the document
if start_marker in raw_text and end_marker in raw_text:
    raw_text = raw_text.split(start_marker, 1)[1]
    raw_text = raw_text.split(end_marker, 1)[0]

# ---------- Define section headings we care about ----------
sections = [
    "Objectives",
    "Eligibility",
    "Selection",
    "Nature & Duration of Support",
    "Guidelines",
    "How To Apply Online"
]

clean_output = []

# ---------- Extract sections ----------
for i, section in enumerate(sections):
    if section not in raw_text:
        continue

    # Start of this section
    start = raw_text.find(section)

    # End = start of next section (or end of text)
    if i + 1 < len(sections) and sections[i + 1] in raw_text:
        end = raw_text.find(sections[i + 1])
        section_text = raw_text[start:end]
    else:
        section_text = raw_text[start:]

    # Clean spacing and tag section
    section_text = section_text.strip()
    clean_output.append(f"[SECTION: {section}]\n{section_text}\n")

# ---------- Save cleaned content ----------
CLEAN_FILE.write_text("\n".join(clean_output), encoding="utf-8")

print("Cleaning complete — saved to data/sire_clean.txt")
