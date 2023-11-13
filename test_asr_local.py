# # Use a pipeline as a high-level helper
# from transformers import pipeline

# pipe = pipeline("automatic-speech-recognition", model="openai/whisper-large-v3")
# output = pipe("voice_note_ex.ogg")

from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
import audiofile
import librosa

processor = AutoProcessor.from_pretrained("openai/whisper-large-v3")
model = AutoModelForSpeechSeq2Seq.from_pretrained("openai/whisper-large-v3")
target_sr = processor.feature_extractor.sampling_rate

signal, sampling_rate = audiofile.read("voice_note_ex.ogg")
if sampling_rate != target_sr:
    signal = librosa.resample(signal, orig_sr=sampling_rate, target_sr=target_sr)

inputs = processor(signal, sampling_rate=target_sr, return_tensors="pt")
input_features = inputs.input_features
generated_ids = model.generate(inputs=input_features)
output = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]


print(output)