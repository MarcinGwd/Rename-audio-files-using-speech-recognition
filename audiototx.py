import os
import speech_recognition as sr
from pydub import AudioSegment

def recognize_audio_file(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_sphinx(audio_data)
            return text
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))

def convert_to_wav(file_path):
    audio = AudioSegment.from_mp3(file_path)
    wav_file_path = os.path.splitext(file_path)[0] + ".wav"
    audio.export(wav_file_path, format="wav")
    return wav_file_path

def get_unique_filename(directory, base_filename, extension):
    counter = 1
    unique_filename = base_filename + extension
    while os.path.exists(os.path.join(directory, unique_filename)):
        unique_filename = f"{base_filename}_{counter}{extension}"
        counter += 1
    return unique_filename

def truncate_filename(filename, max_words):
    words = filename.split()
    return " ".join(words[:max_words])

def rename_audio_files(directory, max_filename_words):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if filename.endswith(".mp3"):
            file_path = convert_to_wav(file_path)
            filename = os.path.basename(file_path)

        if filename.endswith(".wav"):
            recognized_text = recognize_audio_file(file_path)
            if recognized_text:
                base_filename = truncate_filename(recognized_text.strip(), max_filename_words)
                unique_filename = get_unique_filename(directory, base_filename, ".wav")
                new_file_path = os.path.join(directory, unique_filename)
                os.rename(file_path, new_file_path)
                print(f"Renamed '{file_path}' to '{new_file_path}'")

if __name__ == "__main__":
    directory = "audio/"
    max_filename_words = 5  # Adjust this value to set the maximum filename word count
    rename_audio_files(directory, max_filename_words)