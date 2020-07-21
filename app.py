import random
from flask import Flask, request
from pymessenger.bot import Bot
import requests
from scrapping import scrape_google, scrape_youtube
import abc
import logging
import hashlib
import hmac
import six
import requests


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
    # https://developers.facebook.com/docs/messenger-platform/send-messages#messaging_types
MESSAGING_TYPES = {
    'RESPONSE',
    'UPDATE',
    'MESSAGE_TAG',
}

# https://developers.facebook.com/docs/messenger-platform/reference/send-api/#payload
NOTIFICATION_TYPES = {
    'REGULAR',
    'SILENT_PUSH',
    'NO_PUSH'
}
DEFAULT_API_VERSION = 2.6
__version__ = '6.0.0'

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
                            video = Video(url='http://example.com/video.mp4')
                            send(video.to_dict(),recipient_id, 'RESPONSE')
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

def send_message_youtube_url(self, recipient_id, video_url):
    '''Send file to the specified recipient.
    https://developers.facebook.com/docs/messenger-platform/send-api-reference/file-attachment
    Input:
        recipient_id: recipient id to send to
        file_path: path to file to be sent
    Output:
        Response from API as <dict>
    '''
    payload = {
        'recipient': json.dumps(
            {
                'id': recipient_id
            }
        ),
        'message': json.dumps(
            {
                'attachment': {
                    'type': 'template',
                    'payload': {
                        "template_type":"media",
                        "elements":[{
                        "media_type":"video",
                        "url":video_url
                        }]
                    }
                }
            }
        )
    }
    multipart_data = MultipartEncoder(payload)
    multipart_header = {
        'Content-Type': multipart_data.content_type
    }
    return requests.post(self.base_url, data=multipart_data, headers=multipart_header).json()
def send_video_url(self, recipient_id, video_url):
    payload = {
            'recipient': json.dumps(
                {
                    'id': recipient_id
                }
            ),
            'message': json.dumps(
                {
                    'attachment': {
                        'type': 'template',
                        'payload': {
                            'template_type': 'media',
                            'elements':[
                                {
                                "media_type":"video",
                                "url":video_url
                                }
                            ]
                        }
                    }
                }
            )
        }
    return self.send_raw(payload)
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

session = requests.Session()
api_version = DEFAULT_API_VERSION
graph_url = 'https://graph.facebook.com/v{api_version}'.format(api_version=api_version)

class BaseMessenger(object):
    __metaclass__ = abc.ABCMeta

    last_message = {}
    @abc.abstractmethod
    def message(self, message):
        """Method to handle `messages`"""
    @abc.abstractmethod
    def postback(self, message):
        """Method to handle `messaging_postbacks`"""

    def handle(self, payload):
        for entry in payload['entry']:
            for message in entry['messaging']:
                self.last_message = message
                if message.get('message'):
                    return self.message(message)
                elif message.get('postback'):
                    return self.postback(message)

    def send(self, payload, messaging_type='RESPONSE', notification_type='REGULAR', timeout=None, tag=None):
        return self.client.send(payload, self.get_user_id(), messaging_type=messaging_type,
                                notification_type=notification_type, timeout=timeout, tag=tag)

    def upload_attachment(self, attachment, timeout=None):
        return self.client.upload_attachment(attachment, timeout=timeout)

class Messenger(BaseMessenger): 
    def message(self, message):
        action = process_message(message)
        res = self.send(action, 'RESPONSE')
    def init_bot(self):
        self.add_whitelisted_domains('https://facebook.com/')
        greeting = GreetingText(text='Welcome to the fbmessenger bot demo.')
        self.set_messenger_profile(greeting.to_dict())

        get_started = GetStartedButton(payload='start')
        self.set_messenger_profile(get_started.to_dict())

        menu_item_1 = PersistentMenuItem(
            item_type='postback',
            title='Help',
            payload='help',
        )
        menu_item_2 = PersistentMenuItem(
            item_type='web_url',
            title='Messenger Docs',
            url='https://developers.facebook.com/docs/messenger-platform',
        )
        persistent_menu = PersistentMenu(menu_items=[
            menu_item_1,
            menu_item_2
        ])
        res = self.set_messenger_profile(persistent_menu.to_dict())
        app.logger.debug('Response: {}'.format(res))
