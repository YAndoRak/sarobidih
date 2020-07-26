from __future__ import unicode_literals
import youtube_dl
import os
from moviepy.editor import *


ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})
ydlaudio = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})
def find_ydl_url(url):
    with ydl:
        result = ydl.extract_info(
            url,
            download=False # We just want to extract the info
        )

    if 'entries' in result:
        video = result['entries'][0]
    else:
        video = result

    video_urls = video['formats']
    for video_url in video_urls:
        if video_url['format_id'] == '18' :
            print('=================================== 360 P ====================================')
            print('Extension : {}'.format(video_url['ext']))
            print('URL : {}'.format(video_url['url']))
            print('Fomart ID: {}'.format(video_url['format_id']))
            print('Fomart : {}'.format(video_url['format']))
            print('Filesize : {}'.format(video_url['filesize']))
            print('=================================== 360 P ====================================')
            return video_url
def find_audio_url(url_audio):
    with ydlaudio:
        resultaudio = ydlaudio.extract_info(
            url_audio,
            download=False # We just want to extract the info
        )

    if 'entries' in resultaudio:
        audio = resultaudio['entries'][0]
    else:
        audio = resultaudio

    audio_urls = audio['formats']
    print(audio_urls)
    for audio_url in audio_urls:
        print(audio_url)
        print('=================================== M4a ====================================')
        print('Extension : {}'.format(audio_url['ext']))
        print('URL : {}'.format(audio_url['url']))
        print('Fomart ID: {}'.format(audio_url['format_id']))
        print('Fomart : {}'.format(audio_url['format']))
        print('Filesize : {}'.format(audio_url['filesize']))
        print('=================================== M4a ====================================')
def download_video(url):
    ydl_opts = {
        'outtmpl': './tmp/video/%(title)s.%(ext)s',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_audio(url):
    ydl_opts = {
        'outtmpl': './tmp/audio/%(title)s.%(ext)s',
        'format': '18/best',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        info_dict = ydl.extract_info(url, download=False)
        input = ydl.prepare_filename(info_dict)

    output = '{}mp3'.format(input[:-3])
    video = VideoFileClip(os.path.join(input))
    video.audio.write_audiofile(os.path.join(output))
    url = {
        "input": input,
        "output": output
    }
    return url



if __name__ == "__main__":

    output = download_audio('https://www.youtube.com/watch?v=M4EZ8kpX3Os')
    print(output)

