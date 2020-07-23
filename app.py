import random
from flask import Flask, request
from pymessenger.bot import Bot
import requests
from scrapping import scrape_google, scrape_youtube
from fbmessenger import BaseMessenger
from fbmessenger.elements import Text
from fbmessenger.attachments import Image, Video
from youtube_dl import YoutubeDL

app = Flask(__name__)
ACCESS_TOKEN = 'EAAI1QygXjocBAHbkdNCVBv53GXvCm0IrgFUZAdZCJ5TdhKvyaAYnWx1XpycJCRnIrVAE81FgY0LG3ZAAHZA05E90U4zXX1ZCeYtZCW4pL2yTdgLRlb8omoRPIJPOwftvNQT4r3Gc1D0MpNe4ZBmyjvQsK8eZCejr80kZBWqy3H5yZCqUSMNFVCC6D6'
VERIFY_TOKEN = 'd8230120b243bf986a3f998a24db674c451160a6'
bot = Bot(ACCESS_TOKEN)
# elements =[{
#             "type":"web_url",
#             "url":"https://www.messenger.com",
#             "title":"Visit Messenger"
#           }]
elements2 =[{
  "type":"phone_number",
  "title":"Jao's phone",
  "payload":"+261329125857"
    }]

################ fb messenger #################"""
#
class Messenger(BaseMessenger):
    def __init__(self, page_access_token):
        self.page_access_token = page_access_token
        super(Messenger, self).__init__(self.page_access_token)

    def postback(self, message):
        payload = message['postback']['payload'].split()
        payload2 = payload[1]
        payload1 = payload[0]
        ####YOUTUBE DL#####
        #ydl = YoutubeDL()
        #url = "https://www.youtube.com/watch?v=Cfv7qHMeNS4"
        #r = ydl.extract_info(url, download=False)
        #payloadt = [format['url'] for format in r['formats']]
        #payloadtest= payloadt[0]
        #print(payloadtest)
        ###################
        if 'image' in payload1:
            response = Image(url=payload2)
        elif 'viewvideo' in payload1:
            response = Video(url=payload2)
        else : 
            response = Text(text='This is an example text message.')
        action = response.to_dict()
        self.send(action, 'RESPONSE')
        return "200 ok"

messenger = Messenger(ACCESS_TOKEN)
#We will receive messages that Facebook sends our bot at this endpoint 
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
                if message.get('message'):
                    recipient_id = message['sender']['id']
                    if message['message'].get('text'):
                        receive_message = message['message'].get('text').split()
                        if (receive_message[0] == "search_google"):
                            if len(receive_message) < 2:
                                send_message(recipient_id, 'Veuillez réessayer la syntaxe exacte doit être search_google + mot_recherché')
                            else:
                                response_query = ' '.join(map(str, receive_message[1:]))
                                send_message(recipient_id, 'ok, research google {} en cours ....'.format(response_query))
                                send_generic_template_google(recipient_id, response_query)
                        if (receive_message[0] == "search_youtube"):
                            if len(receive_message) < 2:
                                send_message(recipient_id, 'Veuillez réessayer la syntaxe exacte doit être search_youtube + mot_recherché')
                            else:
                                response_query = ' '.join(map(str, receive_message[1:]))
                                send_message(recipient_id, 'ok, research youtube {} en cours ....'.format(response_query))
                                send_generic_template_youtube(recipient_id, response_query)
                        else:
                            response_sent_text = get_message()
                            send_BM(recipient_id, response_sent_text,elements2)
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
                                send_message(recipient_id, 'Veuillez réessayer la syntaxe exacte doit être PDF_view + lien_recherché')
                            else:
                                response_query = ' '.join(map(str, receive_postback[1:]))
                                send_message(recipient_id, 'ok, transcription to PDF {} en cours ....'.format(response_query))
                        if receive_postback[0] == "image":
                            response_query = ' '.join(map(str, receive_postback[1:]))
                            send_message(recipient_id, 'ok, Teléchargement {} en cours ....'.format(response_query))
                            messenger.handle(request.get_json(force=True))
                            return "200 ok"
                        if receive_postback[0] == "viewvideo":
                            response_query = ' '.join(map(str, receive_postback[1:]))
                            send_message(recipient_id, 'ok, envoye {} en cours ....'.format(response_query))
                            messenger.handle(request.get_json(force=True))
                            send_message(recipient_id, 'Profiter bien')
                            return "200 ok"
    return "200 ok"


