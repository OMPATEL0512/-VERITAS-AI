import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.model.inference import predict
from verification import check_web_corroboration

test_cases = [
    # Real
    ("Real 1 (Insect flour)", "A bakery in France began selling bread made with insect flour as a sustainable protein alternative, following new EU food regulations permitting the ingredient."),
    ("Real 2 (Solar highway)", "A city in South Korea installed solar panels on top of a highway median to generate power without using additional land."),
    ("Real 3 (Filtration)", "A teenager in the US built a low-cost water filtration device for a school science project, which was later adopted by a local nonprofit for use in rural areas."),
    # Fake
    ("Fake 4 (Telecom Fingerprint)", '. "A statement attributed to a national telecom company claims that all customers will be required to submit fingerprint data to keep their phone lines active."'),
    ("Fake 5 (Bank freeze)", 'A report citing an anonymous insider at a major bank claims that all customer accounts will be frozen for 48 hours next month for a \'mandatory system upgrade.\''),
    ("Fake 6 (Tracking bracelets)", 'An announcement attributed to a school district claims that all students will be required to wear tracking bracelets starting next semester.')
]

print("=" * 80)
print("TESTING CLAUDE AI SAMPLES")
print("=" * 80)

for name, text in test_cases:
    print(f"\n--- {name} ---")
    print(f"Input: {text}")
    res = predict(text)
    print(f"Label: {res.get('label')} | Verdict: {res.get('verdict')} | Conf: {res.get('confidence')}%")
    web = res.get('web_corroboration', {})
    print(f"Web Corroboration: matches={web.get('trusted_matches')}, query='{web.get('query_used')}'")
    for s in web.get('matched_sources', []):
        print(f"   -> Source: {s.get('domain')} | Title: {s.get('title')}")
