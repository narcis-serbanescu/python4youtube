#!/usr/bin/env python
import os
from pytube import Playlist


def get_plist():
    my_plist = 'https://youtube.com/playlist?list=PLcfK69wvRgGcm4j92pXKYsJSzX3zD8M_7'
    playlist = Playlist(my_plist)
    print('Number of videos in playlist: %s' % len(playlist.video_urls))
    playlist_file = "hp.txt"
    try:
        os.remove(playlist_file)
    except OSError:
        pass

    for video_url in playlist.video_urls:
        print(video_url)
        with open(playlist_file, "a") as hp_play_list:
            hp_play_list.write(video_url + '\n')
    # playlist.download_all()


def main():
    get_plist()


if __name__ == "__main__":
    main()
