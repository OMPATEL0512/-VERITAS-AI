import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ddgs import DDGS
from verification import TRUSTED_DOMAINS, FACT_CHECK_SITES, INSTITUTIONS_KEYWORD_MAP, SENSITIVE_PREDICATES, STOPWORDS

s2 = "A city in South Korea installed solar panels on top of a highway median to generate power without using additional land."

# Better clean query:
import re
cleaned = s2.strip()
cleaned = re.sub(r"^[\s\.\,\'\"\“\”\‘\’\-\*\#\:\;\(\)\[\]\d]+", "", cleaned).strip()
cleaned = re.sub(r"[\'\"\“\”\‘\’]+$", "", cleaned).strip()

print("Original:", s2)
print("Searching DDGS with:", cleaned)

with DDGS() as ddgs:
    res = list(ddgs.text(cleaned, max_results=8))
    for r in res:
        url = r.get("href", "")
        title = r.get("title", "")
        body = r.get("body", "")
        combined = (title + " " + body).lower()
        matched = [d for d in TRUSTED_DOMAINS if d in url.lower()]
        print("URL:", url, "Matched Domains:", matched)
        raw_words = re.findall(r"\b[a-zA-Z]{3,}\b", cleaned.lower())
        c_words = [w for w in raw_words if w not in STOPWORDS]
        overlap = [w for w in c_words if w in combined]
        print("  Overlap:", overlap)
