from pydub import AudioSegment


def overlayAmbient(i):
    audio1 = AudioSegment.from_file(f'music_{i}.wav')
    audio2 = AudioSegment.from_file(f'ambient_{i}.mp3')
    audio2 = audio2.apply_gain(5)

    # Overlay audio2 on top of audio1, starting at the beginning of audio1
    overlayed = audio1.overlay(audio2,loop=True)

    # Export the overlayed audio
    overlayed.export(f"music_overlay_{i}.wav", format="wav")
    return

overlayAmbient(6)