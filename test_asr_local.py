# Use a pipeline as a high-level helper
from transformers import pipeline
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
import audiofile
import librosa
import time
import torch


cuda_available = torch.cuda.is_available()

""" pipeline """
if cuda_available:
    print("CUDA available") 
    pipe = pipeline("automatic-speech-recognition", model="openai/whisper-large-v3", device=0)
else:
    pipe = pipeline("automatic-speech-recognition", model="openai/whisper-large-v3")

target_sr = 16000

start_time = time.time()
signal, sampling_rate = audiofile.read("voice_note_ex.ogg")
if sampling_rate != target_sr:
    signal = librosa.resample(signal, orig_sr=sampling_rate, target_sr=target_sr)
output = pipe(signal, generate_kwargs={"language": "english"})
print("Time taken (pipeline):", time.time() - start_time)

# """ manual way (faster because inputs are cached for second time?) """
# processor = AutoProcessor.from_pretrained("openai/whisper-large-v3", language="en", task="transcribe")
# model = AutoModelForSpeechSeq2Seq.from_pretrained("openai/whisper-large-v3")
# model = model.to("cuda" if cuda_available else "cpu")
# target_sr = processor.feature_extractor.sampling_rate

# start_time = time.time()
# signal, sampling_rate = audiofile.read("voice_note_ex.ogg")
# if sampling_rate != target_sr:
#     signal = librosa.resample(signal, orig_sr=sampling_rate, target_sr=target_sr)

# inputs = processor(signal, sampling_rate=target_sr, return_tensors="pt")
# input_features = inputs.input_features
# input_features = input_features.to("cuda" if cuda_available else "cpu")
# generated_ids = model.generate(input_features=input_features)
# output = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

print(output)
print("Time taken (manual):", time.time() - start_time)
