import urllib.request
import json
import time

test_cases = [
    ("Case 1: Japan clerical error", "A man in Japan has been legally declared dead for three years despite being alive, after a clerical error at a local government office went unnoticed — officials have since apologized and corrected the record."),
    ("Case 2: Twins superfetation UK hospital", "Doctors were stunned after a woman gave birth to twins conceived three weeks apart, a rare medical phenomenon known as superfetation, confirmed by fertility specialists at a UK hospital."),
    ("Case 3: Town debt-free bond disclosure", "Government records show a small U.S. town accidentally became debt-free overnight after a decades-old bond was misfiled and legally expired, according to municipal financial disclosures.")
]

print("=== VERIFYING API HYBRID FIX OVER HTTP ===\n")
for name, txt in test_cases:
    req = urllib.request.Request(
        "http://127.0.0.1:5000/api/predict",
        data=json.dumps({"text": txt}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    res = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))
    data = res.get("data", {})
    print(f"{name}:")
    print(f"  Status: {res.get('status')}")
    print(f"  Label: {data.get('label')}")
    print(f"  Verdict: {data.get('verdict')}")
    print(f"  Confidence: {data.get('confidence')}%")
    print(f"  Architecture: {data.get('model_architecture')}")
    print(f"  Citations: {data.get('citation_info', {}).get('match_count')} matches -> {data.get('citation_info', {}).get('matches')}")
    print(f"  Probabilities: Real {data.get('probabilities', {}).get('real')}% | Fake {data.get('probabilities', {}).get('fake')}%")
    print("-" * 60)
