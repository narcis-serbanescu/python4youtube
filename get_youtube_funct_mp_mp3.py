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
    global yt
    print("Link: ", youtube_link)
    try:
        yt = YouTube(youtube_link)
    except Exception as e1:
        cprint("Connection error! " + str(e1), "red")
        pass
#    yt = YouTube(youtube_link)

    # Title of video
    print("Title: ", yt.title)

    # Number of views of video
    print("Number of views: ", yt.views)

    # Length of the video
    print("Length of video: ", yt.length, "seconds")

    # Description of video
    print("Description: ", yt.description)

    # Rating
    print("Ratings: ", yt.rating)

    # printing all the available streams
    # print(yt.streams)

    print(yt.streams.filter(progressive=True))

    # Audio only mp4
    ya = yt.streams.filter(only_audio=True).first()
    # ya = yt.streams.filter().first()

    # ys = yt.streams.get_highest_resolution()
    # print("Hihgest Resolution: ", ys)

    file_name = yt.title
    char = "|/<>?,:'}{][+_-=)(*&%$#@!~` "
    for c in char:
        file_name = file_name.replace(c, "")
    file_name_mp4 = file_name + ".mp4"

    base_folder = "/Users/snarcis/tmp/mp3/"
    video_folder = base_folder
    # video_folder = base_folder + "Coldplay_mp3/2021_MusicOfTheSpheres/"
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
        # yt_file = "ylinks_Coldplay.txt"
        # yt_file = "ylinks_EndlessRiver.txt"
        # yt_file = "ylinks_Hart.txt"
        yt_file = "TheFaces_Nod.txt"
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
            ytlist.close()
        except IOError as e:
            cprint("Unable to open file " + yt_file, "red")
            print(e)
            youtube_links = input("Enter comma separated links: ")
            if not youtube_links or youtube_links == "q":
                exit()
            youtube_links_list = youtube_links.split(",")
            print("Youtube links: ", youtube_links_list)
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


if __name__ == "__main__":
    main()
