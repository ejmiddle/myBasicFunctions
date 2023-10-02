
import os
import requests
import feedparser

def download_podcast(rss_url, save_folder, dl = False, n_dl = 1):
    # Parse the RSS feed
    feed = feedparser.parse(rss_url)
    
    print(feed.entries[0])
    # Ensure save directory exists
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    counter = 0
    # Loop through each podcast episode in the feed
    for entry in feed.entries:
        # Find a suitable audio file to download (assuming it's an MP3)
        audio_url = None
        for link in entry.enclosures:
            print(link.type)
            if 'audio/mpeg' in link.type:
                audio_url = link.href
                break

        if dl and counter < n_dl:
            # If we found an audio link, download it
            if audio_url:
                response = requests.get(audio_url, stream=True)
                tmp = entry.title
                tmp = tmp.replace(" ", "_")
                file_name = os.path.join(save_folder, tmp[:30] + '.mp3')
                with open(file_name, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            file.write(chunk)

                print(f"Downloaded {entry.title} to {file_name}")
                counter += 1
        else:
            print(f"Found: {entry.title}")

if __name__ == '__main__':
    # Input Feeds and output folder
    # RSS_URL = 'https://ploetz.podigee.io/feed/mp3'
    # SAVE_FOLDER = './downloaded_podcasts'

    # RSS_URL = 'https://feeds.lagedernation.org/feeds/ldn-mp3.xml'
    # SAVE_FOLDER = './downloaded_podcasts/lage'
    
    RSS_URL = 'https://feeds.megaphone.fm/newheights'
    SAVE_FOLDER = './downloaded_podcasts/new_heights'


    
    download_podcast(RSS_URL, SAVE_FOLDER, dl=True, n_dl = 2)

