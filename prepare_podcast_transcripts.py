import time
from dotenv import load_dotenv
load_dotenv()
import os
import json
import openai

import tiktoken

from  src.audio_functions import *


# input_folder = "output_audio/transcripts/ploetzblog"
# rag_data = "output_audio/rag_data/ploetzblog"
input_folder = "output_audio/transcripts/wingfoil_podcast"
rag_data = "output_audio/rag_data/wingfoil_podcast"


def num_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    num_tokens = len(encoding.encode(string))
    return num_tokens
num_tokens_from_string("tiktoken is great!")

def translate_text(text, source_language, target_language):
    prompt = f"Translate the following text from '{source_language}' to '{target_language}': {text}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that translates text."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=3000,
        n=1,
        stop=None,
        temperature=0.01,
    )

    translation = response.choices[0].message.content.strip()
    return translation

import spacy
from spacy.language import Language
from spacy_langdetect import LanguageDetector
spacy.prefer_gpu()

@Language.factory("language_detector")
def create_language_detector(nlp, name):
    return LanguageDetector(language_detection_function=None)
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe('language_detector')
# text = 'This is an english text.'
# text = "Er lebt mit seinen Eltern und seiner Schwester in Berlin."
# doc = nlp(text)
# # document level language detection. Think of it like average language of the document!
# print(doc._.language)
# # sentence level language detection
# for sent in doc.sents:
#    print(sent, sent._.language)


from deep_translator import (GoogleTranslator,
                             ChatGptTranslator,
                             DeeplTranslator)

# text = "Er lebt mit seinen Eltern und seiner Schwester in Berlin."
# translated = GoogleTranslator(source='auto', target='de').translate(text=text)
# print(translated)
# translated = ChatGptTranslator(source='auto', target='de', api_key=os.getenv("OPENAI_API_KEY")).translate(text=text)
# print(translated)
# translated = DeeplTranslator(source='auto', target='de').translate(text=text)
# print(translated)

# if not os.path.exists(rag_data):
#     os.makedirs(rag_data)
# response = input("Do you really want to empty " + rag_data + "? (yes/no) ").lower()
# if response == "yes":
#     empty_folder(rag_data)

def split_text(text, chunk_size=4900, overlap=100):
    """
    Split the text into overlapping chunks.

    Parameters:
    text (str): The text to be split
    chunk_size (int): The maximum size of each chunk
    overlap (int): The number of overlapping characters between each chunk
    
    Returns:
    list: A list of strings representing each chunk
    """
    
    chunks = []
    text_length = len(text)
    
    for i in range(0, text_length, chunk_size-overlap):
        # If it's the last chunk and it's smaller than the overlap
        if i + chunk_size > text_length:
            chunks.append(text[i:])
        else:
            chunks.append(text[i:i+chunk_size])
            
    return chunks



# Example usage:
# text = "This is a simple text to be split into overlapping chunks."
# split_point = int(len(text)/2)
# overlap = 12
# chunk1, chunk2 = split_text(text, split_point, overlap)

# print("First Chunk:", chunk1)
# print("Second Chunk:", chunk2)


for filename in os.listdir(input_folder):
    if filename.endswith(".json"):
        path_to_file = os.path.join(input_folder, filename)
        with open(path_to_file, 'r') as f:
            pod_dict = json.load(f)

        text = pod_dict["text"]
        doc = nlp(text)
        print(doc._.language)
        if doc._.language["language"] == "en":
            # text = translate_text(text, "english", "german")
            chunks = split_text(text, chunk_size=4900, overlap=15)
            text = ""
            for i, chunk in enumerate(chunks):
                print(f"Chunk {i+1}:")
                text += "\n" + GoogleTranslator(source='auto', target='de').translate(text=chunk)
            print(filename)
            # print(num_tokens_from_string(text))
            # break
        fileout = os.path.join(rag_data, pod_dict["ident"] + '_' + pod_dict["chunk_ident"] + '.txt' )
        fileout = fileout.replace(" ","_")
        fileout = fileout.replace("_-_","_")
        print(fileout)
        with open(fileout, 'w', encoding='utf-8') as file:
            file.write("Title: " + pod_dict["ident"])
            file.write("Content: " + text)
