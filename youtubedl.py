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
    ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url_audio, download=False)
    if 'entries' in result:
        audios = result['entries'][0]
    else:
        audios = result
    audios['formats']
    for audio in audios:
        print('=================================== 360 P ====================================')
        print('Extension : {}'.format(audio['ext']))
        print('URL : {}'.format(audio['url']))
        print('Fomart ID: {}'.format(audio['format_id']))
        print('Fomart : {}'.format(audio['format']))
        print('Filesize : {}'.format(audio['filesize']))
        print('=================================== 360 P ====================================')
    print(audios['formats'])
    return audios['formats'][0]['url']
