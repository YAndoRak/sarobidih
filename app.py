import random
from flask import Flask, request
from pymessenger.bot import Bot
import requests
from scrapping import scrape_google, scrape_youtube



app = Flask(__name__)
ACCESS_TOKEN = 'EAAIiXXZBZBZAd8BAFIvOnSw5u7WIFkC5ZA7NSfCgSvziYhZBr3cUVlZBm4DZBiY4ZB0SYAT0ZBIXXJZCmBujX0OxZCiESbqZAw34xZC7KXT03DJZCpK0SxAi1nIJpN0AmU7LFd0rnNktcTW76XoqHxZAKPBV4ZCEEnRx5KYiFZC1hUSeINMSTKaZBYuNEil1P2'
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
          print(messaging)
          for message in messaging:
            if message.get('message'):
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    receive_message = message['message'].get('text').split()
                    print(receive_message)
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
                    print(receive_postback)
                    if receive_postback[0] == "PDF_view":
                        if len(receive_postback) < 2:
                            send_message(recipient_id, 'Veuillez réessayer la syntaxe exacte doit être PDF_view + lien_recherché')
                        else:
                            response_query = ' '.join(map(str, receive_postback[1:]))
                            send_message(recipient_id, 'ok, transcription to PDF {} en cours ....'.format(response_query))
                    if receive_postback[0] == "Download":
                        if len(receive_postback) < 2:
                            send_message(recipient_id, 'Veuillez réessayer la syntaxe exacte doit être PDF_view + lien_recherché')
                        else:
                            response_query = ' '.join(map(str, receive_postback[1:]))
                            send_message(recipient_id, 'ok, Teléchargement {} en cours ....'.format(response_query))
                    if receive_postback[0] == "View_here":
                        if len(receive_postback) < 2:
                            send_message(recipient_id, 'Veuillez réessayer la syntaxe exacte doit être PDF_view + lien_recherché')
                        else:
                            response_query = ' '.join(map(str, receive_postback[1:]))
                            #path = './DIR-PATH-HEREMaroon 5 - Memories (Official Video).mp4'
                            send_message(recipient_id, 'ok, envoye {} en cours ....'.format(response_query))
                            #send_video_url(recipient_id, 'http://techslides.com/demos/sample-videos/small.mp4')
                            #video = attachments.Video(url='http://example.com/video.mp4')
                            send_video_youtube(recipient_id)
                            send_message(recipient_id, 'Profiter bien')
    return "Message Processed"


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
    print(payload[0])
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
    print(postback_data)
    return "success"


def send_generic_template_youtube(recipient_id, research_query):
    url = "https://graph.facebook.com/v2.6/me/messages?access_token="+ACCESS_TOKEN
    results = scrape_youtube(research_query)

    payload = []
    print(results)
    for result in results['search_result']:
        payload.append({
            "title": result["title"],
            "image_url": result['thumbnails'][2],
            "subtitle": "Nombre de vue {} | Durée {} | Chaine {}".format(result["views"], result["duration"], result["channel"]),
            "default_action": {
                "type": "web_url",
                "url": result["link"],
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
                    "payload": "Download {}".format(result["link"])
                },
                {
                    "type": "postback",
                    "title": "Regarder Ici",
                    "payload": "View_here {}".format(result["link"])
                }
            ]
        })
    print(payload[0])
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
    print(postback_data)
    return "success"


def send_video_youtube(recipient_id):
    url = "https://graph.facebook.com/v2.6/me/messages?access_token="+ACCESS_TOKEN
    payload = [{
        'recipient': {'id': recipient_id},
        "message": {
           "attachment": {
               "type": "template",
               "payload": {
                   "template_type": "open_graph",
                   "elements": [
                       {
                           "url": "https://www.youtube.com/watch?v=eNuZNbeA9K8"
                       }
                   ]
               }
           }
       }}]
    resp = requests.post(url, json=payload)
    return "success"


def send_BM(recipient_id, response_sent_text,element):
    bot.send_button_message(recipient_id, response_sent_text,element)
    return "success"

if __name__ == "__main__":
    app.run()