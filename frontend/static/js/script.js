// --- DOM Element Selection ---
// Get references to all the interactive elements from the HTML.
const textInput = document.getElementById('text-input');
const langSelect = document.getElementById('lang-select');
const generateBtn = document.getElementById('generate-btn');
const audioPlayer = document.getElementById('audio-player');
const errorMessage = document.getElementById('error-message');
const loader = generateBtn.querySelector('.loader');
const btnText = generateBtn.querySelector('.btn-text');

// --- Event Listener ---
// Attach a click event listener to the "Generate Voice" button.
generateBtn.addEventListener('click', handleGenerateClick);

// --- Core Function ---
async function handleGenerateClick() {
    // Get the user's text and selected language.
    const text = textInput.value.trim();
    const lang = langSelect.value;

    // --- Input Validation ---
    // If the textarea is empty, show an error and stop.
    if (!text) {
        showError('Please enter some text.');
        return;
    }

    // --- UI State Management ---
    // Show a loading state while the audio is being generated.
    setLoading(true);
    clearError();
    hideAudioPlayer();

    try {
        // --- API Call ---
        // Make a POST request to the backend API endpoint.
        const response = await fetch('/api/tts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            // Send the text and language in the request body.
            body: JSON.stringify({ text, lang }),
        });

        // --- Response Handling ---
        // If the response is not successful (e.g., 400 or 500 error), handle it.
        if (!response.ok) {
            const errorData = await response.json();
            // Display the error message from the server.
            throw new Error(errorData.error || 'An unknown error occurred.');
        }

        // If the request is successful, get the audio data as a blob.
        const audioBlob = await response.blob();
        
        // Create a URL for the blob object.
        const audioUrl = URL.createObjectURL(audioBlob);
        
        // Set the audio player's source to the new URL and make it visible.
        audioPlayer.src = audioUrl;
        showAudioPlayer();

    } catch (error) {
        // --- Error Handling ---
        // Display any errors that occurred during the fetch or response processing.
        console.error('Error:', error);
        showError(error.message);
    } finally {
        // --- UI State Cleanup ---
        // Whether the request succeeded or failed, always hide the loading indicator.
        setLoading(false);
    }
}

// --- UI Helper Functions ---

function setLoading(isLoading) {
    // Disable the button to prevent multiple clicks while loading.
    generateBtn.disabled = isLoading;
    if (isLoading) {
        // Show the loader and hide the button text.
        loader.style.display = 'block';
        btnText.style.display = 'none';
        generateBtn.classList.add('loading');
    } else {
        // Hide the loader and show the button text.
        loader.style.display = 'none';
        btnText.style.display = 'block';
        generateBtn.classList.remove('loading');
    }
}

function showError(message) {
    // Display an error message to the user.
    errorMessage.textContent = message;
}

function clearError() {
    // Clear any previous error messages.
    errorMessage.textContent = '';
}

function showAudioPlayer() {
    // Make the audio player visible.
    audioPlayer.style.display = 'block';
}

function hideAudioPlayer() {
    // Hide the audio player.
    audioPlayer.style.display = 'none';
    // Also clear the src to free up memory.
    audioPlayer.src = '';
}
