import urllib.request
import json
import time

time.sleep(2)

payload = {
    "text": '"An announcement attributed to a city\'s water department claims that tap water will be intentionally fluoridated at double the recommended levels starting next month."'
}

req = urllib.request.Request(
    "http://127.0.0.1:5000/api/predict",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

with urllib.request.urlopen(req) as resp:
    res = json.loads(resp.read().decode("utf-8"))["data"]
    print("LIVE SERVER RESPONSE:")
    print("Label:", res["label"])
    print("Verdict:", res["verdict"])
    print("Confidence:", res["confidence"])
    print("Web Matches:", res["web_corroboration"]["trusted_matches"])
