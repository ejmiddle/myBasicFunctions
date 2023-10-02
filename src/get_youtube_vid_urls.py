from googleapiclient.discovery import build
import json
import os

def get_urls_from_channel(channel_name: str, channel_id: str ) -> str:

    # Set up the YouTube API client
    api_key = "AIzaSyC1Tp6XrPy8vi04Gb_MIwXdoKf8GjEXoCk"
    youtube = build('youtube', 'v3', developerKey=api_key)

    # ------ Retrieve channel details using the Channels API
    channel_response = youtube.channels().list(
        part='snippet,contentDetails,statistics',
        id=channel_id
    ).execute()

    # Extract the channel information from the response
    channel = channel_response['items'][0]
    channel_title = channel['snippet']['title']
    channel_description = channel['snippet']['description']
    channel_subscriber_count = channel['statistics']['subscriberCount']

    # Print the channel information
    print(f"Channel Title: {channel_title}")
    print(f"Channel Description: {channel_description}")
    print(f"Subscriber Count: {channel_subscriber_count}")
    # Extract the video count from the channel statistics
    video_count = int(channel_response['items'][0]['statistics']['videoCount'])
    # Print the total number of videos
    print(f"Total number of videos: {video_count}")



    # Retrieve the playlist ID of the uploaded videos for the channel
    channel_response = youtube.channels().list(
        part='contentDetails',
        id=channel_id
    ).execute()
    playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    # Retrieve the video details from the playlist using the PlaylistItems API
    videos = []
    next_page_token = None
    while True:
        playlist_items_response = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=10,
            pageToken=next_page_token
        ).execute()

        videos.extend(playlist_items_response['items'])
        next_page_token = playlist_items_response.get('nextPageToken')
        if not next_page_token:
            break

    # Extract the video URLs from the video details
    video_urls = []
    titles = []
    descriptions = []
    for video in videos:
        video_id = video['snippet']['resourceId']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        video_urls.append(video_url)

        title = video['snippet']['title']
        titles.append(title)

        description = video['snippet']['description']
        descriptions.append(description)

    # # Print the list of video URLs
    # for video_url in video_urls:
    #     print(video_url)
    # print(len(video_urls))

    channel_dict = {
    "channel_name": channel_name,
    "channel_id": channel_id,
    "video_urls": video_urls,
    "channel_title": channel_title,  # Assigning the existing list to the 'url' key
    "channel_descr": channel_description
    }

    return channel_dict

# # Energiesparkommissar Info
# channel_id = "UCfaiQVlrxIFnPkodykZ-zFw" # Energiesparkommissar
# channel_name = "Energiesparkommissar"

# channel_dict = get_urls_from_channel(channel_name, channel_id)
# # print(channel_dict)

# output_data = "RAG_data"
# filename = os.path.join(output_data, channel_name + "_info.json")
# with open(filename, 'w') as f:
#     json.dump(channel_dict, f)
# print(f"Dictionary saved to {filename}")


    # # Specify the file path
    # file_path = data_path + "output_" + channel_name + ".csv"

    # # Write the list of strings to a CSV file
    # print("writing to " + file_path)
    # with open(file_path, 'w', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(["title", "description", "urls"])  # Write header row
    #     writer.writerows(zip(titles, descriptions, video_urls))



