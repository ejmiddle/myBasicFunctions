import time
from dotenv import load_dotenv
load_dotenv()
import os
import json
from  src.audio_functions import *

input_folder = "output_audio/transcripts/ploetzblog"
rag_data = "output_audio/rag_data/ploetzblog"


if not os.path.exists(rag_data):
    os.makedirs(rag_data)
empty_folder(rag_data)

for filename in os.listdir(input_folder):
    if filename.endswith(".json"):
        path_to_file = os.path.join(input_folder, filename)
        with open(path_to_file, 'r') as f:
            pod_dict = json.load(f)
        # print(pod_dict)
        fileout = os.path.join(rag_data, pod_dict["ident"] + '_' + pod_dict["chunk_ident"] + '.txt' )
        fileout = fileout.replace(" ","_")
        fileout = fileout.replace("_-_","_")
        print(fileout)
        with open(fileout, 'w', encoding='utf-8') as file:
            file.write("Title: " + pod_dict["ident"])
            file.write("Content: " + pod_dict["text"])
