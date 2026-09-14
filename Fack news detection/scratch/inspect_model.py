from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch

MODEL = "jy46604790/Fake-News-Bert-Detect"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

test_samples = [
    ("NASA Real", "NASA's Perseverance rover has been exploring Mars' Jezero Crater since 2021, collecting rock samples as part of a mission to search for signs of ancient microbial life."),
    ("Lemon Cure Fake", "Scientists at a major university have confirmed that drinking hot lemon water every morning completely cures diabetes within two weeks, according to a new study that has not been reviewed by any medical journal."),
    ("Reuters Real", "WASHINGTON (Reuters) - The White House confirmed today that the President signed the international clean energy accord following bipartisan negotiations."),
    ("Conspiracy Fake", "SHOCKING: Secret government microchips found in ordinary grocery store drinking water bottles to control human brainwaves! Elites are trying to silence this!")
]

print("Model config id2label:", model.config.id2label)
print("=" * 60)
for name, text in test_samples:
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=-1)[0].tolist()
    print(f"[{name}]")
    print(f"  LABEL_0 (Fake/Real?): {probs[0]:.4f}, LABEL_1 (Fake/Real?): {probs[1]:.4f}")
    print(f"  Argmax: LABEL_{torch.argmax(outputs.logits, dim=-1).item()}")
    print("-" * 60)
