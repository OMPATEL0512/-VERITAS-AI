import urllib.request
import json
import time

cases = [
    ("Real: Alaska Fish", "A fisherman in Alaska accidentally caught a fish believed to be over 100 years old, according to marine biologists who examined its growth rings.", "Real"),
    ("Real: Train Delivery", "A woman in India gave birth on a moving train after the crew helped deliver the baby mid-journey, according to railway officials.", "Real"),
    ("Real: Insect Bakery", "A bakery in France began selling bread made with insect flour as a sustainable protein alternative, following new EU food regulations permitting the ingredient.", "Real"),
    ("Real: Solar Highway", "A city in South Korea installed solar panels on top of a highway median to generate power without using additional land.", "Real"),
    ("Fake: Fluoride Water", "\"An announcement attributed to a city's water department claims that tap water will be intentionally fluoridated at double the recommended levels starting next month.\"", "Fake"),
    ("Fake: Telecom Fingerprints", '. "A statement attributed to a national telecom company claims that all customers will be required to submit fingerprint data to keep their phone lines active."', "Fake"),
    ("Fake: Bank Freeze", "A report citing an anonymous insider at a major bank claims that all customer accounts will be frozen for 48 hours next month for a 'mandatory system upgrade.'", "Fake"),
    ("Fake: Tracking Bracelets", "An announcement attributed to a school district claims that all students will be required to wear tracking bracelets starting next semester.", "Fake")
]

print("=" * 80)
print("COMPREHENSIVE MULTI-CASE VALIDATION")
print("=" * 80)

for name, text, expected in cases:
    req = urllib.request.Request(
        "http://127.0.0.1:5000/api/predict",
        data=json.dumps({"text": text}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))["data"]
        actual = res["label"]
        status = "PASSED" if actual == expected else "FAILED"
        print(f"[{status}] {name} -> Expected: {expected} | Actual: {actual} ({res['confidence']}%) | Verdict: {res['verdict']}")
