# 🛡️ VERITAS AI — Fake News Detection System

An end-to-end Deep Learning & Machine Learning Fake News Detection application powered by **Hugging Face DistilBERT**, **PyTorch**, **Scikit-Learn**, and a modern **Flask Web Interface** with rich laser scanning animations, circular SVG confidence meters, and linguistic explainability.

---

## 🌟 Key Features

- **Transformer Architecture**: Pretrained & Fine-Tuned RoBERTa / DistilBERT transformers via Hugging Face API with 12-layer bidirectional self-attention.
- **Hybrid Citation & Verifiability Layer**: Mitigates tone-based false positives by cross-evaluating named checkable sources, institutional attribution (NASA, WHO, Reuters, universities, peer-reviewed journals, official public records), and lexical signals.
- **Deep Linguistic Explainability**:
  - Clickbait & Sensationalism keyword extraction (`#SHOCKING`, `#EXPOSED`, etc.)
  - In-Text interactive credibility heatmaps with character-level token highlighting
  - Emotional tone & sentiment radar (Sensationalist, Journalistic, Opinionated)
  - Uppercase shout ratio & sensational punctuation index
  - Source citation & objective marker count
- **Multi-Modal Verification**: Voice dictation (Speech-to-Text), Client-side Image OCR (`Tesseract.js`), Web URL scraping, and Direct Text analysis.
- **Side-by-Side Model Battle**: Live real-time performance telemetry comparing 12-layer Transformer vs Scikit-Learn TF-IDF baseline.
- **Official Fact-Check Certificates**: Exportable high-resolution PNG / PDF report cards with dynamic verification hashes.
- **Session Analytics**: Interactive Chart.js analytics tracking credibility distributions and keyword trends.

> [!IMPORTANT]
> **Fact-Checking Transparency Notice**:
> Veritas AI evaluates linguistic style, sensationalist cues, and verifiable attribution signals through a hybrid transformer and citation-matching pipeline. Language models judge text framing and verifiable evidence cues, not absolute ground truth. This application serves as an assistive digital intelligence signal to aid readers in fact-checking, not an infallible final verdict.

---

## 📁 Project Structure

```
fack news detection/
├── app.py                          # Root launcher script
├── requirements.txt                # Python dependencies
├── README.md                       # Complete documentation
├── data/                           # (Optional) Kaggle dataset folder
│   ├── Fake.csv
│   └── True.csv
├── model_training/                 # ML & Deep Learning Pipeline
│   ├── preprocess.py               # Text cleaning and Kaggle CSV ingestion
│   ├── train_bert.py               # DistilBERT fine-tuning script (GPU/Colab)
│   ├── train_baseline.py           # Fast TF-IDF + Classifier baseline
│   └── evaluate.py                 # Accuracy, F1, Confusion Matrix evaluation
└── backend/
    ├── app.py                      # Flask REST API & Web Server
    ├── model/
    │   ├── inference.py            # Model loading, predict() & explainability
    │   └── saved_model/            # Saved weights & tokenizer files
    ├── templates/
    │   └── index.html              # Main Glassmorphic UI template
    └── static/
        ├── css/
        │   └── style.css           # Modern CSS3 with Keyframes & Glassmorphism
        └── js/
            └── script.js           # Interactive controller, Gauge & Scanner FX
```

---

## 🚀 Quick Start Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch Web Application
```bash
python app.py
```
Open your browser and navigate to: **`http://127.0.0.1:5000`**

*(On the very first launch, the system automatically bootstraps and compiles the baseline NLP pipeline so you can start testing immediately!)*

---

## 🧠 Training Custom DistilBERT Model

### Dataset
Download the **Kaggle Fake and Real News Dataset** (`Fake.csv` and `True.csv` ~45k articles) and place them in the `data/` directory:
- `data/Fake.csv`
- `data/True.csv`

### Run Fine-Tuning (Google Colab / Local GPU)
```bash
python model_training/train_bert.py --data_dir data --epochs 3 --batch_size 16 --lr 2e-5
```

The script will:
1. Tokenize sequences with `DistilBertTokenizer`.
2. Fine-tune `DistilBertForSequenceClassification` with early stopping.
3. Save the model weights and tokenizer directly into `backend/model/saved_model/`.
4. The Flask web app will automatically detect and prioritize the fine-tuned DistilBERT weights!

### Evaluate Performance
```bash
python model_training/evaluate.py
```
Outputs Accuracy, Precision, Recall, F1-Score, and a complete Confusion Matrix.

---

## 🔌 REST API Endpoints

### 1. Predict Text or URL
`POST /api/predict`
```json
// Request Text
{
  "text": "NASA's James Webb Space Telescope has captured new high-resolution infrared images of a distant star..."
}

// Or Request URL
{
  "url": "https://www.reuters.com/article/example-news"
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "label": "Real",
    "verdict": "Verified Credible",
    "confidence": 94.2,
    "probabilities": {
      "real": 94.2,
      "fake": 5.8
    },
    "status_theme": "real",
    "model_architecture": "DistilBERT (Fine-Tuned)",
    "latency_ms": 38.4,
    "linguistics": {
      "sentiment_tone": "Journalistic & Objective",
      "sensational_words": [],
      "uppercase_ratio": 0.0,
      "exclamation_count": 0,
      "objective_markers": ["according to", "study published"]
    }
  }
}
```

### 2. Fetch Sample Articles
`GET /api/samples`

### 3. History Management
`GET /api/history` — Get recent scans  
`DELETE /api/history` — Clear history

---

## 🛠️ Tech Stack
- **Backend**: Python 3.10+, Flask, Flask-CORS, BeautifulSoup4, Requests
- **Machine Learning & NLP**: PyTorch, Hugging Face Transformers (`distilbert-base-uncased`), Scikit-Learn, Joblib
- **Frontend**: Vanilla HTML5, CSS3 Glassmorphism, JavaScript (ES6+), FontAwesome, Google Fonts Outfit & Plus Jakarta Sans

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](file:///c:/Users/ompat/Desktop/fack%20news%20detection/LICENSE) file for full details.

Copyright (c) 2026 OM Patel.

