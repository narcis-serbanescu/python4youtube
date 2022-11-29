#/usr/bin/env python3
# https://codenaive.com/python/python-examples/how-to-download-youtube-captions-in-srt-using-pytube-in-python/
# https://stackoverflow.com/questions/68780808/xml-to-srt-conversion-not-working-after-installing-pytube

# Import Pytube module to use API
from pytube import YouTube


video_url = 'https://https://youtu.be/mBJMkFNRVek'
# video_url = 'https://www.youtube.com/watch?v=ekTJG9P9JHU'
# create an object of YouTube() and pass the  URL of YouTube Videos
video_src = YouTube(video_url)

# print the all avaible caption list, to see  language code
print("All Avaible Captions : \n",video_src.captions)

# to get particular langauge caption you need to pass the language code e.g, captions['a.en']
en_caption_data = video_src.captions['a.en']

print("\nCaption Data in SRT Format: \n")

# call .xml_caption_to_srt() function and pass the XML Caption as an arguments
srt_format = en_caption_data.xml_caption_to_srt(en_caption_data.xml_captions)

# print caption in SRT format
print(srt_format)
