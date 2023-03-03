import streamlit as st
import pandas as pd
import numpy as np
from gtts import gTTS
import openai
from audio_recorder_streamlit import audio_recorder
from io import BytesIO
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
#---------------------------------#
# Set page configuration
#---------------------------------#
st.set_page_config(page_title='Real Time Translation', 
					page_icon='🌎', 
					layout='wide', 
					initial_sidebar_state='auto')
hide_streamlit_style = """
			<style>
			footer {visibility: hidden;}
			</style>
			"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

#---------------------------------#
# Main
#---------------------------------#
def main():
	st.header('Real Time Translation')

	# OpenAI API key
	openai.api_key = st.secrets["OPENAI_API_KEY"]

	from audio_recorder_streamlit import audio_recorder

	audio_bytes = audio_recorder()
	if audio_bytes:
		st.audio(audio_bytes, format="audio/wav")

		# To save audio to a file:
		wav_file = open("temp.mp3", "wb")
		wav_file.write(audio_bytes.tobytes())


	# Form for real time translation
	with st.form('input_form'):
		st.subheader('Real Time Speech Translation')

		# Submit button
		submit_button = st.form_submit_button(label='Translate')
		if submit_button:
			# Translate audio bytes into English
			audio_file= open("temp.mp3", "rb")
			try:
				transcript = openai.Audio.translate("whisper-1", audio_file)
				st.success('Translation successful!')
				st.write(transcript)
				# Convert text to speech
				sound_file = BytesIO()
				tts = gTTS(transcript, lang='en')
				tts.write_to_fp(sound_file)
				st.audio(sound_file)
			except:
				st.warning('Translation failed! Please try again.')
				transcript = "Sorry, I didn't catch that. Please try again."

	# Just play text to speech
	with st.form('text_to_speech'):
		st.subheader('Text to Speech')
		text_to_speech = st.text_area('Enter text to convert to speech')
		submit_button = st.form_submit_button(label='Convert')
		if submit_button:
			# Convert text to speech
			sound_file = BytesIO()
			tts = gTTS(text_to_speech, lang='en')
			tts.write_to_fp(sound_file)
			st.audio(sound_file)

def check_password():
	"""
	A function that return True if the password is correct, False otherwise.
	"""

	def password_entered():
		"""
		Checks whether a password entered by the user is correct.
		"""
		if st.session_state["password"] == st.secrets["user_pass"]:
			st.session_state["password_correct"] = True
			del st.session_state["password"]  # don't store password
		else:
			st.session_state["password_correct"] = False

	if "password_correct" not in st.session_state:
		# First run, show input for password.
		st.text_input(
			"Password", type="password", on_change=password_entered, key="password"
		)
		return False
	
	elif not st.session_state["password_correct"]:
		# Password not correct, show input + error.
		st.text_input(
			"Password", type="password", on_change=password_entered, key="password"
		)
		st.error("Password incorrect")
		return False
	else:
		# Password correct.
		return True
	
#---------------------------------#
# Run the main function
#---------------------------------#
if __name__ == '__main__':
	# if check_password():
		main()