def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    return random.choice(sample_responses)

def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return "success"




# def send_message_video(recipien_id, response):
#     bot.send_video(recipien_id, response)
#     return "success"

def send_generic_template_google(recipient_id, research_query):
    url = "https://graph.facebook.com/v2.6/me/messages?access_token="+ACCESS_TOKEN
    results = scrape_google(research_query, 10, "en")
    payload = []
    for result in results:
        payload.append({
            "title": result["title"],
            "image_url": "https://www.presse-citron.net/wordpress_prod/wp-content/uploads/2020/05/Section-Google.jpg",
            "subtitle": result["description"],
            "default_action": {
                "type": "web_url",
                "url": result["link"],
                "webview_height_ratio": "tall",
            },
            "buttons": [
                {
                    "type": "web_url",
                    "url": result["link"],
                    "title": "View In Google"
                },
                {
                    "type": "postback",
                    "title": "PDF view",
                    "payload": "PDF_view {}".format(result["link"])
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
    resp = requests.post(url, json=data)
    postback_data = request.get_json()
    return "success"


def send_generic_template_youtube(recipient_id, research_query):
    url = "https://graph.facebook.com/v2.6/me/messages?access_token="+ACCESS_TOKEN
    results = scrape_youtube(research_query)

    payload = []
    for result in results['search_result']:
        payload.append({
            "title": result["title"],
            "image_url": result['thumbnails'][2],
            "subtitle": "Nombre de vue {} | Durée {} | Chaine {}".format(result["views"], result["duration"], result["channel"]),
            "default_action": {
                "type": "web_url",
                "url": "https://r4---sn-q0cedn7s.googlevideo.com/videoplayback?expire=1595464559&ei=D4cYX8nmBM2pxN8Pzvmx2A8&ip=54.154.4.19&id=o-AFM-BjtFyA8fupXQFLZ9JH9mRA7HxwBzr5iH4gqMsfpF&itag=249&source=youtube&requiressl=yes&mh=q1&mm=31%2C26&mn=sn-q0cedn7s%2Csn-4g5edn7y&ms=au%2Conr&mv=u&mvi=4&pl=22&vprv=1&mime=audio%2Fwebm&gir=yes&clen=1283583&dur=194.801&lmt=1595377258766667&mt=1595442728&fvip=4&keepalive=yes&fexp=23883097&beids=9466588&c=WEB&txp=5511222&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cgir%2Cclen%2Cdur%2Clmt&sig=AOq0QJ8wRQIgSDYtwvD4dznUwNz-Pi4NMwIo79KM-g52zC9KFmCro6QCIQDyE2DE4KV8BWT0PiYr8UqNwv-FcL2_1unzqdyMhCzT_g%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl&lsig=AG3C_xAwRQIhALY8uvc3MuYdcc27n4lA2BDaZaaxkp2kdEGpTtsfhrLxAiBTHbmU_9BHxMnXHg-_zYiFngNpRRvOgi0ABCUsk0WtBg%3D%3D&ratebypass=yes",
                "webview_height_ratio": "tall",
            },
            "buttons": [
                {
                    "type": "web_url",
                    "url": result["link"],
                    "title": "View In Youtube"
                },
                {
                    "type": "postback",
                    "title": "Télecharger",
                    "payload":"image https://unsplash.it/300/200/?random"
                },
                {
                    "type": "postback",
                    "title": "Regarder Ici",
                    "payload":"viewvideo https://brash-lime-enigmosaurus.glitch.me/myvideo.mp4"
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
    resp = requests.post(url, json=data)
    postback_data = request.get_json()
    return "success"




def send_BM(recipient_id, response_sent_text,element):
    bot.send_button_message(recipient_id, response_sent_text,element)
    return "successe"

if __name__ == "__main__":
    app.run()