auth = {
        'access_token': ACCESS_TOKEN
        }
def process_message(message):

    if 'attachments' in message['message']:
        if message['message']['attachments'][0]['type'] == 'location':
            response = Text(text='{}: lat: {}, long: {}'.format(
                message['message']['attachments'][0]['title'],
                message['message']['attachments'][0]['payload']['coordinates']['lat'],
                message['message']['attachments'][0]['payload']['coordinates']['long']
            ))
            return response.to_dict()
        if 'image' in msg:
            response = Image(url='https://unsplash.it/300/200/?random')
        if 'video' in msg:
            response = Video(url='http://techslides.com/demos/sample-videos/small.mp4')
        return response.to_dict()

def send(self, payload, recipient_id, messaging_type='RESPONSE', notification_type='REGULAR',
         timeout=None, tag=None):
    if messaging_type not in MESSAGING_TYPES:
        raise ValueError('`{}` is not a valid `messaging_type`'.format(messaging_type))

    if notification_type not in NOTIFICATION_TYPES:
        raise ValueError('`{}` is not a valid `notification_type`'.format(notification_type))

    body = {
        'messaging_type': messaging_type,
        'notification_type': notification_type,
        'recipient': {
            'id': recipient_id,
        },
        'message': payload,
    }

    if tag:
        body['tag'] = tag

    r = session.post(
        '{graph_url}/me/messages'.format(graph_url=graph_url),
        params=auth,
        json=body,
        timeout=timeout
    )
    return r.json()
def upload_attachment(self, attachment, timeout=None):
    if not attachment.url:
        raise ValueError('Attachment must have `url` specified')
    if attachment.quick_replies:
        raise ValueError('Attachment may not have `quick_replies`')
    r = session.post(
        '{graph_url}/me/message_attachments'.format(graph_url=graph_url),
        params=auth,
        json={
            'message':  attachment.to_dict()
        },
        timeout=timeout
    )
    return r.json()

class BaseAttachment(object):
    def __init__(self, attachment_type, url=None, is_reusable=None,
                 attachment_id=None):
        self.attachment_type = attachment_type
        self.url = url
        self.is_reusable = is_reusable
        self.attachment_id = attachment_id

    def to_dict(self):
        d = {
            'attachment': {
                'type': self.attachment_type,
                'payload': {}
            }
        }

        if self.url:
            d['attachment']['payload']['url'] = self.url

        if self.is_reusable:
            d['attachment']['payload']['is_reusable'] = 'true'

        if self.attachment_id:
            d['attachment']['payload']['attachment_id'] = self.attachment_id

        return d


class Image(BaseAttachment):
    def __init__(self, url=None, is_reusable=None, attachment_id=None):
        self.attachment_type = 'image'
        self.url = url
        self.is_reusable = is_reusable
        self.attachment_id = attachment_id
        super(Image, self).__init__(self.attachment_type, self.url, self.is_reusable,
                                    self.attachment_id)


class Audio(BaseAttachment):
    def __init__(self, url=None, is_reusable=None, attachment_id=None):
        self.attachment_type = 'audio'
        self.url = url
        self.is_reusable = is_reusable
        self.attachment_id = attachment_id
        super(Audio, self).__init__(self.attachment_type, self.url, self.is_reusable,
                                    self.attachment_id)


class Video(BaseAttachment):
    def __init__(self, url=None, is_reusable=None, attachment_id=None):
        self.attachment_type = 'video'
        self.url = url
        self.is_reusable = is_reusable
        self.attachment_id = attachment_id
        super(Video, self).__init__(self.attachment_type, self.url, self.is_reusable,
                                    self.attachment_id)


class File(BaseAttachment):
    def __init__(self, url=None, is_reusable=None, attachment_id=None):
        self.attachment_type = 'file'
        self.url = url
        self.is_reusable = is_reusable
        self.attachment_id = attachment_id
        super(File, self).__init__(self.attachment_type, self.url, self.is_reusable,
                                   self.attachment_id)

def send_BM(recipient_id, response_sent_text,element):
    bot.send_button_message(recipient_id, response_sent_text,element)
    return "success"

if __name__ == "__main__":
    app.run()