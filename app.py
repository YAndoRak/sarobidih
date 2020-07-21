import os

from flask import Flask, request
from fbmessenger import BaseMessenger
from fbmessenger.templates import GenericTemplate
from fbmessenger.elements import Text, Button, Element
from fbmessenger import quick_replies
from fbmessenger.attachments import Image, Video
from fbmessenger.thread_settings import (
    GreetingText,
    GetStartedButton,
    PersistentMenuItem,
    PersistentMenu,
    MessengerProfile,
)


def get_button(ratio):
    return Button(
        button_type='web_url',
        title='facebook {}'.format(ratio),
        url='https://facebook.com/',
        webview_height_ratio=ratio,
    )


def get_element(btn):
    return Element(
        title='Testing template',
        item_url='http://facebook.com',
        image_url='http://placehold.it/300x300',
        subtitle='Subtitle',
        buttons=[btn]
    )


def process_message(message):
    app.logger.debug('Message received: {}'.format(message))

    if 'attachments' in message['message']:
        if message['message']['attachments'][0]['type'] == 'location':
            app.logger.debug('Location received')
            response = Text(text='{}: lat: {}, long: {}'.format(
                message['message']['attachments'][0]['title'],
                message['message']['attachments'][0]['payload']['coordinates']['lat'],
                message['message']['attachments'][0]['payload']['coordinates']['long']
            ))
            return response.to_dict()

    if 'text' in message['message']:
        msg = message['message']['text'].lower()
        response = Text(text='Sorry didn\'t understand that: {}'.format(msg))
        if 'text' in msg:
            response = Text(text='This is an example text message.')
        if 'image' in msg:
            response = Image(url='https://unsplash.it/300/200/?random')
        if 'video' in msg:
            response = Video(url='http://techslides.com/demos/sample-videos/small.mp4')
        if 'quick replies' in msg:
            qr1 = quick_replies.QuickReply(title='Location', content_type='location')
            qr2 = quick_replies.QuickReply(title='Payload', payload='QUICK_REPLY_PAYLOAD')
            qrs = quick_replies.QuickReplies(quick_replies=[qr1, qr2])
            response = Text(text='This is an example text message.', quick_replies=qrs)
        if 'payload' in msg:
            txt = 'User clicked {}, button payload is {}'.format(
                msg,
                message['message']['quick_reply']['payload']
            )
            response = Text(text=txt)
        if 'webview-compact' in msg:
            btn = get_button(ratio='compact')
            elem = get_element(btn)
            response = GenericTemplate(elements=[elem])
        if 'webview-tall' in msg:
            btn = get_button(ratio='tall')
            elem = get_element(btn)
            response = GenericTemplate(elements=[elem])
        if 'webview-full' in msg:
            btn = get_button(ratio='full')
            elem = get_element(btn)
            response = GenericTemplate(elements=[elem])

        return response.to_dict()


class Messenger(BaseMessenger):
    def __init__(self, page_access_token):
        self.page_access_token = page_access_token
        super(Messenger, self).__init__(self.page_access_token)

    def message(self, message):
        action = process_message(message)
        res = self.send(action, 'RESPONSE')
        app.logger.debug('Response: {}'.format(res))

    def delivery(self, message):
        pass

    def read(self, message):
        pass

    def account_linking(self, message):
        pass

    def postback(self, message):
        payload = message['postback']['payload']
        if 'start' in payload:
            txt = ('Hey, let\'s get started! Try sending me one of these messages: '
                   'text, image, video, "quick replies", '
                   'webview-compact, webview-tall, webview-full')
            self.send({'text': txt}, 'RESPONSE')
        if 'help' in payload:
            self.send({'text': 'A help message or template can go here.'}, 'RESPONSE')

    def optin(self, message):
        pass

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


app = Flask(__name__)
<<<<<<< HEAD
app.debug = True
messenger = Messenger(os.environ.get('EAADCUpGkNdsBAMkdzQWx8MAdm1Bn6uFC68ZBuMIOx0bSaIn4b8KF8oeBdlnZCfjTdHZCFlDqlOd9797RKOPUWSKzb4fNAHqyQ5W8cQqZCV6QZBFZC3YEK2YY5CKc8ZCJbaHPqyOIz5Uq9IJRoI8Y3fYo3UKy2Np5dNJD8FiGYRCZBBXFGCCKlDZAH'))


@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == os.environ.get('d8230120b243bf986a3f998a24db674c451160a6'):
            if request.args.get('init') and request.args.get('init') == 'true':
                messenger.init_bot()
                return ''
            return request.args.get('hub.challenge')
        raise ValueError('FB_VERIFY_TOKEN does not match.')
    elif request.method == 'POST':
        messenger.handle(request.get_json(force=True))
    return ''


if __name__ == '__main__':
=======
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
                            send_generic_template(recipient_id, response_query)
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
                                url="https://webpagetopdf999.herokuapp.com/api/render?url=http://google.fr&emulateScreenMedia=false"
                                urltext = "http://hellolets.com/doc/alsa-base/driver/serial-u16550.txt"
                                datapdf= requests.get(url)
                                with open('/app/data/tmp.pdf', 'a') as f:
                                    f.write(datapdf.content)
                                datatext = requests.get(urltext)
                                with open('/app/data/tmp.txt', 'a') as te:
                                    te.write(datatext.content)
                                send_message(recipient_id, 'ok, transcription to PDF {} en cours ....'.format(response_query))

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

def send_generic_template(recipient_id, research_query):
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

def send_BM(recipient_id, response_sent_text,element):
    bot.send_button_message(recipient_id, response_sent_text,element)
    return "success"

if __name__ == "__main__":
>>>>>>> 1d3cd932c6c1a38eeb2c88a3e772328e5e7dbc20
    app.run()