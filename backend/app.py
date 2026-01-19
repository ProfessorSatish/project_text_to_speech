from gtts import gTTS

import sys
import subprocess
import os
import io
import webbrowser
from threading import Timer
from flask import Flask, render_template, request, send_file, jsonify

# --- Configuration ---
# Define the absolute path for the frontend directory.
# This is crucial for Flask to locate the template and static files.
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))

# Initialize the Flask app, specifying the template and static folder paths.
# This setup allows us to have a clean separation between backend and frontend code.
app = Flask(
    __name__,
    template_folder=os.path.join(FRONTEND_DIR, 'templates'),
    static_folder=os.path.join(FRONTEND_DIR, 'static')
)

# --- Dependency Management ---
def install_dependencies():
    """
    Reads the requirements.txt file and installs the necessary packages using pip.
    This makes the project setup automatic and user-friendly.
    """
    print("Checking and installing dependencies...")
    try:
        # Construct the absolute path to requirements.txt
        requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
        # Use subprocess to run pip install.
        # sys.executable ensures we use the pip associated with the current Python interpreter.
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
        print("Dependencies are all set.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        # Exit the application if dependencies can't be installed, as it cannot run otherwise.
        sys.exit(1)
    except FileNotFoundError:
        print("Error: requirements.txt not found. Please make sure the file exists.")
        sys.exit(1)

# --- Core Application Logic ---
def initialize_app():
    """
    Installs dependencies and then imports the gTTS library.
    This function is called before the first request to ensure the environment is ready.
    """
    install_dependencies()
    # Import gTTS only after ensuring it's installed.
    # This avoids an ImportError when the script is run for the first time.
    global gTTS
    from gtts import gTTS
    print("gTTS imported successfully.")

# --- Routes ---
@app.route('/')
def index():
    """
    Serves the main HTML page of the application.
    Flask will look for 'index.html' in the specified 'template_folder'.
    """
    return render_template('index.html')

@app.route('/api/tts', methods=['POST'])
def text_to_speech():
    """
    API endpoint to convert text to speech.
    It receives JSON data with 'text' and 'lang', generates an MP3 file,
    and sends it back to the frontend.
    """
    try:
        # Get data from the POST request
        data = request.get_json()
        text = data.get('text')
        lang = data.get('lang', 'en') # Default to English if no language is provided

        # Validate input
        if not text:
            return jsonify({"error": "Text input is required."}), 400

        # Generate speech using gTTS
        # The 'slow=False' argument makes the speech faster.
        tts = gTTS(text=text, lang=lang, slow=False)
        
        # Use an in-memory byte stream to hold the audio data, avoiding temporary files.
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0) # Rewind the stream to the beginning

        # Send the audio file back to the client
        return send_file(
            mp3_fp,
            mimetype='audio/mpeg',
            as_attachment=True,
            download_name='speech.mp3'
        )
    except Exception as e:
        # Handle potential errors, such as unsupported languages or network issues with gTTS.
        print(f"An error occurred: {e}")
        return jsonify({"error": "Failed to generate audio. Please check the language code or try again."}), 500

# --- Auto-run and Browser Opening ---
def open_browser():
    """
    Opens the default web browser to the application's URL.
    """
    webbrowser.open_new("http://127.0.0.1:5000/")

# --- Main Execution ---
if __name__ == '__main__':
    # Ensure dependencies are installed before starting the server.
    initialize_app()
    
    # Use a timer to open the browser shortly after the app starts.
    # This gives the server a moment to get ready.
    Timer(1, open_browser).start()
    
    # Run the Flask application.
    # 'debug=False' is recommended for this setup to avoid running initialization twice.
    app.run(port=5000, debug=False)
