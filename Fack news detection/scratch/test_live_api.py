import urllib.request
import json

payload = {
    "text": '. "A statement attributed to a national telecom company claims that all customers will be required to submit fingerprint data to keep their phone lines active."'
}

req = urllib.request.Request(
    "http://127.0.0.1:5000/api/predict",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

with urllib.request.urlopen(req) as resp:
    res = json.loads(resp.read().decode("utf-8"))
    print("API RESPONSE SUCCESS:")
    print("Label:", res["data"]["label"])
    print("Verdict:", res["data"]["verdict"])
    print("Confidence:", res["data"]["confidence"])
    print("Web Corroboration Matches:", res["data"]["web_corroboration"]["trusted_matches"])
    print("Transparency Notice:", res["data"].get("transparency_notice"))
