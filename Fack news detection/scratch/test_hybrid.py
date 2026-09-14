import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.model.inference import predict

examples = [
    ("Test 1 (Japan clerical error)", "A man in Japan has been legally declared dead for three years despite being alive, after a clerical error at a local government office went unnoticed — officials have since apologized and corrected the record."),
    ("Test 2 (Twins superfetation UK hospital)", "Doctors were stunned after a woman gave birth to twins conceived three weeks apart, a rare medical phenomenon known as superfetation, confirmed by fertility specialists at a UK hospital."),
    ("Test 3 (Town debt-free bond disclosure)", "Government records show a small U.S. town accidentally became debt-free overnight after a decades-old bond was misfiled and legally expired, according to municipal financial disclosures."),
    ("Test 4 (Fake Microchips Hoax)", "SHOCKING REVEAL: Secret government microchips found in bottled water to control human brainwaves! Elites are terrified this secret leak is going viral! Share this urgent alert before it is permanently deleted by the deep state!"),
    ("Test 5 (Real NASA James Webb)", "NASA's James Webb Space Telescope has captured new high-resolution infrared spectrum data from a distant exoplanet, revealing previously obscured atmospheric water vapor and carbon dioxide structures. The international research team published their peer-reviewed findings in the Astrophysical Journal on Thursday.")
]

print("=== HYBRID MODEL INFERENCE TEST RESULTS ===\n")
for title, text in examples:
    res = predict(text)
    print(f"{title}:")
    print(f"  Label: {res['label']}")
    print(f"  Verdict: {res['verdict']}")
    print(f"  Confidence: {res['confidence']}%")
    print(f"  Citations Matched ({res['citation_info']['match_count']}): {res['citation_info']['matches']}")
    print(f"  Probabilities: Real {res['probabilities']['real']}% | Fake {res['probabilities']['fake']}%")
    print("-" * 60)
