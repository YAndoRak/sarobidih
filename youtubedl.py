import youtube_dl
ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})
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
    for audio_url in audio_urls:
        if audio_url['ext'] == 'm4a' :
            print('=================================== M4a ====================================')
            print('Extension : {}'.format(audio_url['ext']))
            print('URL : {}'.format(audio_url['url']))
            print('Fomart ID: {}'.format(audio_url['format_id']))
            print('Fomart : {}'.format(audio_url['format']))
            print('Filesize : {}'.format(audio_url['filesize']))
            print('=================================== M4a ====================================')
            return audio_url
#     ydl_opts = {
#     'format': 'bestaudio/best',
#     'postprocessors': [{
#         'key': 'FFmpegExtractAudio',
#         'preferredcodec': 'mp3',
#         'preferredquality': '192'
#     }],
#     'postprocessor_args': [
#         '-ar', '16000'
#     ],
#     'prefer_ffmpeg': True,
#     'keepvideo': True
#     }
#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         ydl.download(url_audio)

# if __name__ == "__main__":
#     print(find_audio_url(["https://www.youtube.com/watch?v=Cfv7qHMeNS4"]))
