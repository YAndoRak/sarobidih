import random, json
from flask import Flask, request
from pymessenger.bot import Bot
import requests
from scrapping import scrape_google, scrape_youtube
from response import help, other
from fbmessenger import BaseMessenger
from fbmessenger.elements import Text
from fbmessenger.attachments import Image, Video
from youtubedl import find_ydl_url, find_audio_url, download_audio, download_video
from pdfconverter import convert_url_img, convert_url_pdf
import os
from requests_toolbelt import MultipartEncoder
import threading
import atexit


app = Flask(__name__)

ACCESS_TOKEN = 'EAAI1QygXjocBAJupxEXFiNJAFlIGCA44EjIe1Itui35dZCfTZAZCZAUiZBYCRcbs6X4sDhOq5IKm6OJK16i9hqw7d3podv0717ezpMwiDspFfaYiH1vsyZBDIvgYtLOa6dca2GSPv9RuD2R0Be7CW29jaBrde85y3kX8OSDwzmZBc3ptnKgo20y    '

VERIFY_TOKEN = 'd8230120b243bf986a3f998a24db674c451160a6'
bot = Bot(ACCESS_TOKEN)

elements2 = [{
    "type": "phone_number",
    "title": "Jao's phone",
    "payload": "+261329125857"
}]


################ fb messenger #################"""
#test
def process_message(message):
    response = Video(url='https://brash-lime-enigmosaurus.glitch.me/myvideo.webm')
    return response.to_dict()


class Messenger(BaseMessenger):
    def __init__(self, page_access_token):
        self.page_access_token = page_access_token
        super(Messenger, self).__init__(self.page_access_token)

    def message(self, message):
        action = process_message(message)
        res = self.send(action, 'RESPONSE')
        return 'success'

    def postback(self, message):
        payload = message['postback']['payload'].split()
        url_video = find_ydl_url(payload[1])
        payload2 = url_video['url']
        payload1 = payload[0]


        if 'viewvideo' in payload1:
            response = Video(url=payload2)
        else:
            response = Text(text='This is an example text message.')
        action = response.to_dict()
        self.send(action)
        return 'success'


request_check = {'previous': '', 'recent': ''}

messenger = Messenger(ACCESS_TOKEN)

POOL_TIME = 1000 #Seconds
dataLock = threading.Lock()
yourThread = threading.Thread()


