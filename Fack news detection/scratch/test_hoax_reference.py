import urllib.request
import json
import time

time.sleep(3)

test_inputs = [
    (
        "Hoax Reference 1 (Private Vehicle Ban)",
        "A widely shared post falsely claims that a new law will ban all private vehicles in the city starting next year."
    ),
    (
        "Hoax Reference 2 (Soft Drink Recall Rumor)",
        "A rumor circulating online incorrectly states that a popular soft drink brand is being recalled worldwide due to contamination."
    ),
    (
        "Genuinely Real Claim (NASA)",
        "NASA's James Webb Space Telescope observed atmospheric water vapor on a rocky exoplanet in the habitable zone, confirmed by peer-reviewed findings in Nature Astronomy."
    ),
    (
        "Genuinely Fake Claim (Water Microchip)",
        "Urgent alert: Microchips found in bottled water to control human brainwaves, share before deleted!"
    )
]

print("=" * 80)
print(" HOAX-DESCRIBING / META-DISCOURSE VERIFICATION TESTS")
print("=" * 80)

for name, text in test_inputs:
    req = urllib.request.Request(
        "http://127.0.0.1:5000/api/predict",
        data=json.dumps({"text": text}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req) as resp:
            top_data = json.loads(resp.read().decode("utf-8"))
            data = top_data.get("data", {})
            print(f"\n[TEST CASE]: {name}")
            print(f"  Input: \"{text}\"")
            print(f"  Label: {data.get('label')}")
            print(f"  Verdict: {data.get('verdict')}")
            print(f"  Confidence: {data.get('confidence')}%")
            print(f"  Theme: {data.get('status_theme')}")
            print(f"  Message: {data.get('message')}")
            print(f"  Advisory: {data.get('verification_advisory')}")
            print("-" * 60)
    except Exception as e:
        print(f"Error calling API for {name}: {e}")

print("\n" + "=" * 80)
