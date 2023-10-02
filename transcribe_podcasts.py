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
output_folder = "output_audio/transcripts/ploetzblog"
chunk_folder = "tmp" # temporary chunks to be passed to openai api

for filename in os.listdir(input_folder):
    if filename.endswith(".mp3"):
        print(filename)
        # filename = "PB 23 - Stellschrauben beim Brotbacken.mp3"
        input_path = os.path.join(input_folder, filename)
        split_mp3(input_path, output_dir=chunk_folder)

        ident = os.path.splitext(filename)[0]
        get_transcript_for_dir(chunk_folder, output_folder, ident= ident)