# We will receive messages that Facebook sends our bot at this endpoint
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    else:
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                print(message)
                if message.get('message'):
                    recipient_id = message['sender']['id']
                    if message['message'].get('text'):
                        receive_message = message['message'].get('text').split()
                        print(receive_message)
                        if (receive_message[0] == "search_google"):
                            if len(receive_message) < 2:
                                send_message(recipient_id,'Veuillez réessayer la syntaxe exacte doit être search_google + mot_recherché')
                            else:
                                response_query = ' '.join(map(str, receive_message[1:]))
                                send_message(recipient_id,'ok, research google {} en cours ....'.format(response_query))
                                send_generic_template_google(recipient_id, response_query)

                        elif (receive_message[0].upper() == "YTB"):
                            if len(receive_message) < 2:
                                send_message(recipient_id,'Veuillez réessayer la syntaxe exacte doit être ytb + mot_recherché')
                            else:
                                response_query = ' '.join(map(str, receive_message[1:]))
                                send_message(recipient_id,'ok, recherche youtube 🔑{}🔑 en cours ....'.format(response_query))
                                send_generic_template_youtube(recipient_id, response_query)

                        elif (receive_message[0].upper() == "HELP"):
                            response_sent_text = help()
                            send_message(recipient_id, response_sent_text)
                        else:
                            response_sent_text = other()
                            send_message(recipient_id, response_sent_text)


                    if message['message'].get('attachments'):
                        response_sent_nontext = get_message()
                        send_message(recipient_id, response_sent_nontext)

                if message.get('postback'):
                    recipient_id = message['sender']['id']
                    if message['postback'].get('payload'):
                        receive_postback = message['postback'].get('payload').split()
                        if receive_postback[0] == "PDF_view":
                            if len(receive_postback) < 2:
                                send_message(recipient_id,
                                             'Veuillez réessayer la syntaxe exacte doit être PDF_view + lien_recherché')
                            else:
                                response_query = ' '.join(map(str, receive_postback[1:]))
                                type_query = 'pdf'
                                request_check['recent'] = response_query + type_query
                                request_check['recent'] = response_query
                                with dataLock:
                                    print('======================================request check=====================================')
                                    print(request_check)
                                    print('======================================request check=====================================')
                                    if (request_check['previous'] != request_check['recent']):
                                        send_message(recipient_id, 'ok, Envoye {} en cours ....'.format(response_query))
                                        pdf_path = convert_url_pdf(receive_postback[1])
                                        upload_file_filedata(recipient_id, pdf_path)
                                        send_message(recipient_id, 'Profiter bien')
                                atexit.register(interrupt)
                                atexit.unregister
                                yourThread = threading.Timer(POOL_TIME, timeout(), ())
                                yourThread.start()
                                request_check['previous'] = request_check['recent']
                                request_check['recent'] = ''
                                print('=============================== verify ==============================')
                                print(request_check)
                                print('=============================== verify ==============================')
                        if receive_postback[0] == "IMAGE_view":
                            if len(receive_postback) < 2:
                                send_message(recipient_id,
                                             'Veuillez réessayer la syntaxe exacte doit être PDF_view + lien_recherché')
                            else:
                                response_query = ' '.join(map(str, receive_postback[1:]))
                                type_query = 'image'
                                request_check['recent'] = response_query + type_query
                                request_check['recent'] = response_query
                                with dataLock:
                                    print('======================================request check=====================================')
                                    print(request_check)
                                    print('======================================request check=====================================')
                                    if (request_check['previous'] != request_check['recent']):
                                        send_message(recipient_id, 'ok, Envoye {} en cours ....'.format(response_query))
                                        image_path = convert_url_img(receive_postback[1])
                                        upload_img_filedata(recipient_id, image_path)
                                        send_message(recipient_id, 'Profiter bien')
                                atexit.register(interrupt)
                                atexit.unregister
                                yourThread = threading.Timer(POOL_TIME, timeout(), ())
                                yourThread.start()
                                request_check['previous'] = request_check['recent']
                                request_check['recent'] = ''
                                print('=============================== verify ==============================')
                                print(request_check)
                                print('=============================== verify ==============================')
                        if receive_postback[0] == "image":
                            response_query = ' '.join(map(str, receive_postback[1:]))
                            send_message(recipient_id, 'ok, Teléchargement {} en cours ....'.format(response_query))
                            messenger.handle(request.get_json(force=True))
                        if receive_postback[0] == "viewaudio":
                            response_query = ' '.join(map(str, receive_postback[1:]))
                            type_query = 'audio'
                            request_check['recent'] = response_query + type_query
                            request_check['recent'] = response_query
                            print( '======================================request check=====================================')
                            print(request_check)
                            print( '======================================request check=====================================')
                            with dataLock:
                                if (request_check['previous'] != request_check['recent']):
                                    send_message(recipient_id, 'Please, veuillez patientez🙏🙏\n\nenvoye en cours📫')
                                    audio_path = download_audio(receive_postback[1])
                                    upload_audio_filedata(recipient_id, audio_path['output'])
                                    #audio_url = find_audio_url(receive_postback[1])
                                    #attachmentID = upload_audio_fb(recipient_id, audio_url['url'])
                                    #upload_audio_attachements(recipient_id, attachmentID)
                                    send_message(recipient_id, 'Profiter bien')
                            atexit.register(interrupt)
                            atexit.unregister
                            yourThread = threading.Timer(POOL_TIME, timeout(), ())
                            yourThread.start()
                            request_check['previous'] = request_check['recent']
                            request_check['recent'] = ''
                            print('=============================== verify ==============================')
                            print(request_check)
                            print('=============================== verify ==============================')
                            return 'start'
                        if receive_postback[0] == "viewvideo":
                            response_query = ' '.join(map(str, receive_postback[1:]))
                            type_query = 'video'
                            request_check['recent'] = response_query + type_query
                            with dataLock:
                                print('======================================request check=====================================')
                                print(request_check)
                                print('======================================request check=====================================')
                                if (request_check['previous'] != request_check['recent']):
                                    send_message(recipient_id, 'Please, veuillez patientez🙏🙏\n\nenvoye en cours📫')
                                    messenger.handle(request.get_json(force=True))
                                    send_message(recipient_id, 'Profiter bien')
                            atexit.register(interrupt)
                            atexit.unregister
                            yourThread = threading.Timer(POOL_TIME, timeout(), ())
                            yourThread.start()
                            request_check['previous'] = request_check['recent']
                            request_check['recent'] = ''
                            print('=============================== verify ==============================')
                            print(request_check)
                            print('=============================== verify ==============================')
                            return 'start'
                        if receive_postback[0] == "Down_youtube":
                            if len(receive_postback) < 2:
                                send_message(recipient_id, 'Erreur veuillez recommencer')
                            else:
                                response_query = ' '.join(map(str, receive_postback[1:]))
                                send_generic_template_download_youtube(recipient_id, response_query)
                        if receive_postback[0] == "audio_download":
                            if len(receive_postback) < 2:
                                send_message(recipient_id, 'Erreur veuillez recommencer')
                            else:
                                response_query = ' '.join(map(str, receive_postback[1:]))
                                type_query = 'down_audio'
                                request_check['recent'] = response_query + type_query
                                with dataLock:
                                    print('======================================request check=====================================')
                                    print(request_check)
                                    print('======================================request check=====================================')
                                    if (request_check['previous'] != request_check['recent']):
                                        send_message(recipient_id, 'Please, veuillez patientez🙏🙏\n\nTélechargement en cours📫')
                                        audio_path = download_audio(receive_postback[1])
                                        upload_file_filedata(recipient_id, audio_path['output'])
                                        send_message(recipient_id, 'Profiter bien')
                                atexit.register(interrupt)
                                atexit.unregister
                                yourThread = threading.Timer(POOL_TIME, timeout(), ())
                                yourThread.start()
                                request_check['previous'] = request_check['recent']
                                request_check['recent'] = ''
                                print('=============================== verify ==============================')
                                print(request_check)
                                print('=============================== verify ==============================')

                        if receive_postback[0] == "video_download":
                            if len(receive_postback) < 2:
                                send_message(recipient_id, 'Erreur veuillez recommencer')
                            else:
                                response_query = ' '.join(map(str, receive_postback[1:]))
                                type_query = 'down_video'
                                request_check['recent'] = response_query + type_query
                                with dataLock:
                                    print('======================================request check=====================================')
                                    print(request_check)
                                    print('======================================request check=====================================')
                                    if (request_check['previous'] != request_check['recent']):
                                        send_message(recipient_id, 'Please, veuillez patientez🙏🙏\n\nTélechargement en cours📫')
                                        audio_path = download_video(receive_postback[1])
                                        upload_file_filedata(recipient_id, audio_path)
                                        send_message(recipient_id, 'Profiter bien')

                                atexit.register(interrupt)
                                atexit.unregister
                                yourThread = threading.Timer(POOL_TIME, timeout(), ())
                                yourThread.start()
                                request_check['previous'] = request_check['recent']
                                request_check['recent'] = ''
                                print('=============================== verify ==============================')
                                print(request_check)
                                print('=============================== verify ==============================')
    return 'success'



