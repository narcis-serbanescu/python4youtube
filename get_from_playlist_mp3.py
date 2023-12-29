#!/usr/bin/env python
from pytube import Playlist, YouTube
from pytube.exceptions import VideoUnavailable, AgeRestrictedError
from datetime import datetime
from termcolor import cprint
from moviepy.editor import *
import os
import snoop


# @snoop
def get_file(line_no, youtube_link):
    # Get the youtube link
    print("Link: ", youtube_link)
    yt = YouTube(youtube_link)

    # Try to get the youtube link when error occurs
    # https://stackoverflow.com/questions/4606919/in-python-try-until-no-error
    while "Video Not Available" in yt.title:
        cprint(yt.title, "red")
        try:
            yt = YouTube(youtube_link)
            cprint(yt.title, "yellow")
        except Exception as ex:
            cprint(ex, "red")
            pass
        except RecordingUnavailable:
            print(f'Recording {youtube_link} is unavailable!')
            pass
        except VideoUnavailable:
            print(f'Video {youtube_link} is unavailable!')
            pass
        if "Video Not Available" not in yt.title:
            break
    '''
            else:
                # execute if no exception
                # yt.streams.first().download()
                yt = YouTube(youtube_link)
                cprint(yt.title, "cyan")
                break
            finally:
                # Some code ...(always executed)
                yt = YouTube(youtube_link)
                cprint(yt.title, "green")
                print(f'Finally ... downloading video again: {youtube_link}')
    '''

    base_folder = "/Users/snarcis/tmp/mp3/"

    # Description of video
    print("Description: ", yt.description)
    desc_file = base_folder + "Read.me"
    with open (desc_file, "a") as desc:
        desc.write(str(yt.description) + '\n')

    # Audio only mp4
    try:
        ya = yt.streams.filter(only_audio=True).first()
    except Exception as exa:
        cprint(exa, "red")
        pass
    except RecordingUnavailable:
        print(f'Recording {youtube_link} is unavailable!')
        pass
    except VideoUnavailable:
        print(f'Video {youtube_link} is unavailable!')
        pass

    file_name = yt.title
    char = "|/<>?,:'}{][+_-=)(*&%$#@!~` "
    for c in char:
        file_name = file_name.replace(c, "")
    file_name_mp4 = file_name + ".mp4"

    video_folder = base_folder
    # video_folder = base_folder + "BethHart_JoeBonamassa/2011_DontExplain/"

    file_name_mp3 = str(line_no) + file_name + ".mp3"
    path2file_name_mp3 = video_folder + file_name_mp3
    path2playlist = video_folder + "playlist.m3u"
    with open(path2playlist, "a", encoding='utf-8') as f:
        f.write(file_name_mp3 + "\n")
    print("Downloading: " + yt.title + " into: " + video_folder + " folder!")
    try:
        start_time_1 = datetime.now()

        ya.download(video_folder, filename=file_name_mp4)
        # video = VideoFileClip(video_folder + file_name_mp4)
        # video.audio.write_audiofile(path2file_name_mp3)
        video = AudioFileClip(video_folder + file_name_mp4)
        video.write_audiofile(path2file_name_mp3)
        video.close()

        end_time_1 = datetime.now()
    except Exception as e:
        print("Error ...", e)
    cprint("Task completed!", "green")
    # cprint(end_time_1 - start_time_1, "green")

    # Sort playlist in m3u file
    # subprocess.run(["sort", "-h", path2playlist, ">", path2playlist])
    path2list = video_folder + "list.m3u"
    sort_cmd = "sort -h " + path2playlist + ">" + path2list
    os.system(sort_cmd)

    # Remove mp4 files only if mp3 exists
    '''
    mp4_files = os.listdir(video_folder)
    for mp4_file in mp4_files:
        if mp4_file.endswith(".mp4"):
            os.remove(os.path.join(video_folder, mp4_file))
    '''

def main():
    playlist_url = 'https://www.youtube.com/playlist?list=OLAK5uy_mXDo71jVKMdFMkpRjd-E-pnvUuuG8Nia0'
    p = Playlist(playlist_url)

    # Get line number with enumerate()
    # for lno, ytl in enumerate(ytlist):
    for lno, ytl in enumerate(p.video_urls):
        lno = lno + 1
        print("Track no.:", lno)
        print("YouTube Link ytl:", ytl)

        # Run without mp
        get_file(lno, ytl)


if __name__ == "__main__":
    main()
