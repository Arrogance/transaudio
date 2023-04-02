import os
import sys
import tempfile
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence

def transcribe_audio_file(audio_file_path, language="es-ES"):
    recognizer = sr.Recognizer()
    audio = load_audio_file(audio_file_path)

    text = ""
    for segment in split_on_silence(audio, min_silence_len=500, silence_thresh=-40):
        with tempfile.NamedTemporaryFile(delete=False) as fp:
            file_name = fp.name + ".wav"
            segment.export(file_name, format="wav")

        with sr.AudioFile(file_name) as source:
            audio_segment = recognizer.record(source)
            try:
                text += recognizer.recognize_google(audio_segment, language=language) + " "
            except sr.UnknownValueError:
                pass

        os.remove(file_name)

    return text

def load_audio_file(audio_file_path):
    audio_file = AudioSegment.from_file(audio_file_path)
    return audio_file.set_channels(1).set_frame_rate(16000)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <path_to_audio_file>")
        sys.exit()

    audio_file_path = sys.argv[1]
    transcription = transcribe_audio_file(audio_file_path)
    print(transcription)
