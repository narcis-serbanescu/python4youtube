from pytube import Playlist, YouTube
from pytube.exceptions import VideoUnavailable, AgeRestrictedError
playlist_url = 'https://youtube.com/playlist?list=special_playlist_id'
p = Playlist(playlist_url)
for url in p.video_urls:
    try:
        yt = YouTube(url)
    except VideoUnavailable:
        print(f'Video {url} is unavaialable, skipping.')
    except AgeRestrictedError:
        print(f'Video {url} is unavaialable, skipping.')
    else:
        print(f'Downloading video: {url}')
        yt.streams.first().download()