def interrupt():
    global yourThread
    yourThread.cancel()


def timeout():
    return 'temps écouler'


def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!",
                        "We're greatful to know you :)"]
    return random.choice(sample_responses)


def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return "success"


def upload_video_fb(recipient_id, audio_url):
    payload ={
    "recipient":{
      "id":recipient_id
    },
    "message":{
    "attachment":{
      "type":"file",
        "payload":{
            "url": audio_url,
            "is_reusable":"True"
        }
        }
    }}
    reponse = requests.post("https://graph.facebook.com/v7.0/me/messages",
    params={"access_token": ACCESS_TOKEN},
    headers = {"Content-Type": "application/json"},
    json=payload)

    response = json.loads(reponse.text)
    print(response)


def upload_audio_fb(recipient_id, audio_url):
    payload ={ 
    "recipient":{
      "id":recipient_id
    },
    "message":{
    "attachment":{
      "type":"audio", 
        "payload":{
            "url": audio_url,
            "is_reusable":"True"
        }
        }
    }}
    reponse = requests.post("https://graph.facebook.com/v7.0/me/message_attachments",
    params={"access_token": ACCESS_TOKEN},
    headers = {"Content-Type": "application/json"},
    json=payload)
    rep = json.loads(reponse.text)
    print(rep)
    return rep.get('attachment_id')

