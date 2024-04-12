import torchaudio
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write

model = MusicGen.get_pretrained('facebook/musicgen-melody')
model.set_generation_params(duration=8)  # generate 8 seconds.

descriptions = ['Cozy lo-fi hip-hop with a touch of rain sound and soft beats to accompany your indoor activities']

melody, sr = torchaudio.load('humming-song.mp3')
# generates using the melody from the given audio and the provided descriptions.
wav = model.generate_with_chroma(descriptions, melody[None], sr)

audio_write('humming-song', wav[0].cpu(), model.sample_rate, strategy="loudness", loudness_compressor=True)