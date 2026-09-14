"""
Flask Application Backend for Fake News Detection.
Serves interactive web UI and provides REST APIs for single/batch predictions,
OCR text parsing, live fact-checking search, analytics telemetry, and URL scraping.
"""

import os
import sys
import time
import json
import re
from collections import Counter
from flask import Flask, render_template, request, jsonify, send_from_directory

try:
    import requests
    from bs4 import BeautifulSoup
    has_scraping = True
except ImportError:
    import urllib.request
    has_scraping = False

try:
    from flask_cors import CORS
    has_cors = True
except ImportError:
    has_cors = False

# Ensure model directory is on sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.model.inference import get_classifier

app = Flask(__name__, template_folder="templates", static_folder="static")
if has_cors:
    CORS(app)
else:
    @app.after_request
    def add_cors_headers(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        return response

# Session in-memory store for recent analyses
analysis_history = []

SAMPLE_ARTICLES = {
    "real": [
        {
            "title": "NASA's James Webb Telescope Discovers Distant Exoplanet Atmosphere",
            "source": "Science & Space Journal",
            "text": "NASA's James Webb Space Telescope has captured new high-resolution infrared spectrum data from a distant exoplanet, revealing previously obscured atmospheric water vapor and carbon dioxide structures. The international research team published their peer-reviewed findings in the Astrophysical Journal on Thursday, noting that the observational benchmarks corroborate long-standing theoretical planetary models."
        },
        {
            "title": "Federal Reserve Maintains Benchmark Interest Rates Following Inflation Review",
            "source": "Global Financial Gazette",
            "text": "The Federal Reserve announced on Wednesday that it will maintain current benchmark interest rates following a comprehensive assessment of recent inflation data and national labor market stability. Officials indicated during the press conference that monetary policy will remain data-dependent to ensure long-term economic equilibrium."
        },
        {
            "title": "Renewable Energy Investments Surge by 22% in Global Infrastructure Quarter",
            "source": "Economic Energy Review",
            "text": "Quarterly financial filings show renewable energy investments surged by 22% in the second quarter, driven by solar infrastructure expansions and offshore wind initiatives across North America and Europe. Government agencies and private sector consortiums confirmed the milestone in an official joint statement."
        }
    ],
    "fake": [
        {
            "title": "SHOCKING REVEAL: Secret Government Microchips Found in Bottled Water!",
            "source": "Conspiracy Express",
            "text": "SHOCKING REVEAL: Whistleblowers have EXPOSED that secret government microchips are being placed inside ordinary grocery store drinking water bottles to control human brainwaves! Elites are terrified this secret leak is going viral! Share this urgent alert before it is permanently deleted by the deep state!"
        },
        {
            "title": "MIRACLE CURE: Drinking Boiled Lemon Peel Cures All Illnesses in 48 Hours!",
            "source": "Hidden Health Secrets",
            "text": "Doctors are furious! A local grandmother has completely DESTROYED the $50 Billion pharmaceutical industry with one weird boiled kitchen lemon peel trick! Big pharma is trying to ban this ancient remedy immediately, wake up sheeple and share this hidden miracle truth now!"
        },
        {
            "title": "LEAKED: Global Leaders Replace Moon with Giant Artificial Hologram!",
            "source": "Forbidden Truth Today",
            "text": "UNBELIEVABLE PROOF: Leaked secret military documents reveal that the moon was replaced by a giant hollow surveillance hologram during last month's eclipse! Anonymous insiders confirm world leaders hold secret alien summits inside the hollow satellite!"
        }
    ]
}

# Curated Fact-Check Knowledge Base for Instant Matching
FACT_CHECK_DATABASE = [
    {
        "keywords": ["lemon", "water", "cure", "cancer", "diabetes", "disease", "नींबू", "इलाज"],
        "claim": "Drinking hot lemon water cures cancer, diabetes, and all diseases in 48 hours.",
        "claimant": "Viral Social Media Posts",
        "rating": "False / Fabricated Medical Claim",
        "rating_level": "false",
        "fact_checker": "World Health Organization & PolitiFact",
        "fact_check_url": "https://www.politifact.com/factchecks/coronavirus/",
        "summary": "Medical oncologists and WHO confirm lemon water cannot cure metabolic diseases or malignant tumors."
    },
    {
        "keywords": ["microchip", "water", "bottle", "brainwave", "mind control", "माइक्रोचिप", "साजिश"],
        "claim": "Secret government microchips are inserted into grocery bottled water to control human brainwaves.",
        "claimant": "Conspiracy Forums & WhatsApp Forwards",
        "rating": "False / Unsubstantiated Conspiracy",
        "rating_level": "false",
        "fact_checker": "Snopes Fact Check",
        "fact_check_url": "https://www.snopes.com/fact-check/",
        "summary": "No microchip technology capable of mind control exists in consumer beverage packaging."
    },
    {
        "keywords": ["moon", "hologram", "artificial", "satellite", "eclipse", "चांद"],
        "claim": "The moon is an artificial surveillance hologram built by ancient extraterrestrials.",
        "claimant": "Anonymous Video Channels",
        "rating": "Pants on Fire / Debunked",
        "rating_level": "false",
        "fact_checker": "Reuters Fact Check",
        "fact_check_url": "https://www.reuters.com/fact-check/",
        "summary": "Astronomical data and lunar orbital mechanics disprove hollow or artificial moon theories."
    },
    {
        "keywords": ["nasa", "perseverance", "mars", "rover", "jezero", "नासा", "मंगल"],
        "claim": "NASA Perseverance rover analyzes rock samples on Mars to search for ancient microbial biosignatures.",
        "claimant": "NASA & Jet Propulsion Laboratory",
        "rating": "Verified Authentic / True",
        "rating_level": "true",
        "fact_checker": "NASA & Astrophysical Journal",
        "fact_check_url": "https://mars.nasa.gov/mars2020/",
        "summary": "Peer-reviewed findings confirm ongoing exploratory sample collection by the Perseverance science payload."
    },
    {
        "keywords": ["federal reserve", "interest rate", "inflation", "economy", "आरबीआई"],
        "claim": "Federal Reserve maintains benchmark interest rates based on economic reviews.",
        "claimant": "Federal Reserve Board Press Release",
        "rating": "Verified Official Record",
        "rating_level": "true",
        "fact_checker": "Associated Press & Bloomberg",
        "fact_check_url": "https://apnews.com/hub/federal-reserve",
        "summary": "Confirmed through official monetary policy releases and public board minutes."
    }
]


def extract_text_from_url(url: str) -> dict:
    """Extracts article title and clean paragraph text from a web URL."""
    if has_scraping:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }
        try:
            response = requests.get(url, headers=headers, timeout=8)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            title = ""
            if soup.title and soup.title.string:
                title = soup.title.string.strip()
            elif soup.find("h1"):
                title = soup.find("h1").get_text().strip()

            paragraphs = soup.find_all("p")
            body_text = " ".join([p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 30])

            if len(body_text) < 50:
                return {"error": "Could not extract sufficient article text from the URL. Please copy and paste the text directly."}

            full_content = f"{title}\n\n{body_text}".strip()
            return {"title": title, "content": full_content, "url": url}
        except Exception as e:
            return {"error": f"Failed to fetch URL ({str(e)}). Please copy and paste article text manually."}
    else:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                html = resp.read().decode("utf-8", errors="ignore")
                title_match = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
                title = title_match.group(1).strip() if title_match else ""
                clean = re.sub(r"<[^>]+>", " ", html)
                clean = re.sub(r"\s+", " ", clean).strip()
                if len(clean) > 2000:
                    clean = clean[:2000]
                return {"title": title, "content": f"{title}\n\n{clean}".strip(), "url": url}
        except Exception as e:
            return {"error": f"Scraping error ({str(e)}). Install beautifulsoup4 or paste text directly."}


