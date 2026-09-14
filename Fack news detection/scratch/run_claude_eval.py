import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.model.inference import predict

test_cases = [
    # 3 Real from Claude AI screenshot
    ("Real 1 (Insect flour)", "A bakery in France began selling bread made with insect flour as a sustainable protein alternative, following new EU food regulations permitting the ingredient."),
    ("Real 2 (Solar highway)", "A city in South Korea installed solar panels on top of a highway median to generate power without using additional land."),
    ("Real 3 (Filtration)", "A teenager in the US built a low-cost water filtration device for a school science project, which was later adopted by a local nonprofit for use in rural areas."),
    
    # 3 Fake from Claude AI screenshot
    ("Fake 4 (Telecom Fingerprint)", '. "A statement attributed to a national telecom company claims that all customers will be required to submit fingerprint data to keep their phone lines active."'),
    ("Fake 5 (Bank freeze)", "A report citing an anonymous insider at a major bank claims that all customer accounts will be frozen for 48 hours next month for a 'mandatory system upgrade.'"),
    ("Fake 6 (Tracking bracelets)", "An announcement attributed to a school district claims that all students will be required to wear tracking bracelets starting next semester.")
]

print("=" * 80)
print("BENCHMARKING 6 CASES")
print("=" * 80)

for name, text in test_cases:
    res = predict(text)
    label = res.get('label')
    verdict = res.get('verdict')
    conf = res.get('confidence')
    matches = res.get('web_corroboration', {}).get('trusted_matches', 0)
    print(f"[{name}] -> {label} ({conf}%) | {verdict} | Web Matches: {matches}")
