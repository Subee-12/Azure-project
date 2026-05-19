import os
import requests
from flask import Flask, render_template

app = Flask(__name__)

API_URL = os.getenv("API_URL", "http://backend:5001")

@app.route("/")
def dashboard():
    metrics = []

    try:
        response = requests.get(API_URL)

        if response.status_code == 200:
            metrics = response.json()

    except Exception as e:
        print("Error connecting to backend:", e)

    return render_template("index.html", metrics=metrics)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)