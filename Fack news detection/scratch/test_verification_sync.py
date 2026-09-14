import re
from typing import Dict, Any, List, Optional

try:
    from ddgs import DDGS
except ImportError:
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        DDGS = None

TRUSTED_DOMAINS = [
    "reuters.com", "apnews.com", "bbc.com", "bbc.co.uk", "npr.org", 
    "who.int", "nasa.gov", "nature.com", "sciencedirect.com",
    "cdc.gov", "nih.gov", "theguardian.com", "nytimes.com",
    "washingtonpost.com", "aljazeera.com", "mit.edu", "stanford.edu",
    "harvard.edu", "smithsonianmag.com", "scientificamerican.com",
    "technologyreview.com", "thelocal.se", "bloomberg.com", "wsj.com",
    "thehindu.com", "ndtv.com", "indianexpress.com", "politifact.com",
    "snopes.com", "factcheck.org", "thehill.com", "cbsnews.com",
    "nbcnews.com", "abcnews.go.com", "upi.com", "therecord.com",
    "usatoday.com", "cnn.com", "time.com", "independent.co.uk",
    "telegraph.co.uk", "altnews.in", "boomlive.in"
]

FACT_CHECK_SITES = [
    "politifact.com", "snopes.com", "factcheck.org", "reuters.com/fact-check",
    "altnews.in", "boomlive.in", "bbc.com/news/reality_check", "afp.com/fact-check"
]

INSTITUTIONS_KEYWORD_MAP = {
    "mit": ["mit.edu", "massachusetts institute of technology", "mit news"],
    "stanford": ["stanford.edu", "stanford university", "stanford report"],
    "harvard": ["harvard.edu", "harvard university", "harvard medical"],
    "nasa": ["nasa.gov", "jet propulsion laboratory", "jpl"],
    "cdc": ["cdc.gov", "centers for disease control"],
    "who": ["who.int", "world health organization"],
    "world health organization": ["who.int", "world health organization"],
    "federal reserve": ["federalreserve.gov", "fed", "central bank"]
}

FILLER_PREFIXES = [
    r"^(?:a\s+widely\s+shared\s+post\s+(?:claims?|states?|says?)\s+that\s+)",
    r"^(?:a\s+viral\s+(?:post|video|image|message)\s+(?:claims?|states?)\s+that\s+)",
    r"^(?:a\s+rumor\s+(?:circulating|spreading)\s+online\s+(?:claims?|states?)\s+that\s+)",
    r"^(?:according\s+to\s+(?:reports|rumors|posts)\s+)",
    r"^(?:a\s+study\s+(?:credited|attributed)\s+to\s+[\w\s]+\s+claims?\s+that\s+)",
    r"^(?:a\s+statement\s+attributed\s+to\s+[\w\s]+\s+claims?\s+that\s+)",
    r"^(?:an?\s+(?:announcement|report|memo|statement)\s+attributed\s+to\s+[\w\s]+\s+claims?\s+that\s+)",
    r"^(?:an?\s+(?:announcement|report|memo|statement)\s+citing\s+[\w\s]+\s+claims?\s+that\s+)",
    r"^(?:reports\s+citing\s+an?\s+[\w\s]+\s+suggest\s+)",
    r"^(?:did\s+you\s+know\s+that\s+)",
    r"^(?:it\s+is\s+claimed\s+that\s+)",
    r"^(?:breaking\s*:\s*)",
    r"^(?:urgent\s*:\s*)"
]

SENSITIVE_PREDICATES = [
    r"\b(?:reduces?|shortens?|decreases?)\s+(?:[\w]+\s+)?(?:lifespan|life\s+expectancy)\b",
    r"\b(?:reduces?|decreases?)\s+(?:[\w]+\s+)?(?:iq|intelligence|brain\s+capacity)\b",
    r"\bmortality\s+rate\s+of\s+\d+%\b",
    r"\b\d+%\s+mortality\s+rate\b",
    r"\bmandatory\s+\d+%\s+(?:tax|fee|withdrawal)\b",
    r"\b100%\s+cures?\b",
    r"\bcures?\s+(?:cancer|diabetes|alzheimer|hiv|aids|covid)\b",
    r"\bban\s+all\s+private\s+vehicles\b",
    r"\bmicrochips?\s+(?:found\s+in|in)\s+water\b"
]

STOPWORDS = {
    "that", "this", "with", "from", "have", "will", "been", "they", "their",
    "about", "there", "which", "would", "could", "should", "more", "other",
    "than", "some", "also", "into", "then", "what", "when", "where", "after",
    "before", "says", "said", "claim", "claims", "claimed", "statement", "report",
    "reports", "citing", "attributed", "according", "announced", "announcement",
    "were", "being", "been", "does", "done", "must", "each", "every", "over",
    "such", "through", "under", "while", "during"
}

