import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from verification import check_web_corroboration, clean_query_text

s6 = "An announcement attributed to a school district claims that all students will be required to wear tracking bracelets starting next semester."
res = check_web_corroboration(s6)
print("Query used:", res["query_used"])
print("Trusted matches:", res["trusted_matches"])
for s in res["matched_sources"]:
    print("Domain:", s["domain"])
    print("Title:", s["title"])
    print("Matched terms:", s.get("matched_terms"))
    print("Snippet:", s["snippet"])
    print("---")