#    #upload_audio_attachements(recipient_id, videme.Response()['message'].get('attachment_id'))
# def send_message_video(recipien_id, response):
#     bot.send_video(recipien_id, response)
#     return "success"
def upload_audio_attachements(recipient_id, attachment_id):
    payload = {
    "recipient":{
      "id":recipient_id
    },
    "message":{
    "attachment":{
      "type":"audio", 
      "payload":{"attachment_id": attachment_id}
        }
    }}
    reponse = requests.post("https://graph.facebook.com/v7.0/me/messages",
    params={"access_token": ACCESS_TOKEN},
    headers = {"Content-Type": "application/json"},
    json=payload)
    print(reponse)

def upload_audio_filedata(recipient_id,path):
    params = {
        "access_token": ACCESS_TOKEN
    }
    print(os.getcwd())
    data = {
        # encode nested json to avoid errors during multipart encoding process
        'recipient': json.dumps({
            'id': recipient_id
        }),
        # encode nested json to avoid errors during multipart encoding process
        'message': json.dumps({
            'attachment': {
                'type': 'audio',
                'payload': {}
            }
        }),
        'filedata': (os.path.basename(path), open(path, 'rb'), 'audio/mp3')
    }

    # multipart encode the entire payload
    multipart_data = MultipartEncoder(data)

    # multipart header from multipart_data
    multipart_header = {
        'Content-Type': multipart_data.content_type
    }

    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=multipart_header,data=multipart_data)

def upload_file_filedata(recipient_id,path):
    params = {
        "access_token": ACCESS_TOKEN
    }
    print(os.getcwd())
    data = {
        # encode nested json to avoid errors during multipart encoding process
        'recipient': json.dumps({
            'id': recipient_id
        }),
        # encode nested json to avoid errors during multipart encoding process
        'message': json.dumps({
            'attachment': {
                'type': 'file',
                'payload': {}
            }
        }),
        'filedata': (os.path.basename(path), open(path, 'rb'), 'image/png')
    }

    # multipart encode the entire payload
    multipart_data = MultipartEncoder(data)

    # multipart header from multipart_data
    multipart_header = {
        'Content-Type': multipart_data.content_type
    }

    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=multipart_header,data=multipart_data)

