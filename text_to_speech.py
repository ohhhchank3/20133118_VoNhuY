import io
import os
from threading import Thread
import pygame
from google.cloud import texttospeech_v1
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"GoogleCloudKey_MyServiceAcct.json"
stop_audio_flag = False
immediately_stop_flag = False  # Biến cờ để kiểm tra ngừng ngay lập tức
audio_thread = None
pygame.mixer.init()

def play_audio_thread(sound):
    global stop_audio_flag, immediately_stop_flag
    pygame.mixer.music.load(io.BytesIO(sound))
    pygame.mixer.music.play()
    while not stop_audio_flag and not immediately_stop_flag:
        pygame.time.Clock().tick(10)  # Kiểm soát tốc độ vòng lặp
        if pygame.mixer.music.get_busy() == 0:  # Kiểm tra xem âm thanh đã phát xong chưa
            break  # Dừng nếu nhận được tín hiệu từ Event
    pygame.mixer.music.stop()
    print("Audio playback stopped.")

def play_sound(audio_data):
    global stop_audio_flag, audio_thread, immediately_stop_flag
    audio_thread = Thread(target=play_audio_thread, args=(audio_data,))
    audio_thread.start()
    return audio_thread

def stop_sound():
    global stop_audio_flag, audio_thread, immediately_stop_flag
    stop_audio_flag = True
    immediately_stop_flag = True
    audio_thread.join(timeout=0)

def text_to_speech(text, language_code="vi-VN"):
    client = texttospeech_v1.TextToSpeechClient()
    synthesis_input = texttospeech_v1.SynthesisInput(text=text)
    voice = texttospeech_v1.VoiceSelectionParams(
        language_code=language_code,
        name=f'{language_code}-Wavenet-D',
        ssml_gender=texttospeech_v1.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech_v1.AudioConfig(
        audio_encoding=texttospeech_v1.AudioEncoding.LINEAR16
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    audio_data = response.audio_content
    return audio_data

def play_text_to_speech(text, language_code="vi-VN"):
    global stop_audio_flag, audio_thread, immediately_stop_flag
    stop_audio_flag = False
    immediately_stop_flag = False
    audio_data = text_to_speech(text, language_code)
    audio_thread = play_sound(audio_data)
    return audio_thread

def stop_text_to_speech():
    global stop_audio_flag, audio_thread, immediately_stop_flag
    stop_sound()
    return audio_thread

def stop_stt():
    global stop_audio_flag, immediately_stop_flag
    stop_audio_flag = True  # Dừng âm thanh nếu đang phát
    immediately_stop_flag = True
    stop_text_to_speech()
    return True
