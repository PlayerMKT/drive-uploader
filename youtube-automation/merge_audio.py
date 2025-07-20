from pydub import AudioSegment
import os

def merge_wav_files(wav_paths, output_path):
    combined = AudioSegment.empty()
    for path in wav_paths:
        audio = AudioSegment.from_wav(path)
        combined += audio
    combined.export(output_path, format="wav")
    print(f"🧩 Áudio combinado salvo em {output_path}")

if __name__ == "__main__":
    audio_paths = [
        "assets/audio/scene_1.wav",
        "assets/audio/scene_2.wav",
        "assets/audio/scene_3.wav",
    ]
    merge_output = "assets/audio/final_audio.wav"
    merge_wav_files(audio_paths, merge_output)
