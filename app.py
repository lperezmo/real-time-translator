import io
import openai
from gtts import gTTS
import streamlit as st
from io import BytesIO
from audio_recorder_streamlit import audio_recorder

# Set page configuration
st.set_page_config(
    page_title='Real Time Translation',
    page_icon='🌎',
    layout='centered',
    initial_sidebar_state='auto'
)

# Hide Streamlit footer
hide_streamlit_style = """
<style>
    footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def main():
    st.header('Real Time Translation')
    st.caption('Written by LPM')

    # Set OpenAI API key
    openai.api_key = st.secrets["OPENAI_API_KEY"]

    audio_bytes = audio_recorder(pause_threshold=40)
    if audio_bytes:
        # Check if audio is of sufficient length
        if len(audio_bytes) > 8000:
            st.success('Audio captured correctly')
        else:
            st.warning('Audio captured incorrectly, please try again.')
        st.audio(audio_bytes, format="audio/wav")
        st.session_state.audio_bytes = audio_bytes

    # Form for real-time translation
    with st.form('input_form'):
        submit_button = st.form_submit_button(label='Translate', type='primary')
        if submit_button and 'audio_bytes' in st.session_state and len(st.session_state.audio_bytes) > 0:
            # Translate audio bytes into English
            audio_file = io.BytesIO(st.session_state.audio_bytes)
            audio_file.name = "temp_audio_file.wav"
            transcript = openai.Audio.translate("whisper-1", audio_file)
            st.markdown("***Translation Transcript***")
            st.text_area('transcription', transcript['text'], label_visibility='collapsed')
            if transcript['text']:
                # Convert text to speech
                sound_file = BytesIO()
                tts = gTTS(transcript['text'], lang='id')
                tts.write_to_fp(sound_file)
                st.markdown("***Synthesized Speech Translation***")
                st.audio(sound_file)
            else:
                st.warning('No text to convert to speech.')
        else:
            st.warning('No audio recorded, please ensure your audio was recorded correctly.')

    # Text to speech section
    with st.expander("Text to speech"):
        with st.form('text_to_speech'):
            text_to_speech = st.text_area('Enter text to convert to speech')
            submit_button = st.form_submit_button(label='Convert')
            if submit_button and text_to_speech:
                # Convert text to speech
                sound_file = BytesIO()
                tts = gTTS(text_to_speech, lang='id')
                tts.write_to_fp(sound_file)
                st.audio(sound_file)


if __name__ == '__main__':
    main()
