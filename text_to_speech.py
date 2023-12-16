import io
import os

from google.cloud import texttospeech_v1
from pydub import AudioSegment
from pydub.playback import play

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"GoogleCloudKey_MyServiceAcct.json"

def text_to_speech_and_play(text, language_code="vi-VN"):
    # Instantiates a client
    client = texttospeech_v1.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech_v1.SynthesisInput(text=text)

    voice = texttospeech_v1.VoiceSelectionParams(
        language_code=language_code,
        name=f'{language_code}-Wavenet-D',
        ssml_gender=texttospeech_v1.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech_v1.AudioConfig(
        audio_encoding=texttospeech_v1.AudioEncoding.LINEAR16
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    audio_data = response.audio_content

    # Play the audio
    sound = AudioSegment.from_file(io.BytesIO(audio_data), format="wav")
    play(sound)


    print("File temp.wav deleted.")


