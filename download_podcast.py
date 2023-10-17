
import os
import requests
import feedparser

def download_podcast(rss_url, save_folder, dl = False, n_dl = 1):
    # Parse the RSS feed
    feed = feedparser.parse(rss_url)
    
    # print(feed.entries[0])
    # Ensure save directory exists
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    counter = 0
    list_of_titles=[]
    # Loop through each podcast episode in the feed
    for entry in feed.entries:
        # Find a suitable audio file to download (assuming it's an MP3)
        audio_url = None
        for link in entry.enclosures:
            # print(link.type)
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
                list_of_titles.append(entry.title)
                counter += 1
        else:
            list_of_titles.append(entry.title)
            print(f"Found: '{entry.title}'")
    return list_of_titles


def download_podcast_episode(rss_url, save_folder, episode_name):
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

        if audio_url and entry.title == episode_name:
            print(f"Downloading {entry.title} ...")
            response = requests.get(audio_url, stream=True)
            tmp = entry.title
            tmp = tmp.replace(" ", "_")
            file_name = os.path.join(save_folder, tmp[:40] + '.mp3')
            with open(file_name, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)

            print(f"Downloaded {entry.title} to {file_name}")
            counter += 1

if __name__ == '__main__':
    # Input Feeds and output folder
    # RSS_URL = 'https://ploetz.podigee.io/feed/mp3'
    # SAVE_FOLDER = './downloaded_podcasts'

    # RSS_URL = 'https://feeds.lagedernation.org/feeds/ldn-mp3.xml'
    # SAVE_FOLDER = './downloaded_podcasts/lage'
    
    # RSS_URL = 'https://feeds.megaphone.fm/newheights'
    # SAVE_FOLDER = './downloaded_podcasts/new_heights'

    # RSS_URL = 'https://fmcar8.podcaster.de/dgraffe.rss'
    # SAVE_FOLDER = './downloaded_podcasts/wingfoil_experience'

    # RSS_URL = 'https://jung-naiv.podigee.io/feed/mp3'
    # SAVE_FOLDER = './downloaded_podcasts/jung_und_naiv'
    
    # RSS_URL = 'https://criticalmedia.de/feed/podcast/'
    # SAVE_FOLDER = './downloaded_podcasts/criticalmedia'

    # RSS_URL = 'https://feeds.megaphone.fm/FGP6717686883'
    # RSS_URL = 'https://daspolitikteil.podigee.io/feed/mp3'
    # SAVE_FOLDER = './downloaded_podcasts/random_collection'

    RSS_URL = 'https://feed.podbean.com/timwendelboe/feed.xml'
    SAVE_FOLDER = './downloaded_podcasts/tim_wendelboe'
    
    titles = download_podcast(RSS_URL, SAVE_FOLDER, dl=True, n_dl = 50)

    # episode_name = 'How Asylum-Seekers Shake Up Economies (Mostly in Good Ways)'
    # episode_name = input("Please enter episode to download: ")
    # download_podcast_episode(RSS_URL, SAVE_FOLDER, episode_name)

