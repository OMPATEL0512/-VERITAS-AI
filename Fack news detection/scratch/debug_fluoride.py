import sys, os
import re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from verification import clean_query_text, check_web_corroboration
from backend.model.inference import predict, GENERIC_RUMOR_PATTERNS

s = '"An announcement attributed to a city\'s water department claims that tap water will be intentionally fluoridated at double the recommended levels starting next month."'

print("Query extracted:", clean_query_text(s))
print("Generic rumor match:", [p for p in GENERIC_RUMOR_PATTERNS if re.search(p, s, re.IGNORECASE)])
print("Prediction:", predict(s))
