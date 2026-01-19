# Text-to-Speech Web Application
https://project-text-to-speech-5.onrender.com/

This is a complete, end-to-end runnable Text-to-Speech (TTS) project that converts text into natural-sounding speech using Python's gTTS (Google Text-to-Speech) library and a modern web interface.

## Features

- **Clean & Modern UI**: A responsive and user-friendly interface built with HTML, CSS, and JavaScript.
- **Backend Powered by Flask**: A robust Python backend to handle text processing and speech generation.
- **gTTS Integration**: Leverages Google's powerful text-to-speech engine.
- **Multilingual Support**: Easily convert text in various languages (English, Hindi, Marathi, Spanish, etc.).
- **Dynamic Audio Generation**: Generates MP3 audio on the fly without saving files on the server.
- **Automatic Dependency Installation**: The application automatically installs required Python libraries on first run.
- **Loading & Error States**: The UI provides clear feedback to the user during processing and in case of errors.

## Folder Structure

The project is organized into a clean and scalable structure:

```
project2/
│
├── backend/
│   │── app.py             # Main Flask application, API logic, and dependency handling.
│   └── requirements.txt   # Python dependencies (Flask, gTTS).
│
├── frontend/
│   │── templates/
│   │   └── index.html     # The main HTML file for the user interface.
│   │
│   └── static/
│       ├── css/
│       │   └── style.css  # CSS for styling the UI.
│       └── js/
│           └── script.js  # JavaScript for frontend logic and API calls.
│
└── README.md              # This documentation file.
```

## How to Run the Project

Follow these simple steps to get the application running on your local machine.

### Step 1: Make sure you have Python installed

This project requires Python. You can download it from [python.org](https://www.python.org/downloads/).

### Step 2: Navigate to the Project Directory

Open your command prompt or terminal and navigate into the `backend` directory inside the project folder:

```bash
cd C:\Users\91789\Desktop\project2\backend
```

### Step 3: Run the Application

Execute the main Python script. The application will handle the rest.

```bash
python app.py
```

### What to Expect

1.  When you run the command, the script will first **check for and install the required Python libraries** (`Flask` and `gTTS`). You will see output in your terminal related to this process.
2.  Once the dependencies are installed, the Flask web server will start.
3.  Your default **web browser will automatically open** a new tab to `http://127.0.0.1:5000/`.
4.  The Text-to-Speech web interface will be displayed, ready for you to use.

## Expected Output

- **Terminal**: You will see logs indicating that dependencies are being installed, followed by the Flask server starting up.
- **Browser**: A web page with a centered card where you can:
    1.  Enter text into the textarea.
    2.  Select a language from the dropdown menu.
    3.  Click the "Generate Voice" button.
    4.  After a brief loading animation, an audio player will appear, allowing you to play the generated speech.

Enjoy your new Text-to-Speech application!

```
