#!/usr/bin/env python3
from pytube import YouTube
import multiprocessing as mp
from datetime import datetime
from termcolor import cprint


def get_file(youtube_link):
    global yt
    print("Link: ", youtube_link)
    try:
        yt = YouTube(youtube_link)
    except Exception as e1:
        cprint("Connection error! " + str(e1), "red")
        pass
    # yt = YouTube(youtube_link)

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

    # Get available subtitles
    print (yt.captions)

    # Audio only mp4
    ya = yt.streams.filter(only_audio=True).first()

    ys = yt.streams.get_highest_resolution()
    print("Hihgest Resolution: ", ys)

    global file_name
    file_name = yt.title
    # Remove non-chars fron filename
    char = "|/<>?,:'}{][+_-=)(*&%$#@!~` "
    for c in char:
        file_name = file_name.replace(c, "")
    full_file_name = file_name + ".mp4"
    global video_folder
    video_folder = "/Users/snarcis/tmp/"
    print("Downloading: " + yt.title + " into: " + video_folder + " folder!")
    try:
        start_time_1 = datetime.now()
        ys.download(video_folder, filename=full_file_name)
        end_time_1 = datetime.now()
    except VideoUnavailable:
        print(f"Video {yt.title} Unavailable")
    except Exception as e:
        print("Error ...", e)
    cprint("Task completed!", "green")
    cprint(end_time_1 - start_time_1, "green")


def get_sub(youtube_link):
    # https://stackoverflow.com/questions/68780808/xml-to-srt-conversion-not-working-after-installing-pytube
    global yt
    yt = YouTube(youtube_link)
    # print the all avaible caption list, to see  language code
    print("All Avaible Captions : \n",yt.captions)

    # Iterate over subs
    subs_dict = yt.captions
    print (type(subs_dict))
    for key in subs_dict:
        print(key)

    # to get particular langauge caption you need to pass the language code e.g, captions['a.en']
    en_caption_data = yt.captions['a.en']

    print("\nCaption Data in SRT Format: \n")

    # call .xml_caption_to_srt() function and pass the XML Caption as an arguments
    # srt_format = en_caption_data.xml_caption_to_srt(en_caption_data.xml_captions)
    srt_format = en_caption_data.generate_srt_captions()

    # print / export caption in SRT format
    # print(srt_format)
    with open(video_folder + file_name + '.srt', 'w') as srt_file:
        srt_file.write(srt_format)


def main():
    max_proc = mp.cpu_count()
    cprint("Number of processors: " + str(max_proc), "cyan")

    youtube_links_list = list()

    if len(youtube_links_list) == 0:
        yt_file = "dan_dart.txt"
        # yt_file = ""
        try:
            ytlist = open(yt_file, "r")
            for ytl in ytlist:
                print("ytl", ytl)
                ytl = ytl.rstrip('\r\n')
                # Skip commented lines
                # Skip empty lines, read only existing ines
                if (ytl) and (not ytl.startswith("#")):
                    cprint(ytl, "green")
                    youtube_links_list.append(ytl)
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
    # output = pool.map(get_file, youtube_links_list)
    pool.map(get_file, youtube_links_list)
    # pool.map(get_sub, youtube_links_list)

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
