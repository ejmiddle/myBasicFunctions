import os
import json
import re


def modify_json_content(json_content, old_string, new_string):
    json_string = json.dumps(json_content)
    # print(old_string)
    # print(new_string)
    # print(json_string)
    
    json_string = json_string.replace(old_string, new_string)
    return json.loads(json_string)

def process_json_files(folder_path, output_folder):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(folder_path, file_name)
            
            with open(file_path, 'r', encoding='utf-8') as file:
                json_content = json.load(file)
            
            old_string = 'chunk_'
            new_string = 'seg_'
            modified_content = modify_json_content(json_content, old_string, new_string)

            old_string = '"ident"'
            pattern = r'\b{}\b'.format(re.escape(old_string))

            new_string = '"podcast_ident"'
            modified_content = modify_json_content(modified_content, old_string, new_string)
            # print(modified_content)
            
            file_name = file_name.replace('"',"")
            new_file_path = os.path.join(output_folder, f"{file_name}")
            with open(new_file_path, 'w', encoding='utf-8') as file:
                json.dump(modified_content, file, indent=4)

# Usage
folder_path = "output_audio/transcripts/current_selection backup"
output_folder = "tmp"
process_json_files(folder_path, output_folder)
