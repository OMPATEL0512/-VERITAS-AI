import urllib.request
import json
import time

time.sleep(3)

test_scenarios = [
    # 1. Adversarial Fake News (Spoofing real institutions with fabricated statistics/claims)
    (
        "Harvard Lifespan Claim (Adversarial Fake)",
        "A study credited to Harvard Medical School claims that drinking two cups of coffee daily reduces lifespan by an average of three years."
    ),
    (
        "WHO Virus Mortality (Adversarial Fake)",
        "A statement attributed to the World Health Organization claims that a newly discovered virus in Southeast Asia has a mortality rate of 60%, prompting international travel bans."
    ),
    (
        "Federal Reserve 5% Fee (Adversarial Fake)",
        "Reports citing an internal Federal Reserve memo suggest all savings accounts will require a mandatory 5% government withdrawal fee starting next year."
    ),
    # 2. Quirky & Absurd True Stories (Real news that sounds unusual)
    (
        "Scottish Whisky Aged at Sea (Absurd Real)",
        "A Scottish distillery released a whisky aged partly at sea, having spent months rolling on a cargo ship to see if ocean movement changes the flavor."
    ),
    (
        "Goldfish Driving Car on Land (Quirky Real)",
        "Scientists at Ben-Gurion University successfully trained goldfish to navigate a motorized wheeled vehicle across a room on land."
    ),
    # 3. High-Tech & Space Science (Legitimate complex claims)
    (
        "MIT Laundry Robot (Real Tech Claim)",
        "Researchers at MIT built a robot that can fold laundry, though it currently takes about 10 minutes per item, according to the published paper."
    ),
    (
        "NASA Exoplanet Atmosphere (Standard Real)",
        "NASA's James Webb Space Telescope observed atmospheric water vapor on a rocky exoplanet in the habitable zone, confirmed by peer-reviewed findings in Nature Astronomy."
    ),
    # 4. Debunking / Meta-Discourse Statements
    (
        "Private Vehicle Ban Hoax (Debunking / Meta-Reporting)",
        "A widely shared post falsely claims that a new law will ban all private vehicles in the city starting next year."
    ),
    # 5. Viral Hoax / Conspiracy
    (
        "Bottled Water Microchip (Blatant Hoax)",
        "Urgent alert: Microchips found in bottled water to control human brainwaves, share before deleted!"
    )
]

print("=" * 85)
print(" VERITASAI COMPREHENSIVE HARD & HARDEST NEWS DETECTION BENCHMARK")
print("=" * 85)

for name, text in test_scenarios:
    req = urllib.request.Request(
        "http://127.0.0.1:5000/api/predict",
        data=json.dumps({"text": text}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req) as resp:
            top_data = json.loads(resp.read().decode("utf-8"))
            data = top_data.get("data", {})
            web = data.get("web_corroboration", {})
            print(f"\n[SCENARIO]: {name}")
            print(f"  Input: \"{text[:75]}...\"")
            print(f"  Label: {data.get('label')}")
            print(f"  Verdict: {data.get('verdict')}")
            print(f"  Confidence: {data.get('confidence')}%")
            print(f"  Theme: {data.get('status_theme')}")
            print(f"  Web Matches: {web.get('trusted_matches', 0)} | FactCheck Debunk: {web.get('debunked_by_factcheck', False)}")
            print("-" * 65)
    except Exception as e:
        print(f"Error calling API for {name}: {e}")

print("\n" + "=" * 85)
