import sys
import subprocess
import os
import io
import webbrowser
from threading import Timer
from flask import Flask, render_template, request, send_file, jsonify

# --- Configuration ---
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))

app = Flask(
    __name__,
    template_folder=os.path.join(FRONTEND_DIR, 'templates'),
    static_folder=os.path.join(FRONTEND_DIR, 'static')
)

# --- Dependency Management ---
def install_dependencies():
    try:
        requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
        return True
    except Exception as e:
        print("Dependency install error:", e)
        sys.exit(1)

# --- Initialize ---
def initialize_app():
    install_dependencies()
    global gTTS
    from gtts import gTTS

# --- Routes ---

# ✅ MERGED ROUTE (2nd code ka logic yahin add kiya)
@app.route("/")
def home():
    return "Text to Speech App is Running"

@app.route("/ui")
def index():
    return render_template("index.html")

@app.route("/api/tts", methods=["POST"])
def text_to_speech():
    try:
        data = request.get_json()
        text = data.get("text")
        lang = data.get("lang", "en")

        if not text:
            return jsonify({"error": "Text is required"}), 400

        tts = gTTS(text=text, lang=lang, slow=False)
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)

        return send_file(
            mp3_fp,
            mimetype="audio/mpeg",
            as_attachment=True,
            download_name="speech.mp3"
        )

    except Exception as e:
        print("TTS Error:", e)
        return jsonify({"error": "Audio generation failed"}), 500

# --- Browser Auto Open (Local only) ---
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

# --- Main ---
if __name__ == "__main__":
    initialize_app()
    Timer(1, open_browser).start()
    app.run(host="0.0.0.0", port=5000, debug=False)
