import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from verification import check_web_corroboration, clean_query_text
from ddgs import DDGS

for query_text in [
    "A city in South Korea installed solar panels on top of a highway median to generate power without using additional land.",
    "An announcement attributed to a school district claims that all students will be required to wear tracking bracelets starting next semester."
]:
    print("=" * 80)
    print("Testing:", query_text)
    print("Clean query:", clean_query_text(query_text))
    with DDGS() as ddgs:
        results = list(ddgs.text(clean_query_text(query_text), max_results=5))
        for r in results:
            print("---")
            print("Title:", r.get("title"))
            print("URL:", r.get("href"))
            print("Body:", r.get("body"))
