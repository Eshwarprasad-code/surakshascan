"""
Evaluation, not training: sends each message in test_messages.json to
your OWN running API (must have `uvicorn app.main:app --reload` running
in another terminal first) and compares the result against the
dataset's original label. Reports accuracy and saves misclassified
examples so you know exactly what to look at / adjust in the heuristic
keyword banks or the LLM prompt.
"""
import json
import time
import httpx

API_URL = "http://localhost:8000/analyze"

with open("data/test_messages.json", "r", encoding="utf-8") as f:
    test_set = json.load(f)

results = []
correct = 0
false_positives = []  # system said unsafe, dataset says safe
false_negatives = []  # system said safe, dataset says unsafe

print(f"Running {len(test_set)} messages through {API_URL}...")
print("(this will take a while — one request at a time, ~2-5 sec each)\n")

with httpx.Client(timeout=60.0, trust_env=False) as client:
    for i, item in enumerate(test_set):
        try:
            resp = client.post(API_URL, json={"message": item["text"]})
            resp.raise_for_status()
            data = resp.json()
        except httpx.HTTPStatusError as e:
            # Print the actual detail field from our API's error response,
            # not just the generic status code — this is what tells us
            # rate-limit vs something else without guessing.
            try:
                detail = e.response.json().get("detail", "(no detail)")
            except Exception:
                detail = e.response.text[:200]
            print(f"[{i}] Request failed ({e.response.status_code}): {detail}")
            continue
        except Exception as e:
            print(f"[{i}] Request failed: {e}")
            continue

        system_unsafe = data["risk_level"] in ("Suspicious", "High Risk")
        expected_unsafe = item["expected_unsafe"]
        is_correct = system_unsafe == expected_unsafe
        correct += is_correct

        result = {
            "text": item["text"][:100],
            "expected_unsafe": expected_unsafe,
            "system_risk_level": data["risk_level"],
            "system_unsafe": system_unsafe,
            "correct": is_correct,
            "source": item["source"],
        }
        results.append(result)

        if not is_correct:
            if system_unsafe and not expected_unsafe:
                false_positives.append(result)
            else:
                false_negatives.append(result)

        if (i + 1) % 10 == 0:
            print(f"  {i + 1}/{len(test_set)} done...")

        time.sleep(0.8)  # be polite to your own Groq rate limit

accuracy = correct / len(results) if results else 0

print(f"\n{'=' * 70}")
print(f"Accuracy: {correct}/{len(results)} = {accuracy:.1%}")
print(f"False positives (flagged safe messages as risky): {len(false_positives)}")
print(f"False negatives (missed actually risky messages): {len(false_negatives)}")
print(f"{'=' * 70}")

with open("data/eval_results.json", "w", encoding="utf-8") as f:
    json.dump({
        "accuracy": accuracy,
        "total": len(results),
        "correct": correct,
        "false_positives": false_positives,
        "false_negatives": false_negatives,
        "all_results": results,
    }, f, ensure_ascii=False, indent=2)

print("\nFull results saved to data/eval_results.json")
print("False negatives matter more than false positives here — a missed")
print("scam is worse than an over-cautious flag on a safe message. Review")
print("data/eval_results.json's false_negatives list first.")