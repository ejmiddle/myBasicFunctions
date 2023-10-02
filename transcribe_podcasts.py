import torch
from transformers import pipeline
from datasets import load_dataset
import whisper
import time
import openai
from dotenv import load_dotenv
load_dotenv()
import os
import json
# # --- cut parts of a file
from pydub import AudioSegment
from  src.audio_functions import *

input_folder = "downloaded_podcasts/ploetzblog_sel"
output_folder = "transcripts/ploetzblog"
chunk_folder = "output_chunks"

for filename in os.listdir(input_folder):
    if filename.endswith(".mp3"):
        print(filename)
        # filename = "PB 23 - Stellschrauben beim Brotbacken.mp3"
        input_path = os.path.join(input_folder, filename)
        split_mp3(input_path, output_dir=chunk_folder)

        ident = os.path.splitext(filename)[0]
        get_transcript_for_dir(chunk_folder, output_folder, ident= ident)

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------



# sample_file = "test_english.mp3"
sample_file = "test_lang.mp3"
output_mp3 = "output_first_minute.mp3"  # Replace with desired output MP3 file
# extract_first_n_sec(sample_file, output_mp3, start_sec = 200, n_sec = 40)

# audio = AudioSegment.from_mp3(sample_file)
# audio.export("output_file.wav", format="wav")


# sample_file = "output_first_minute.mp3"
# sample_file = "output_file.wav"
sample_file = "dfunk_test_5min.mp3"
sample_file = "test_lang.mp3"

# sample_file = "https://huggingface.co/datasets/Narsil/asr_dummy/resolve/main/mlk.flac"

# start_time = time.time()

# # device = "cuda:0" if torch.cuda.is_available() else "cpu"
# device = "mps"
# pipe = pipeline(
#   "automatic-speech-recognition",
#   model="openai/whisper-large-v2",
# #   model="openai/whisper-large",
#   chunk_length_s=25,
# #   stride_length_s=4,
#   return_timestamps=False,
#   generate_kwargs = {"task":"transcribe"}, #, "language":"<|de|>"
# #   batch_size=2,     
#   device=device,
#   use_fast=True
# )
# end_time = time.time()
# elapsed_time = end_time - start_time
# print("Elapsed time loading:", elapsed_time, "seconds")


# start_time = time.time()
# # # prediction = pipe(sample_file, batch_size=8)["text"]
# # # prediction = pipe(sample_file, batch_size=8, return_timestamps=True) # we can also return timestamps for the predictions
# # transcript = pipe( sample_file, generate_kwargs = {"task":"transcribe", "language":"<|de|>"})
# # transcript = pipe( sample_file, generate_kwargs = {"language":"<|de|>"})
# transcript = pipe(sample_file)
# print(transcript["text"])
# end_time = time.time()
# elapsed_time = end_time - start_time
# print("Elapsed time:", elapsed_time, "seconds")
# print("Elapsed time:", elapsed_time / 60, "minutes")

# filename = os.path.join("transcript_a.json")
# with open(filename, 'w') as f:
#     json.dump(transcript, f)
# print(f"Dictionary saved to {filename}")


start_time = time.time()
audio_file= open(sample_file, "rb")
transcript = openai.Audio.transcribe("whisper-1", audio_file, api_key=os.getenv("OPENAI_API_KEY"))
print(transcript["text"])
end_time = time.time()
elapsed_time = end_time - start_time
print("Elapsed time:", elapsed_time, "seconds")
print("Elapsed time:", elapsed_time / 60, "minutes")

filename = os.path.join("transcript_b.json")
with open(filename, 'w') as f:
    json.dump(transcript, f)
print(f"Dictionary saved to {filename}")