@app.route("/")
def index():
    """Serves the main application interface."""
    return render_template("index.html")


@app.route("/api/predict", methods=["POST"])
def predict():
    """Analyzes a single news article provided via text, OCR text, or URL."""
    data = request.get_json(force=True, silent=True) or {}
    text = data.get("text", "").strip()
    url = data.get("url", "").strip()
    source_type = data.get("source_type", "text") # "text", "ocr", "url"
    extracted_title = ""

    # If URL provided, fetch content
    if url:
        scraped = extract_text_from_url(url)
        if "error" in scraped:
            return jsonify({"status": "error", "message": scraped["error"]}), 400
        text = scraped["content"]
        extracted_title = scraped.get("title", "")
        source_type = "url"

    if not text:
        return jsonify({"status": "error", "message": "Please enter news text, upload an image, or provide a valid URL."}), 400

    if len(text.split()) < 3:
        return jsonify({"status": "error", "message": "Input is too short. Please provide at least 3 words for an accurate evaluation."}), 400

    start_time = time.time()
    classifier = get_classifier()
    result = classifier.predict(text)
    latency_ms = round((time.time() - start_time) * 1000, 1)

    result["latency_ms"] = latency_ms
    result["url"] = url if url else None
    result["source_type"] = source_type
    result["title"] = extracted_title if extracted_title else (text[:80] + "..." if len(text) > 80 else text)
    result["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
    result["id"] = int(time.time() * 1000)
    result["full_text"] = text

    # Search matching fact-checks for cross-referencing
    matched_checks = search_fact_checks(text)
    result["fact_checks"] = matched_checks

    # Store in history (limit to last 50)
    analysis_history.insert(0, result)
    if len(analysis_history) > 50:
        analysis_history.pop()

    return jsonify({"status": "success", "data": result})


def search_fact_checks(text: str) -> list:
    """Finds cross-referenced fact-checks based on keyword matching."""
    text_lower = text.lower()
    matches = []
    for item in FACT_CHECK_DATABASE:
        hit_count = sum(1 for kw in item["keywords"] if kw.lower() in text_lower)
        if hit_count >= 1:
            matches.append({
                "claim": item["claim"],
                "claimant": item["claimant"],
                "rating": item["rating"],
                "rating_level": item["rating_level"],
                "fact_checker": item["fact_checker"],
                "fact_check_url": item["fact_check_url"],
                "summary": item["summary"],
                "match_score": hit_count
            })
    matches.sort(key=lambda x: x["match_score"], reverse=True)
    return matches[:3]


@app.route("/api/factcheck-search", methods=["GET", "POST"])
def factcheck_search_endpoint():
    """Explicitly search fact-check database with query."""
    if request.method == "POST":
        data = request.get_json(force=True, silent=True) or {}
        query = data.get("query", "").strip() or data.get("q", "").strip()
    else:
        query = request.args.get("q", "").strip() or request.args.get("query", "").strip()

    if not query:
        return jsonify({"status": "success", "results": []})
    results = search_fact_checks(query)
    return jsonify({"status": "success", "results": results})


@app.route("/api/analytics", methods=["GET"])
def analytics_endpoint():
    """Aggregates session analytics and credibility telemetry."""
    total = len(analysis_history)
    if total == 0:
        return jsonify({
            "status": "success",
            "total_scans": 0,
            "real_count": 0,
            "fake_count": 0,
            "real_percentage": 0,
            "fake_percentage": 0,
            "avg_confidence": 0,
            "avg_latency_ms": 0,
            "top_keywords": [],
            "recent_timeline": []
        })

    real_count = sum(1 for item in analysis_history if item.get("label", "").lower() == "real")
    fake_count = total - real_count
    real_pct = round((real_count / total) * 100, 1)
    fake_pct = round((fake_count / total) * 100, 1)
    avg_conf = round(sum(item.get("confidence", 0) for item in analysis_history) / total, 1)
    avg_lat = round(sum(item.get("latency_ms", 0) for item in analysis_history) / total, 1)

    # Aggregate sensational keywords
    keyword_counter = Counter()
    for item in analysis_history:
        ling = item.get("linguistics", {})
        for kw in ling.get("sensational_words", []):
            keyword_counter[kw.lower()] += 1

    top_keywords = [{"keyword": kw, "count": cnt} for kw, cnt in keyword_counter.most_common(8)]

    timeline = [
        {
            "id": item.get("id"),
            "time": item.get("timestamp", "").split(" ")[1] if " " in item.get("timestamp", "") else item.get("timestamp", ""),
            "label": item.get("label"),
            "confidence": item.get("confidence"),
            "latency_ms": item.get("latency_ms", 0)
        }
        for item in reversed(analysis_history[:10])
    ]

    return jsonify({
        "status": "success",
        "total_scans": total,
        "real_count": real_count,
        "fake_count": fake_count,
        "real_percentage": real_pct,
        "fake_percentage": fake_pct,
        "avg_confidence": avg_conf,
        "avg_latency_ms": avg_lat,
        "top_keywords": top_keywords,
        "recent_timeline": timeline
    })


@app.route("/api/samples", methods=["GET"])
def get_samples():
    """Returns curated real and fake news samples for quick testing."""
    return jsonify({"status": "success", "samples": SAMPLE_ARTICLES})


@app.route("/api/history", methods=["GET", "DELETE"])
def history_endpoint():
    """Retrieves or clears the recent analysis history."""
    global analysis_history
    if request.method == "DELETE":
        analysis_history = []
        return jsonify({"status": "success", "message": "History cleared successfully."})
    return jsonify({"status": "success", "history": analysis_history})


@app.route("/api/health", methods=["GET"])
def health():
    """API health check and classifier status."""
    classifier = get_classifier()
    return jsonify({
        "status": "healthy",
        "model_architecture": classifier.model_type,
        "history_count": len(analysis_history)
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Fake News Detector Server starting at http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