def upload_img_filedata(recipient_id, path):
    params = {
        "access_token": ACCESS_TOKEN
    }
    print(os.getcwd())
    data = {
        # encode nested json to avoid errors during multipart encoding process
        'recipient': json.dumps({
            'id': recipient_id
        }),
        # encode nested json to avoid errors during multipart encoding process
        'message': json.dumps({
            'attachment': {
                'type': 'image',
                'payload': {}
            }
        }),
        'filedata': (os.path.basename(path), open(path, 'rb'), 'image/png')
    }

    # multipart encode the entire payload
    multipart_data = MultipartEncoder(data)

    # multipart header from multipart_data
    multipart_header = {
        'Content-Type': multipart_data.content_type
    }

    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=multipart_header,
                      data=multipart_data)

def send_generic_template_google(recipient_id, research_query):
    url = "https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN
    results = scrape_google(research_query, 10, "en")
    payload = []
    for result in results:
        title = result["title"].encode()
        link = result["link"].encode()
        desc = result["description"].encode()
        payload.append({
            "title": title.decode(),
            "image_url": "https://www.presse-citron.net/wordpress_prod/wp-content/uploads/2020/05/Section-Google.jpg",
            "subtitle": desc.decode(),
            "default_action": {
                "type": "web_url",
                "url": link.decode(),
                "webview_height_ratio": "tall",
            },
            "buttons": [
                {
                    "type": "postback",
                    "title": "PDF view",
                    "payload": "PDF_view {}".format(link.decode())
                },
                {
                    "type": "postback",
                    "title": "Image view",
                    "payload": "IMAGE_view {}".format(link.decode())
                }
            ]
        })
    extra_data = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": payload
            }
        }
    }

    data = {
        'recipient': {'id': recipient_id},
        'message': {
            "attachment": extra_data["attachment"]
        }
    }
    resp = requests.post(url, headers={"Content-Type": "application/json"}, json=data)
    return "success"

def send_generic_template_youtube(recipient_id, research_query):
    url = "https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN
    results = scrape_youtube(research_query)

    payload = []
    for result in results['search_result']:
        payload.append({
            "title": result["title"],
            "image_url": result['thumbnails'][2],
            "subtitle": "Nombre de vue {} | Durée {} | Chaine {}".format(result["views"], result["duration"],
                                                                         result["channel"]),
            "default_action": {
                "type": "web_url",
                "url": result["link"],
                "webview_height_ratio": "tall",
            },
            "buttons": [
                {
                    "type": "postback",
                    "title": "Download",
                    "payload": "Down_youtube {}".format(result["link"])
                },
                {
                    "type": "postback",
                    "title": "Ecouter Ici",
                    "payload": "viewaudio {}".format(result["link"])
                },
                {
                    "type": "postback",
                    "title": "Regarder Ici",
                    "payload": "viewvideo {}".format(result["link"])
                },


            ]
        })
    extra_data = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": payload
            }
        }
    }

    data = {
        'recipient': {'id': recipient_id},
        'message': {
            "attachment": extra_data["attachment"]
        }
    }
    resp = requests.post(url, headers={"Content-Type": "application/json"}, json=data)
    postback_data = request.get_json()
    return "success"
def send_generic_template_download_youtube(recipient_id, link):
    url = "https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN
    payload = []
    payload.append({
        "title": "TELECHARGEMENT",
        "image_url": "https://www.prodrivers.ie/wp-content/uploads/dowload.gif",
        "subtitle": "Veuillez choisir une option Video | Audio",
        "buttons": [
            {
                "type": "postback",
                "title": "Video",
                "payload": "video_download {}".format(link)
            },
            {
                "type": "postback",
                "title": "Audio",
                "payload": "audio_download {}".format(link)
            }
        ]
    })
    extra_data = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": payload
            }
        }
    }

    data = {
        'recipient': {'id': recipient_id},
        'message': {
            "attachment": extra_data["attachment"]
        }
    }
    resp = requests.post(url, headers={"Content-Type": "application/json"}, json=data)
    postback_data = request.get_json()
    return "success"

def send_BM(recipient_id, response_sent_text, element):
    bot.send_button_message(recipient_id, response_sent_text, element)
    return "success"



if __name__ == "__main__":
    app.run()
