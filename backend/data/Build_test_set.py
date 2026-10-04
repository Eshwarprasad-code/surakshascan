"""
Lightweight, non-training use of the datasets we inspected:

1. Pull a manageable, diverse sample into one clean JSON file
   (backend/data/test_messages.json) with a normalized shape:
   {text, expected_unsafe, category, language, source}
   "expected_unsafe" is just True/False — did the original dataset
   consider this a scam/spam? Keeping it binary (not the 3-tier
   Safe/Suspicious/High Risk your app uses) makes evaluation simple:
   we're only checking "did the system correctly treat this as
   risky vs not", not trying to match exact score bands.

2. Print word-frequency suggestions: words that show up much more
   often in the "unsafe" messages than the "safe" ones. These are
   candidates to manually review and add to the keyword banks in
   app/services/heuristics/*.py — this is NOT automated learning,
   just a shortcut so you're not reading thousands of rows by hand.
"""
import json
import random
from collections import Counter
from datasets import load_dataset

random.seed(42)
test_set = []

# ---- sidzzz07: large, real, but mostly English/Singlish. Use for
# volume + keyword-frequency signal, stratified sample to keep it
# manageable and not overwhelmingly dominate the test set.
print("Pulling from sidzzz07/scamshield-dataset...")
ds1 = load_dataset("sidzzz07/scamshield-dataset")["train"]
scam_rows = [r for r in ds1 if r["is_scam"] == 1]
safe_rows = [r for r in ds1 if r["is_scam"] == 0]
sample1 = random.sample(scam_rows, min(80, len(scam_rows))) + \
          random.sample(safe_rows, min(80, len(safe_rows)))
for r in sample1:
    test_set.append({
        "text": r["text"],
        "expected_unsafe": bool(r["is_scam"]),
        "category": r.get("head2_scam_intent", "unknown"),
        "language": r.get("language", "unknown"),
        "source": "sidzzz07",
    })

# ---- ganesh9353: tiny but well-labeled and multilingual. Take all
# of it — 120 rows is small enough to just keep everything.
print("Pulling from ganesh9353/Indian_Multilingual_Scam_Message_Dataset...")
ds2 = load_dataset("ganesh9353/Indian_Multilingual_Scam_Message_Dataset")["train"]
for r in ds2:
    test_set.append({
        "text": r["message"],
        "expected_unsafe": r["label"] == "scam",
        "category": r.get("domain", "unknown"),
        "language": r.get("language", "unknown"),
        "source": "ganesh9353",
    })

# ---- anmolshrivastav: real-looking spam/ham, no language field
# (assume English/Hinglish based on sample content).
print("Pulling from anmolshrivastav/scam-hum-india...")
ds3 = load_dataset("anmolshrivastav/scam-hum-india")["train"]
spam_rows = [r for r in ds3 if r["label"] == "spam"]
ham_rows = [r for r in ds3 if r["label"] == "ham"]
sample3 = random.sample(spam_rows, min(50, len(spam_rows))) + \
          random.sample(ham_rows, min(50, len(ham_rows)))
for r in sample3:
    test_set.append({
        "text": r["text"],
        "expected_unsafe": r["label"] == "spam",
        "category": "unknown",
        "language": "unknown",
        "source": "anmolshrivastav",
    })

random.shuffle(test_set)

with open("data/test_messages.json", "w", encoding="utf-8") as f:
    json.dump(test_set, f, ensure_ascii=False, indent=2)

print(f"\nSaved {len(test_set)} test messages to data/test_messages.json")

# ---- Keyword candidate suggestions (English only — the multilingual
# rows are too few to get reliable frequency signal from).
print("\n" + "=" * 70)
print("Keyword candidates (words far more common in unsafe vs safe text)")
print("=" * 70)

english_rows = [r for r in test_set if r["language"] in ("English", "en", "unknown")]
unsafe_words = Counter()
safe_words = Counter()
for r in english_rows:
    words = [w.strip(".,!?:;\"'()").lower() for w in r["text"].split()]
    words = [w for w in words if len(w) > 3]  # skip tiny filler words
    if r["expected_unsafe"]:
        unsafe_words.update(words)
    else:
        safe_words.update(words)

candidates = []
for word, unsafe_count in unsafe_words.most_common(200):
    safe_count = safe_words.get(word, 0)
    # word appears at least 3x in unsafe text and is rare/absent in safe text
    if unsafe_count >= 3 and safe_count <= 1:
        candidates.append((word, unsafe_count, safe_count))

for word, u, s in candidates[:30]:
    print(f"  {word:20s}  unsafe={u:3d}  safe={s}")

print(f"\n{len(candidates)} candidates found. Review these manually — some will be")
print("noise (names, dataset-specific artifacts) — and add the genuinely useful")
print("ones to the category_keywords dicts in app/services/heuristics/english.py")