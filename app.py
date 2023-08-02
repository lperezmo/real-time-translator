import io
import openai
from gtts import gTTS
import streamlit as st
from io import BytesIO
from audio_recorder_streamlit import audio_recorder
import streamlit.components.v1 as components
from st_custom_components import st_audiorec

#---------------------------------#
# Set page configuration
#---------------------------------#
st.set_page_config(page_title='Real Time Translation', 
					page_icon='🌎', 
					layout='centered', 
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
	st.caption('Written by LPM')

	# OpenAI API key
	openai.api_key = st.secrets["OPENAI_API_KEY"]

	# Record audio
	audio_bytes = audio_recorder(pause_threshold=40)
	if audio_bytes:
		if len(audio_bytes) > 0 and len(audio_bytes) < 48000000:
			# Translate audio bytes into English
			audio_file = io.BytesIO(audio_bytes)
			st.session_state.original_sound = audio_file
			if audio_file:
				st.markdown("***Original Recording***")
				st.audio(audio_file)
				st.divider()
		elif len(audio_bytes) > 48000000:
			st.warning('Please keep your audio recordings under 10 minutes, thanks!')
			st.stop()
		
	if st.button("Translate recording", type="primary"):
		audio_file.name = "temp_audio_file.wav"
		transcript = openai.Audio.translate("whisper-1", st.session_state.original_sound)
		st.session_state.transcript = transcript
		if len(transcript['text']) > 0: 
			# Convert text to speech
			sound_file = BytesIO()
			tts = gTTS(transcript['text'], lang='en')
			tts.write_to_fp(sound_file)
			st.session_state.sound_file = sound_file
		else:
			st.warning('No text to convert to speech.')

	cols = st.columns(2)
	if 'transcript' in st.session_state:
		with cols[0]:
			st.markdown("***Translation Transcript***")
			st.text_area("Translation transcript", st.session_state.transcript['text'], label_visibility='collapsed')
	if 'sound_file' in st.session_state:
		with cols[1]:
			st.markdown("***Synthesized Translation***")
			st.audio(st.session_state.sound_file)
			
	# Text to speech
	with st.expander("Text to speech"):
		with st.form('text_to_speech'):
			st.subheader('Text to Speech')
			text_to_speech = st.text_area('Enter text to convert to speech')
			submit_button = st.form_submit_button(label='Convert')
			if submit_button and len(text_to_speech) > 0:
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
	#if st.button("Translate recorded audio", type="primary"):
	#	st.experimental_rerun()
	# if check_password():
	main()
