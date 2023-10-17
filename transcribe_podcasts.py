from transformers import pipeline
from datasets import load_dataset
from dotenv import load_dotenv
load_dotenv()
import os
# # --- cut parts of a file
from  src.audio_functions import *

# input_folder = "downloaded_podcasts/wingfoil_experience_selected"
# output_folder = "output_audio/transcripts/wingfoil_podcast"
input_folder = "downloaded_podcasts/testfolder"
output_folder = "output_audio/transcripts/testfolder"
chunk_folder = "tmp" # temporary chunks to be passed to openai api

# TODO optimizie transcription based on this: https://github.com/openai/openai-cookbook/blob/main/examples/Whisper_prompting_guide.ipynb

response = input("Do you really want to empty " + output_folder + "? (yes/no) ").lower()
if response == "yes":
    empty_folder(output_folder)

# for filename in os.listdir(input_folder):
#     if filename.endswith(".mp3"):
#         print(filename)
#         # filename = "PB 23 - Stellschrauben beim Brotbacken.mp3"
#         input_path = os.path.join(input_folder, filename)
#         split_mp3(input_path, output_dir=chunk_folder)

#         ident = os.path.splitext(filename)[0]
#         get_transcript_for_dir(chunk_folder, output_folder, podcast_ident=ident)

asyncio.run(get_transcript_for_dir_async(input_folder, output_folder, podcast_ident="test"))

