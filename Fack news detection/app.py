"""
Root entry point to launch the Fake News Detection Flask Application.
Usage: python app.py
"""

import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.app import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("============================================================")
    print("       VERITAS - FAKE NEWS DETECTION ENGINE")
    print(f"       Web Server running at: http://127.0.0.1:{port}")
    print("============================================================")
    app.run(host="0.0.0.0", port=port, debug=False)
