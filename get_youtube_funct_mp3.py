#!/usr/bin/env python
from pytube import YouTube
import multiprocessing as mp
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
        desc.write(yt.description + '\n')

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
    max_proc = mp.cpu_count()
    cprint("Number of processors: " + str(max_proc), "cyan")

    youtube_links_list = list()
    line_no_list = list()

    if len(youtube_links_list) == 0:
        # yt_file = "ylinks_S02.txt"
        # yt_file = "ylinks_Coldplay_2021.txt"
        # yt_file = "ylinks_Coldplay.txt"
        # yt_file = "ylinks_ABBA2021Voyage.txt"
        # yt_file = "ylinks_EndlessRiver.txt"
        # yt_file = "ylinks_Hart.txt"
        # yt_file = "TheFaces_Nod.txt"
        yt_file = "ylinks_DBowie_GH.txt"

        try:
            ytlist = open(yt_file, "r")

            # Get line number with enumerate()
            for lno, ytl in enumerate(ytlist):
                lno = lno + 1
                print("Line no.:", lno)
                print("Link ytl:", ytl)
                ytl = ytl.rstrip('\n')
                youtube_links_list.append(ytl)
                line_no_list.append(lno)

                # Run without mp
                get_file(lno, ytl)
            ytlist.close()
        except IOError as e:
            cprint("Unable to open file " + yt_file, "red")
            print(e)
            youtube_links = input("Enter comma separated links: ")
            if not youtube_links or youtube_links == "q":
                exit()
            youtube_links_list = youtube_links.split(",")
            print("Youtube links: ", youtube_links_list)

    '''
    threads = len(youtube_links_list)
    if threads >= max_proc:
        threads == max_proc

    start_time = datetime.now()

    pool = mp.Pool(processes=threads)

    # Multiprocess function with one argument
    ## output = pool.map(get_file, youtube_links_list)
    # pool.map(get_file, youtube_links_list)

    # Multiprocess function with two argument
    pool.starmap(get_file, zip(line_no_list, youtube_links_list))

    # Async https://medium.com/swlh/5-step-guide-to-parallel-processing-in-python-ac0ecdfcea09
    # outputs_async = pool.map_async(get_file, youtube_links_list)
    # outputs = outputs_async.get()
    # print("Output: {}".format(outputs))

    # pool.daemon = True
    pool.close()
    pool.join()
    end_time = datetime.now()
    print("Duration: ", end_time - start_time)
    '''

if __name__ == "__main__":
    main()
