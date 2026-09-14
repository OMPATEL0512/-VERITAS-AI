import time
from transformers import pipeline

MODEL = "jy46604790/Fake-News-Bert-Detect"
print(f"Loading {MODEL}...")
t0 = time.time()
clf = pipeline("text-classification", model=MODEL, tokenizer=MODEL, truncation=True, max_length=512)
print(f"Model loaded in {time.time() - t0:.2f}s")

def predict(text: str):
    result = clf(text)[0]
    label = "Real" if result["label"] == "LABEL_1" else "Fake"
    confidence = result["score"]
    return {"label": label, "confidence": confidence, "raw": result}

real_text = "NASA's Perseverance rover has been exploring Mars' Jezero Crater since 2021, collecting rock samples as part of a mission to search for signs of ancient microbial life."
fake_text = "Scientists at a major university have confirmed that drinking hot lemon water every morning completely cures diabetes within two weeks, according to a new study that has not been reviewed by any medical journal."

print("\n--- Testing Real News Input ---")
res1 = predict(real_text)
print(res1)

print("\n--- Testing Fake News Input ---")
res2 = predict(fake_text)
print(res2)
