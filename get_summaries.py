from dotenv import load_dotenv
load_dotenv()
import os
import json

from langchain.chat_models import ChatOpenAI
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.docstore.document import Document

from  src.audio_functions import *
from  src.text_manip_functions import *

input_folder = "output_audio/transcripts/current_selection"
summary_data = "output_audio/summaries/current_selection"

# Define prompt
prompt_template = """Write a concise summary of the text between triple backticks. 
Extract the most important aspects of the discussion and structure the aspects with bulletpoints in the summary.
Summary should be in german. 

'''{text}'''

CONCISE SUMMARY:"""
prompt = PromptTemplate.from_template(prompt_template)

# Define LLM chain
llm = ChatOpenAI(temperature=0.1, model_name="gpt-3.5-turbo")
llm_chain = LLMChain(llm=llm, prompt=prompt)

# Define StuffDocumentsChain
stuff_chain = StuffDocumentsChain(
    llm_chain=llm_chain, document_variable_name="text"
)

if not os.path.exists(summary_data):
    os.makedirs(summary_data)

counter = 0
for filename in os.listdir(input_folder):
    if filename.endswith(".json"):
        print(filename)
        path_to_file = os.path.join(input_folder, filename)
        with open(path_to_file, 'r') as f:
            pod_dict = json.load(f)
        text = pod_dict["text"]
        doc = []
        doc.append(Document(page_content=text, metadata={"source": filename}))
        summary = stuff_chain.run(doc)

        fileout = os.path.join(summary_data, pod_dict["podcast_ident"] + '_' + pod_dict["seg_ident"] + '.json' )
        audio_seg_dict = {
            "audio_seg_ident": pod_dict["seg_ident"],
            "podcast_ident": pod_dict["podcast_ident"],
            "summary": summary
        }

        fileout = fileout.replace('"','')
        with open(fileout, 'w') as f:
            json.dump(audio_seg_dict, f)

        # counter += 1
        # if counter > 1:
        #     break

