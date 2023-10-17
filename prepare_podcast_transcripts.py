from dotenv import load_dotenv
load_dotenv()
import os
import json
from deep_translator import (GoogleTranslator,
                             ChatGptTranslator,
                             DeeplTranslator)
import spacy
from spacy.language import Language
from spacy_langdetect import LanguageDetector

from  src.audio_functions import *
from  src.text_manip_functions import *

# input_folder = "output_audio/transcripts/ploetzblog"
# rag_data = "output_audio/rag_data/ploetzblog"
# input_folder = "output_audio/transcripts/wingfoil_podcast"
# rag_data = "output_audio/rag_data/wingfoil_podcast"
# input_folder = "output_audio/transcripts/current_selection"
# rag_data = "output_audio/rag_data/critical_discussion"

input_folder = "output_audio/transcripts/tim_wendelboe"
rag_data = "output_audio/rag_data/tim_wendelboe"

TRANSLATE_EN = False

# # pdm run python -m spacy download en_core_web_sm
# # Spacy for detection
spacy.prefer_gpu()
@Language.factory("language_detector")
def create_language_detector(nlp, name):
    return LanguageDetector(language_detection_function=None)
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe('language_detector')
# text = "Er lebt mit seinen Eltern und seiner Schwester in Berlin."
# doc = nlp(text)
# # document level language detection. Think of it like average language of the document!
# print(doc._.language)
# # sentence level language detection
# for sent in doc.sents:
#    print(sent, sent._.language)

# # deep-translate for translation

# text = "Er lebt mit seinen Eltern und seiner Schwester in Berlin."
# translated = GoogleTranslator(source='auto', target='de').translate(text=text)
# print(translated)
# translated = ChatGptTranslator(source='auto', target='de', api_key=os.getenv("OPENAI_API_KEY")).translate(text=text)
# print(translated)
# translated = DeeplTranslator(source='auto', target='de').translate(text=text)
# print(translated)

if not os.path.exists(rag_data):
    os.makedirs(rag_data)
response = input("Do you really want to empty " + rag_data + "? (yes/no) ").lower()
if response == "yes":
    empty_folder(rag_data)


for filename in os.listdir(input_folder):
    if filename.endswith(".json"):
        path_to_file = os.path.join(input_folder, filename)
        with open(path_to_file, 'r') as f:
            pod_dict = json.load(f)

        text = pod_dict["text"]
        doc = nlp(text)
        if TRANSLATE_EN:
            print(doc._.language)
            if doc._.language["language"] == "en":
                # text = translate_text(text, "english", "german")
                chunks = split_text(text, chunk_size=4900, overlap=15)
                text = ""
                for i, chunk in enumerate(chunks):
                    print(f"chunk {i+1}:")
                    text += "\n" + GoogleTranslator(source='auto', target='de').translate(text=chunk)
                print(filename)
                # print(num_tokens_from_string(text))
                # break
        # print(pod_dict)
        fileout = os.path.join(rag_data, pod_dict["podcast_ident"] + '_' + pod_dict["seg_ident"] + '.txt' )
        fileout = fileout.replace(" ","_")
        fileout = fileout.replace("_-_","_")
        fileout = fileout.replace('"',"")
        print(fileout)
        with open(fileout, 'w', encoding='utf-8') as file:
            file.write("Title: " + pod_dict["podcast_ident"])
            file.write("Content: " + text)
