import json
from typing import List
import requests as r
import base64
import mimetypes
import os

ENDPOINT_URL="https://ghfayw3exx0aa00r.eu-west-1.aws.endpoints.huggingface.cloud"
HF_TOKEN="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"

def predict(path_to_audio:str=None):
    # read audio file
    with open(path_to_audio, "rb") as i:
      input = i.read()
    # get mimetype
    content_type= mimetypes.guess_type(path_to_audio)[0]

    headers= {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": content_type,
    }
    # data = json.dumps({"inputs": input, "parameters": {"language":"<|de|>"}})
    parameter_payload = {
        "parameters" : {
            "generate_kwargs": {
               "task":"transcribe"
            }
        }
    }

    response = r.post(ENDPOINT_URL, headers=headers, data=input, json= parameter_payload)
    return response.json()


# # ------ with InferenceClient -----------
# from huggingface_hub import InferenceClient
# # Streaming Client
# client = InferenceClient(ENDPOINT_URL, token=HF_TOKEN)
# # generation parameter
# gen_kwargs = dict(
#     chunk_length_s=25
#     # task="transcribe"
# )
# # pred = client.text_generation(prompt, stream=True, details=True, **gen_kwargs)


input_folder = "downloaded_podcasts/ploetzblog_sel"
filename = "PB 23 - Stellschrauben beim Brotbacken.mp3"
input_path = os.path.join(input_folder, filename)

input_path = "output_first_minute.mp3"

# prediction = client.automatic_speech_recognition(input_path)
prediction = predict(path_to_audio=input_path)

print(prediction)
