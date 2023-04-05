# Real-Time Translator

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://translator.streamlitapp.com/)
![GitHub license](https://img.shields.io/github/license/lperezmo/real-time-translator)
![Python version](https://img.shields.io/badge/python-3.8-blue)
![GitHub last commit](https://img.shields.io/github/last-commit/lperezmo/real-time-translator)
![GitHub issues](https://img.shields.io/github/issues/lperezmo/real-time-translator)
![GitHub stars](https://img.shields.io/github/stars/lperezmo/real-time-translator)

A web app to translate speech in real time using the Whisper API for transcribing and translating recorded audio, and Google Text-to-Speech (gTTS) to play out the translation.

## Features


- Transcribe speech from microphone or audio file

- Translate speech or text into English from any language 

- Display translation results on screen as text

- Translation synthesized as speech by Google text-to-speech module (gTTS).


## Demo


You can try out the app here: https://translator.streamlit.app/


Alternatively, you can run the app locally by following the installation instructions below


## Installation


To run the app locally, you need to have Python 3.7+ and pip installed.


1. Clone this repository: `git clone https://github.com/lperezmo/real-time-translator.git`

2. Navigate to the project directory: `cd real-time-translator`

3. Install the required packages: `pip install -r requirements.txt`

4.  Run the app: `streamlit run app.py`

5.  Open your browser and go to http://localhost:8501


## Usage


To use the app, follow these steps:


1. Click on the microphone and record audio while it's red.

2. If audio is not showing after recording click “rerun app” button at the top of the app.


## License


This project is licensed under the GPL-3.0 License - see [LICENSE.md](LICENSE.md) for details.



