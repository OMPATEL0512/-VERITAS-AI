import urllib.request
import json
import time

time.sleep(2)

queries = [
    "A fisherman in Alaska accidentally caught a fish believed to be over 100 years old, according to marine biologists who examined its growth rings.",
    "A woman in India gave birth on a moving train after the crew helped deliver the baby mid-journey, according to railway officials.",
    "A city in Germany began charging drivers extra to park oversized SUVs in narrow residential streets.",
    "A statement attributed to a national airline claims that passengers will soon be weighed along with their luggage before boarding, with ticket prices adjusted accordingly.",
    "A report citing internal sources at a major search engine company claims that it will begin charging users a monthly fee to keep search history private.",
    "An announcement attributed to a city's water department claims that tap water will be intentionally fluoridated at double the recommended levels starting next month."
]

for q in queries:
    req = urllib.request.Request(
        "http://127.0.0.1:5000/api/predict",
        data=json.dumps({"text": q}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))["data"]
        print(f"\nText: \"{q[:70]}...\"")
        print(f"  -> Label: {res['label']} ({res['confidence']}%) | Verdict: {res['verdict']}")
        print(f"  -> Web Matches: {res['web_corroboration']['trusted_matches']}")
        for s in res['web_corroboration']['matched_sources']:
            print(f"     * {s['domain']} | {s['title']}")