def clean_query_text(text: str) -> str:
    """Strips meta-filler, quotes, leading punctuation to extract the core factual claim for search."""
    cleaned = text.strip()
    # Strip leading bullets, numbers, dots, quotes
    cleaned = re.sub(r"^[\s\.\,\'\"\“\”\‘\’\-\*\#\:\;\(\)\[\]\d]+", "", cleaned).strip()
    cleaned = re.sub(r"[\'\"\“\”\‘\’]+$", "", cleaned).strip()
    
    # Strip common filler prefixes
    for p in FILLER_PREFIXES:
        cleaned = re.sub(p, "", cleaned, flags=re.IGNORECASE).strip()
    
    # Strip leading quotes again if stripped filler revealed quotes
    cleaned = re.sub(r"^[\s\.\,\'\"\“\”\‘\’\-\*\#\:\;\(\)\[\]]+", "", cleaned).strip()
    cleaned = re.sub(r"[\'\"\“\”\‘\’]+$", "", cleaned).strip()

    words = cleaned.split()
    return " ".join(words[:18]).strip()

def check_web_corroboration_v2(text: str, max_results: int = 8) -> Dict[str, Any]:
    if not text or not text.strip():
        return {
            "corroborated": False,
            "trusted_matches": 0,
            "debunked_by_factcheck": False,
            "score": 0.0,
            "matched_sources": [],
            "query_used": ""
        }

    query = clean_query_text(text)
    
    # Extract substantive content words for strict relevance matching
    raw_words = re.findall(r"\b[a-zA-Z]{3,}\b", query.lower())
    content_words = [w for w in raw_words if w not in STOPWORDS]

    if DDGS is None:
        return {
            "corroborated": False,
            "trusted_matches": 0,
            "debunked_by_factcheck": False,
            "score": 0.0,
            "matched_sources": [],
            "query_used": query,
            "error": "DDGS search package not available."
        }

    results = []
    try:
        with DDGS() as ddgs:
            raw_res = ddgs.text(query, max_results=max_results)
            if raw_res:
                results = list(raw_res)
    except Exception as e:
        return {
            "corroborated": False,
            "trusted_matches": 0,
            "debunked_by_factcheck": False,
            "score": 0.0,
            "matched_sources": [],
            "query_used": query,
            "error": str(e)
        }

    text_lower = text.lower()
    named_inst = None
    for inst_key in INSTITUTIONS_KEYWORD_MAP:
        if inst_key in text_lower:
            named_inst = inst_key
            break

    sensitive_preds = [p for p in SENSITIVE_PREDICATES if re.search(p, text_lower)]

    trusted_sources = []
    trusted_matches = 0
    debunked_by_factcheck = False
    factcheck_match_notes = []

    for r in results:
        url = (r.get("href", "") or r.get("link", "")).lower()
        title = r.get("title", "")
        body = r.get("body", "") or r.get("snippet", "")
        combined_text = (title + " " + body).lower()
        
        # Count overlapping content words in title/snippet
        overlapping_words = [w for w in content_words if w in combined_text]
        overlap_count = len(overlapping_words)
        
        # Check fact-check sites
        is_factcheck_site = any(fc in url for fc in FACT_CHECK_SITES)
        if is_factcheck_site and overlap_count >= min(2, len(content_words)):
            if any(term in combined_text for term in ["false", "hoax", "debunk", "fake", "incorrect", "pants on fire", "misleading", "myth", "untrue"]):
                debunked_by_factcheck = True
                factcheck_match_notes.append({
                    "domain": "Fact Check Debunk",
                    "title": title,
                    "url": r.get("href", "") or r.get("link", ""),
                    "snippet": body[:160] + "..." if len(body) > 160 else body
                })

        matched_domain = None
        for domain in TRUSTED_DOMAINS:
            if domain in url:
                matched_domain = domain
                break

        if matched_domain:
            # STRICT RELEVANCE: Require at least 2 content keywords to match title/snippet
            # This prevents random articles (e.g. Al Jazeera Trump auto plants) from matching a telecom rumor!
            min_required = 2 if len(content_words) >= 3 else 1
            if overlap_count < min_required:
                continue

            # Institution check
            if named_inst:
                inst_valid = any(kw in url or kw in combined_text for kw in INSTITUTIONS_KEYWORD_MAP[named_inst])
                if not inst_valid:
                    continue

            # Sensitive predicate check
            if sensitive_preds:
                predicate_supported = any(re.search(p, combined_text) for p in sensitive_preds)
                if not predicate_supported:
                    continue

            trusted_matches += 1
            trusted_sources.append({
                "domain": matched_domain,
                "title": title,
                "url": r.get("href", "") or r.get("link", ""),
                "snippet": body[:160] + "..." if len(body) > 160 else body,
                "matched_terms": overlapping_words
            })

    score = round(min(trusted_matches * 0.2, 0.5), 2)
    return {
        "corroborated": trusted_matches > 0,
        "trusted_matches": trusted_matches,
        "debunked_by_factcheck": debunked_by_factcheck,
        "factcheck_notes": factcheck_match_notes,
        "score": score,
        "matched_sources": trusted_sources,
        "query_used": query
    }

# Test with the exact sentence from user
test_s = '. "A statement attributed to a national telecom company claims that all customers will be required to submit fingerprint data to keep their phone lines active."'
print("Query extracted:", clean_query_text(test_s))
res = check_web_corroboration_v2(test_s)
print("Corroboration result:", res)
