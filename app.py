from flask import Flask, render_template, request, send_file, jsonify
from gtts import gTTS
import os
import hashlib

app = Flask(__name__)
CACHE_DIR = "cache_audio"
os.makedirs(CACHE_DIR, exist_ok=True)

def cache_filename(text, voice):
    key = f"{text}-{voice}"
    return hashlib.md5(key.encode('utf-8')).hexdigest() + ".mp3"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tts", methods=["POST"])
def tts():
    data = request.get_json()
    text = data.get("text", "")
    voice = data.get("voice", "male")

    if not text.strip():
        return jsonify({"error": "empty text"}), 400

    filename = cache_filename(text, voice)
    filepath = os.path.join(CACHE_DIR, filename)

    if os.path.exists(filepath):
        return send_file(filepath, mimetype="audio/mpeg")

    # استخدام نطاق مختلف لكل صوت لتغيير النغمة
    tld = "com.eg" if voice == "male" else "com.sa"

    tts = gTTS(text=text, lang="ar", slow=False, tld=tld)
    tts.save(filepath)
    return send_file(filepath, mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
