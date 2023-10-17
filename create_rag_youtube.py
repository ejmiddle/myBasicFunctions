import os
import json
import csv
import pandas as pd
from pytube import YouTube

from get_transcripts import extract_youtube_video_id, get_video_transcript, get_video_description
from get_youtube_vid_urls import get_urls_from_channel

# -------- Definitions --------------------------------
rag_data = "output_youtube"

#  ---- Energiesparkommissar Info
channel_id = "UCfaiQVlrxIFnPkodykZ-zFw" # Energiesparkommissar
channel_name = "Energiesparkommissar"

# -----Akkudoktor Info
# url = "https://www.youtube.com/watch?v=K-CSz2SO4eQ"
# url = "https://www.youtube.com/watch?v=Zbc9_Pt-3H4" # akkudoktor
# channel_identifier = "UCaWbn671XbI1GLTgndyI7gQ" # Akkudoktor
# channel_name = "Akkudoktor"




# # --- Create basic infos for channel ---------------------------
channel_dict = get_urls_from_channel(channel_name, channel_id)
filename = os.path.join(rag_data, channel_name, "info.json")
with open(filename, 'w') as f:
    json.dump(channel_dict, f)
print(f"Dictionary saved to {filename}")

# --- Get transcripts and video informations ---------------------------
filename = os.path.join(rag_data, channel_name, "info.json")
with open(filename, 'r') as f:
    channel_dict = json.load(f)
print("Dictionary loaded from JSON file:", channel_dict["channel_name"])

list_of_urls = channel_dict["video_urls"]
transcript_list = []
title_list = []
descr_list = []
for video_url in list_of_urls:
    youtube = YouTube(video_url)
    title = youtube.title
    video_id = extract_youtube_video_id(video_url)
    description = get_video_description(video_id)
    # description = youtube.description
    transcript = get_video_transcript(video_id)

    transcript_list.append(transcript)
    title_list.append(title)
    descr_list.append(description)

output_path = os.path.join(rag_data, channel_dict["channel_name"], "transcripts.csv") 
with open(output_path, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["url", "title", "description", "transcript"])  # Write header row
    writer.writerows(zip(list_of_urls, title_list, descr_list, transcript_list))


##################################################################
# --- create files for rag ---------------------------
##################################################################
file_path = os.path.join(rag_data, channel_name, "transcripts.csv") 
df = pd.read_csv(file_path, delimiter=',')
print(df.head())

reversed_df = df.iloc[::-1]

counter = 1
for index, row in reversed_df.iterrows():
    title_short = df.title[index][:40]
    title_short=title_short.replace('"', '')
    title_short = title_short.replace("/","")
    title_short = title_short.replace("'","")
    title_short = title_short.replace("?","")
    title_short = title_short.replace("!","")
    print(title_short)
    filename = os.path.join(rag_data, channel_name, 'data', 'id_' + str(counter) + "_" + title_short + '.txt' )
    with open(filename, 'w', encoding='utf-8') as file:
        # Loop through each row in the DataFrame
        # Write the title, description, and transcript to the file
        file.write(f"Title: {row['title']}\n")
        file.write(f"Description: {row['description']}\n")
        file.write(f"Content: {row['transcript']}\n")
        counter += 1
        # # Optionally, add a separator between different rows
        # if index < len(df) - 1:
        #     file.write("\n" + "="*20 + "\n\n")

