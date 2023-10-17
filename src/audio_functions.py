from pydub import AudioSegment
import os
import shutil
import openai
import json
import asyncio
from dotenv import load_dotenv
load_dotenv()


def extract_first_n_sec(input_mp3, output_mp3, start_sec, n_sec):
    # Load the MP3 audio file
    audio = AudioSegment.from_mp3(input_mp3)

    print(len(audio)/(1000*60))

    start_time = start_sec*1000
    end_time = (start_sec + n_sec) * 1000
    extract = audio[start_time:end_time]

    print(len(extract)/(1000*60))
    # Export the extracted audio to an MP3 file
    extract.export(output_mp3, format="mp3")



def empty_folder(path):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")


def split_mp3(input_file, output_dir, seg_length=10*60*1000, overlap=10*1000):  # overlap is set to 10 seconds
    # Load the audio file
    audio = AudioSegment.from_mp3(input_file)
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    empty_folder(output_dir)

    # Split the audio and save the chunks
    i = 0
    start_time = 0
    while start_time < len(audio):
        end_time = start_time + seg_length
        chunk = audio[start_time:end_time]
        chunk.export(f"{output_dir}/seg_{i}.mp3", format="mp3")
        
        start_time += seg_length - overlap
        i += 1

    print(f"Successfully split the audio into {i} chunks!")

def get_transcript_for_dir(directory_path, output_dir, podcast_ident):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(directory_path):
        if filename.endswith(".mp3"):
            print("Processing ... ", filename)
            file_path = os.path.join(directory_path, filename)
            audio_file= open(file_path, "rb")
            transcript = openai.Audio.transcribe("whisper-1", audio_file, api_key=os.getenv("OPENAI_API_KEY"))

            # --- Format and write outputs
            seg_ident = os.path.splitext(filename)[0]
            seg_dict = {
                "seg_ident": seg_ident,
                "podcast_ident": podcast_ident,
                "text": transcript["text"]
            }
            filename = os.path.join(output_dir, podcast_ident + "_" + seg_ident + ".json")
            with open(filename, 'w') as f:
                json.dump(seg_dict, f)
            print(f"Transcript saved to {filename}")

async def get_transcript_for_file_async(directory_path, filename, output_dir, podcast_ident):
    print("Processing ... ", filename)
    file_path = os.path.join(directory_path, filename)
    audio_file= open(file_path, "rb")
    transcript = await openai.Audio.atranscribe("whisper-1", audio_file, api_key=os.getenv("OPENAI_API_KEY"))

    # --- Format and write outputs
    seg_ident = os.path.splitext(filename)[0]
    seg_dict = {
        "seg_ident": seg_ident,
        "podcast_ident": podcast_ident,
        "text": transcript["text"]
    }
    filename = os.path.join(output_dir, podcast_ident + "_" + seg_ident + ".json")
    with open(filename, 'w') as f:
        json.dump(seg_dict, f)
    print(f"Transcript saved to {filename}")
    return filename

async def get_transcript_for_dir_async(directory_path, output_dir, podcast_ident):
    if not os.path.exists(output_dir):
        print("Creating output dir ... ")
        os.makedirs(output_dir)

    tasks = []  # Creating an empty list to hold tasks
    for filename in os.listdir(directory_path):
        if filename.endswith(".mp3"):
            task = asyncio.create_task(
                get_transcript_for_file_async(directory_path, filename, output_dir, podcast_ident)
            )  # Creating a task
            tasks.append(task)  # Appending the task to the list
    
    print("Tasks created ... ")

    results = await asyncio.gather(*tasks)
    print("Results: ", results)

    return results


# async def get_transcript_for_dir_async(directory_path, output_dir, podcast_ident):
#     if not os.path.exists(output_dir):
#         print("Creating output dir ... ")
#         os.makedirs(output_dir)

#     tasks = []  # Creating an empty list to hold tasks
#     for filename in os.listdir(directory_path):
#         if filename.endswith(".mp3"):
#             # task = asyncio.run(get_transcript_for_file_async(directory_path, filename, output_dir, podcast_ident))            
#             task = asyncio.get_transcript_for_file_async(directory_path, filename, output_dir, podcast_ident)  # Creating a task
#             tasks.append(task)  # Appending the task to the list    
#     print("Tasks created ... ")

#     results = await asyncio.gather(*tasks)
#     print("Results: ", results)

#     return results
