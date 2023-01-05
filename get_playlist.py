#!/usr/bin/env python3
import os
from pytube import Playlist


def get_plist():
    # my_plist = 'https://youtube.com/playlist?list=PLcfK69wvRgGcm4j92pXKYsJSzX3zD8M_7'
    # my_plist = 'https://www.youtube.com/playlist?list=PLo2aaBamFnLQ8RxE-JJpf9tSuiyHPKHoH'

    # Coldplay_2021
    # my_plist = 'https://www.youtube.com/watch?v=cZYKKcof30Q&list=PLxA687tYuMWhVKD7kmUOP8131O7ym8LJZ'

    # ABBA_2021
    aname = "ABBA2021Voyage"
    my_plist = 'https://www.youtube.com/playlist?list=PLxA687tYuMWiaZm97zAKxm6AGNVEWBm9F'

    # David Bowie
    # aname = "DBowie_GH"
    # my_plist = 'https://www.youtube.com/playlist?list=PLkRzqIoq7yc3A5-7E6bDlk5PLeJMNfZIi'

    playlist = Playlist(my_plist)
    # print('Number of videos in playlist: %s' % len(playlist.video_urls))
    playlist_file = "ylinks_" + aname + ".txt"
    # print(f"Writing into {playlist_file}")
    print(f"Number of videos in {playlist_file}: {len(playlist.video_urls)}")

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
