from transformers import pipeline

models_to_test = [
    "jy46604790/Fake-News-Bert-Detect",
    "mrm8488/bert-tiny-finetuned-fake-news-detection",
    "hamzab/roberta-fake-news-classification",
    "vikram71198/distilroberta-base-finetuned-fake-news-detection"
]

real_text = "NASA's Perseverance rover has been exploring Mars' Jezero Crater since 2021, collecting rock samples as part of a mission to search for signs of ancient microbial life."
fake_text = "Scientists at a major university have confirmed that drinking hot lemon water every morning completely cures diabetes within two weeks, according to a new study that has not been reviewed by any medical journal."

for m in models_to_test:
    try:
        print(f"\nTesting {m}...")
        clf = pipeline("text-classification", model=m, tokenizer=m, truncation=True, max_length=512)
        r1 = clf(real_text)[0]
        r2 = clf(fake_text)[0]
        print(f"  REAL: {r1}")
        print(f"  FAKE: {r2}")
    except Exception as e:
        print(f"  Error on {m}: {e}")
