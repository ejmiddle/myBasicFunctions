import re
import os
import openai
import requests

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled


def extract_youtube_video_id(url: str) -> str | None:
    """
    Extract the video ID from the URL
    https://www.youtube.com/watch?v=XXX -> XXX
    https://youtu.be/XXX -> XXX
    """
    found = re.search(r"(?:youtu\.be\/|watch\?v=)([\w-]+)", url)
    if found:
        return found.group(1)
    return None

def get_video_description(video_id: str) -> str:
    # Set up the YouTube API client
    api_key = "AIzaSyC1Tp6XrPy8vi04Gb_MIwXdoKf8GjEXoCk"

    url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={api_key}&part=snippet'

    response = requests.get(url)
    data = response.json()

    # Extract video description
    video_description = data['items'][0]['snippet']['description']
    return video_description


def get_video_transcript(video_id: str) -> str | None:
    """
    Fetch the transcript of the provided YouTube video
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['de', 'en'])
    except TranscriptsDisabled:
        # The video doesn't have a transcript
        return None

    text = " ".join([line["text"] for line in transcript])
    return text



def generate_summary(text: str) -> str:
    """
    Generate a summary of the provided text using OpenAI API
    """
    # Initialize the OpenAI API client
    openai.api_key = os.environ["OPENAI_API_KEY"]

    # Use GPT to generate a summary
    instructions = "Please summarize the provided text"
    # instructions = "Where do the problematic parts come from?"
    # instructions = "Where do the problematic parts come from?"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        # model="gpt-4",
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": text}
        ],
        temperature=0.2,
        n=1,
        max_tokens=200,
        presence_penalty=0,
        frequency_penalty=0.1,
    )

    # Return the generated summary
    return response.choices[0].message.content.strip()


def summarize_youtube_video(video_url: str) -> str:
    """
    Summarize the provided YouTube video
    """
    # Extract the video ID from the URL
    video_id = extract_youtube_video_id(video_url)

    # Fetch the video transcript
    transcript = get_video_transcript(video_id)


    # If no transcript is found, return an error message
    if not transcript:
        return f"No English transcript found " \
               f"for this video: {video_url}"
    
    max_transcript_size = 16000
    if len(transcript) > max_transcript_size:
        print("Reducing transcript")
        transcript = transcript[:max_transcript_size]

    # Generate the summary
    summary = generate_summary(transcript)

    # Return the summary
    return summary



# rag_data = "RAG_data"
# transcr_folder = "transcripts/"
# filename = os.path.join(rag_data, "Energiesparkommissar_info.json")

# # Open the file in read mode and load the JSON content into a dictionary
# with open(filename, 'r') as f:
#     channel_dict = json.load(f)
# print("Dictionary loaded from JSON file:", channel_dict["channel_name"])

# list_of_urls = channel_dict["video_urls"]
# transcript_list = []
# for video_url in list_of_urls:
#     print(video_url)
#     video_id = extract_youtube_video_id(video_url)
#     transcript = get_video_transcript(video_id)
#     transcript_list.append(transcript)


# output_path = os.path.join(rag_data, transcr_folder, channel_dict["channel_name"] + "_transcr.csv") 
# with open(output_path, 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(["url", "transcript"])  # Write header row
#     writer.writerows(zip(list_of_urls, transcript_list))

