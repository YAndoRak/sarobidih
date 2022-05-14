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
from urltopdf import convert_url_img, convert_url_pdf
import os
from requests_toolbelt import MultipartEncoder
import threading
import youtube_dl



app = Flask(__name__)
ACCESS_TOKEN = 'EAAI1QygXjocBACztwQswUz5nv4mhvWhE1iES5syoKES3TRQWQxrcsSh7w8QiE2IEmfcA9bnxTWegpDrU7lDO3EkrmRvG8O8Q78D7S0J397BD1rA7OogDZCypwrTrW4GRdu0pRDzEod6sKQwx0TNTvAdexxvXM2iHpoViqWHV6mwvW2LFw'
VERIFY_TOKEN = 'd8230120b243bf986a3f998a24db674c451160a6'
bot = Bot(ACCESS_TOKEN)

################ fb messenger #################"""

#Reboot/rebuild variables#

pageId = "101187515018902"
RepoName = "YAndoRak/sarobidih"
appName = "sarobidih"
herokutoken = 'fb6b5077-c164-4aa3-bc43-217e7a5b577a'

##########################

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
		filesize = url_video["filesize"]
		payload2 = url_video['url']
		payload1 = payload[0]
		ytb_id = payload[1:]


		if 'viewvideo' in payload1:
			if filesize < 25690112:

				response = Video(url=payload2)
			else:
				response = Text(text="Messenger à bloqué votre video, parce qu'elle est trop volumineuse😞😞")
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
				if message.get('message'):
					recipient_id = message['sender']['id']
					if message['message'].get('text'):
						receive_message = message['message'].get('text').split()
						if (receive_message[0].upper() == "GG"):
							if len(receive_message) < 2:
								send_message(recipient_id,'Veuillez réessayer la syntaxe exacte doit être search_google + mot_recherché')
							else:
								try:
									response_query = ' '.join(map(str, receive_message[1:]))
									send_message(recipient_id,'ok, research google {} en cours ....'.format(response_query))
									send_generic_template_google(recipient_id, response_query)
								except Exception:
									send_message(recipient_id,
												 'Désolé, Une Erreur est survenue😪😪\n\nVeuillez Réssayer après 10 mn⏭️')

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
						elif (receive_message[0].upper() == "REBOOT6362"):
							rebootSys(recipient_id)
						elif (receive_message[0].upper() == "REBUILD6362"):
							rebuildSys(recipient_id)
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
								request_check['recent'] = response_query + type_query+"/"+ recipient_id
								try:
									with dataLock:
										print('======================================request check=====================================')
										print(request_check)
										print('======================================request check=====================================')
										if (request_check['previous'] != request_check['recent']):
											send_message(recipient_id, 'ok, Envoye {} en cours ....'.format(response_query))
											pdf_path = convert_url_pdf(receive_postback[1])
											upload_file_filedata(recipient_id, pdf_path)
											send_message(recipient_id, 'Profiter bien')
									yourThread = threading.Timer(POOL_TIME, timeout(), ())
									yourThread.start()
									request_check['previous'] = request_check['recent']
									request_check['recent'] = ''
									print('=============================== verify ==============================')
									print(request_check)
									print('=============================== verify ==============================')
								except Exception:
									send_message(recipient_id,
												 'Désolé, Une Erreur est survenue😪😪\n\nVeuillez Réssayer après 10 mn⏭️')
						elif receive_postback[0] == "IMAGE_view":
							if len(receive_postback) < 2:
								send_message(recipient_id,
											 'Veuillez réessayer la syntaxe exacte doit être PDF_view + lien_recherché')
							else:
								response_query = ' '.join(map(str, receive_postback[1:]))
								type_query = 'image'
								request_check['recent'] = response_query + type_query + recipient_id
								try:
									with dataLock:
										print('======================================request check=====================================')
										print(request_check)
										print('======================================request check=====================================')
										if (request_check['previous'] != request_check['recent']):
											send_message(recipient_id, 'ok, Envoye {} en cours ....'.format(response_query))
											image_path = convert_url_img(receive_postback[1])
											upload_img_filedata(recipient_id, image_path)
											send_message(recipient_id, 'Profiter bien')
									yourThread = threading.Timer(POOL_TIME, timeout(), ())
									yourThread.start()
									request_check['previous'] = request_check['recent']
									request_check['recent'] = ''
									print('=============================== verify ==============================')
									print(request_check)
									print('=============================== verify ==============================')
								except Exception:
									send_message(recipient_id,
												 'Désolé, Une Erreur est survenue😪😪\n\nVeuillez Réssayer après 10 mn⏭️')
						elif receive_postback[0] == "image":
							response_query = ' '.join(map(str, receive_postback[1:]))
							send_message(recipient_id, 'ok, Teléchargement {} en cours ....'.format(response_query))
							messenger.handle(request.get_json(force=True))
						elif receive_postback[0] == "viewaudio":
							response_query = ' '.join(map(str, receive_postback[1:]))
							type_query = 'audio'
							request_check['recent'] = response_query + type_query + recipient_id
							try:
								with dataLock:
									print('======================================request check=====================================')
									print(request_check)
									print('======================================request check=====================================')
									if (request_check['previous'] != request_check['recent']):
										send_message(recipient_id, 'Please, veuillez patientez🙏🙏\n\nenvoye en cours📫')
										check = find_ydl_url(receive_postback[1])
										filesize = check["filesize"]
										if filesize < 25690112:
											audio_path = download_audio(receive_postback[1])
											upload_audio_filedata(recipient_id, audio_path['output'])
											send_message(recipient_id, 'Profiter bien')
										else:
											ytb_id = receive_postback[1]
											send_message(recipient_id,
														 "Votre video ne pourra pas être diffuser sur messenger."
														 "Il sera donc diffusser sur notre page en tant que video\n\n"
														 "Un lien sera envoyre sous peu, veuillez patientez svp ⏭⏭")
											page_video(ytb_id[32:], recipient_id)
								yourThread = threading.Timer(POOL_TIME, timeout(), ())
								yourThread.start()
								request_check['previous'] = request_check['recent']
								request_check['recent'] = ''
								print('=============================== verify ==============================')
								print(request_check)
								print('=============================== verify ==============================')
								return 'start'
							except Exception:
								send_message(recipient_id, 'Désolé, Une Erreur est survenue😪😪\n\nVeuillez Réssayer après 10 mn⏭️')

						elif receive_postback[0] == "viewvideo":
							response_query = ' '.join(map(str, receive_postback[1:]))
							type_query = 'video'
							request_check['recent'] = response_query + type_query + recipient_id
							try:
								with dataLock:
									print('======================================request check=====================================')
									print(request_check)
									print('======================================request check=====================================')
									if (request_check['previous'] != request_check['recent']):
										send_message(recipient_id, 'Please, veuillez patientez🙏🙏\n\nenvoye en cours📫')
										#messenger.handle(request.get_json(force=True))
										check = find_ydl_url(receive_postback[1])
										filesize = check["filesize"]

										if filesize < 25690112:
											attacheID = upload_video_fb(recipient_id, check['url'])
											print(attacheID)
											upload_video_attachements(recipient_id, attacheID)
											send_message(recipient_id, 'Profiter bien')
										else:
											ytb_id = receive_postback[1]
											send_message(recipient_id,"Votre video ne pourra pas être diffuser sur messenger."
																	  "Il sera donc diffusser sur notre page en tant que video\n\n"
																	  "Un lien sera envoyre sous peu, veuillez patientez svp ⏭⏭")
											page_video(ytb_id[32:], recipient_id)

								yourThread = threading.Timer(POOL_TIME, timeout(), ())
								yourThread.start()
								request_check['previous'] = request_check['recent']
								request_check['recent'] = ''
								print('=============================== verify ==============================')
								print(request_check)
								print('=============================== verify ==============================')
								return 'start'
							except Exception:
								send_message(recipient_id,'Désolé, Une Erreur est survenue😪😪\n\nEssayer une autre video⏭️')
						elif receive_postback[0] == "Down_youtube":
							if len(receive_postback) < 2:
								send_message(recipient_id, 'Erreur veuillez recommencer')
							else:
								response_query = ' '.join(map(str, receive_postback[1:]))
								send_generic_template_download_youtube(recipient_id, response_query)
						elif receive_postback[0] == "audio_download":
							if len(receive_postback) < 2:
								send_message(recipient_id, 'Erreur veuillez recommencer')
							else:
								response_query = ' '.join(map(str, receive_postback[1:]))
								type_query = 'down_audio'
								request_check['recent'] = response_query + type_query + recipient_id
								try:
									with dataLock:
										print('======================================request check=====================================')
										print(request_check)
										print('======================================request check=====================================')
										if (request_check['previous'] != request_check['recent']):
											send_message(recipient_id, 'Please, veuillez patientez🙏🙏\n\nTélechargement en cours📫')
											check = find_ydl_url(receive_postback[1])
											filesize = check["filesize"]
											if filesize < 25690112:
												audio_path = download_audio(receive_postback[1])
												upload_file_filedata(recipient_id, audio_path['output'])
												send_message(recipient_id, 'Profiter bien')
											else:
												ytb_id = receive_postback[1]
												send_message(recipient_id,
															 "Votre video ne pourra pas être diffuser sur messenger."
															 "Il sera donc diffusser sur notre page en tant que video\n\n"
															 "Un lien sera envoyre sous peu, veuillez patientez svp ⏭⏭")
												page_video(ytb_id[32:], recipient_id)

									yourThread = threading.Timer(POOL_TIME, timeout(), ())
									yourThread.start()
									request_check['previous'] = request_check['recent']
									request_check['recent'] = ''
									print('=============================== verify ==============================')
									print(request_check)
									print('=============================== verify ==============================')
								except Exception:
									send_message(recipient_id,
												 'Désolé, Une Erreur est survenue😪😪\n\nVeuillez Réssayer après 10 mn⏭️')

						elif receive_postback[0] == "video_download":
							if len(receive_postback) < 2:
								send_message(recipient_id, 'Erreur veuillez recommencer')
							else:
								response_query = ' '.join(map(str, receive_postback[1:]))
								type_query = 'down_video'
								request_check['recent'] = response_query + type_query + recipient_id
								try:
									with dataLock:
										print('======================================request check=====================================')
										print(request_check)
										print('======================================request check=====================================')
										print("Eto zao ligne 319")
										if (request_check['previous'] != request_check['recent']):
											send_message(recipient_id, 'Please, veuillez patientez🙏🙏\n\nTélechargement en cours📫')
											check = find_ydl_url(receive_postback[1])
											filesize = check["filesize"]
											print("ETo zao filesize")
											if filesize < 25690112:
												print("eto filesize ok")
												audio_path = download_video(receive_postback[1])
												print(audio_path)
												upload_vid_filedata(recipient_id, audio_path)
												send_message(recipient_id, 'Profiter bien')
											else:
												ytb_id = receive_postback[1]
												send_message(recipient_id,
															 "Votre video ne pourra pas être diffuser sur messenger."
															 "Il sera donc diffusser sur notre page en tant que video\n\n"
															 "Un lien sera envoyre sous peu, veuillez patientez svp ⏭⏭")
												page_video(ytb_id[32:], recipient_id)
									yourThread = threading.Timer(POOL_TIME, timeout(), ())
									yourThread.start()
									request_check['previous'] = request_check['recent']
									request_check['recent'] = ''
									print('=============================== verify ==============================')
									print(request_check)
									print('=============================== verify ==============================')
								except Exception:
									print("Tsy mety")
									send_message(recipient_id,
												 'Désolé, Une Erreur est survenue😪😪\n\nVeuillez Réssayer après 10 mn⏭️')
	return 'success'







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


def upload_video_fb(recipient_id, video_url):
	payload ={
	"recipient":{
	  "id":recipient_id
	},
	"message":{
	"attachment":{
	  "type":"video",
		"payload":{
			"url": video_url,
			"is_reusable":"True"
		}
		}
	}}
	reponse = requests.post("https://graph.facebook.com/v9.0/me/messages",
	params={"access_token": ACCESS_TOKEN},
	headers = {"Content-Type": "application/json"},
	json=payload)
	response = json.loads(reponse.text)
	return response


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
	reponse = requests.post("https://graph.facebook.com/v9.0/me/message_attachments",
	params={"access_token": ACCESS_TOKEN},
	headers = {"Content-Type": "application/json"},
	json=payload)
	rep = json.loads(reponse.text)
	upload_audio_attachements(recipient_id, rep.get('attachment_id'))
	return 'ok', 200#rep.get('attachment_id')

#    #upload_audio_attachements(recipient_id, videme.Response()['message'].get('attachment_id'))
# def send_message_video(recipien_id, response):
#     bot.send_video(recipien_id, response)
#     return "success"


def page_video(ytbId, recipient_id):
	print("LE ytbID", ytbId)
	print("LE recipient_id", recipient_id)
	requests.get("https://nodemess.herokuapp.com/"+ytbId+"/"+recipient_id)
	return 'ok', 200


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
	reponse = requests.post("https://graph.facebook.com/v9.0/me/messages",
	params={"access_token": ACCESS_TOKEN},
	headers = {"Content-Type": "application/json"},
	json=payload)

def upload_video_attachements(recipient_id, attachment_id):
	payload = {
	"recipient":{
	  "id":recipient_id
	},
	"message":{
	"attachment":{
	  "type":"video", 
	  "payload":{"attachment_id": attachment_id}
		}
	}}
	reponse = requests.post("https://graph.facebook.com/v9.0/me/messages",
	params={"access_token": ACCESS_TOKEN},
	headers = {"Content-Type": "application/json"},
	json=payload)

def upload_audio_filedata(recipient_id,path):
	params = {
		"access_token": ACCESS_TOKEN
	}
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

	r = requests.post("https://graph.facebook.com/v9.0/me/messages", params=params, headers=multipart_header,data=multipart_data)
def upload_file_filedata(recipient_id,path):
	params = {
		"access_token": ACCESS_TOKEN
	}
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
		'filedata': (os.path.basename(path), open(path, 'rb'))
	}

	# multipart encode the entire payload
	multipart_data = MultipartEncoder(data)

	# multipart header from multipart_data
	multipart_header = {
		'Content-Type': multipart_data.content_type
	}

	r = requests.post("https://graph.facebook.com/v7.0/me/messages", params=params, headers=multipart_header,data=multipart_data)
	print("Le requete ligne",r)
def upload_img_filedata(recipient_id, path):
	params = {
		"access_token": ACCESS_TOKEN
	}
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

	r = requests.post("https://graph.facebook.com/v9.0/me/messages", params=params, headers=multipart_header,
					  data=multipart_data)

def upload_vid_filedata(recipient_id, path):
	params = {
		"access_token": ACCESS_TOKEN
	}
	data = {
		# encode nested json to avoid errors during multipart encoding process
		'recipient': json.dumps({
			'id': recipient_id
		}),
		# encode nested json to avoid errors during multipart encoding process
		'message': json.dumps({
			'attachment': {
				'type': 'video',
				'payload': {}
			}
		}),
		'filedata': (os.path.basename(path), open(path, 'rb'), 'video/mp4')
	}

	# multipart encode the entire payload
	multipart_data = MultipartEncoder(data)

	# multipart header from multipart_data
	multipart_header = {
		'Content-Type': multipart_data.content_type
	}

	r = requests.post("https://graph.facebook.com/v9.0/me/messages", params=params, headers=multipart_header,
					  data=multipart_data)




#For reboot/rebuild fbtoken, recipient_id, pageId, RepoName, appName, herokutoken
def rebuildSys(recipient_id):
	payload = {
	"fb":{
	  "userId":recipient_id,
	  "pageId":pageId,
	  "fbtoken":ACCESS_TOKEN
	},
	"heroku":{
		"repo":RepoName,
		"appName":appName,#botmessengerjao
		"herokutoken": herokutoken
	}}
	reponse = requests.post("https://rebootsystem.herokuapp.com/builds",
	headers = {"Content-Type": "application/json"},
	json=payload)
	reponse.close()
	return "success"

def rebootSys(recipient_id):
	payload = {
	"fb":{
	  "userId":recipient_id,
	  "pageId":pageId,
	  "fbtoken":ACCESS_TOKEN
	},
	"heroku":{
		"appName":appName,
		"herokutoken": herokutoken
	}}
	reponse = requests.post("https://rebootsystem.herokuapp.com/reboot",
	headers = {"Content-Type": "application/json"},
	json=payload)
	reponse.close()
	return "success"



def send_generic_template_google(recipient_id, research_query):
	url = "https://graph.facebook.com/v9.0/me/messages?access_token=" + ACCESS_TOKEN
	results = scrape_google(research_query, 10, "en")
	payload = []
	for result in results:
		title = result["title"].encode()
		link = result["link"].encode()
		print("Le lien : ", link)
		#desc = result["description"].encode('utf8')
		payload.append({
			"title": title.decode(),
			"image_url": "https://www.presse-citron.net/wordpress_prod/wp-content/uploads/2020/05/Section-Google.jpg",
			"subtitle": title.decode(),
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
	url = "https://graph.facebook.com/v9.0/me/messages?access_token=" + ACCESS_TOKEN
	results = scrape_youtube(research_query)


	payload = []
	for result in results['search_result']:
		payload.append({
			"title": result["title"],
			"image_url": result['thumbnails'][2],
			"subtitle": " Nombre de vue {} | Durée {} | Chaine {}".format(result["views"], result["duration"],
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
	url = "https://graph.facebook.com/v9.0/me/messages?access_token=" + ACCESS_TOKEN
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
				"title": "Video 2",
				"payload": "down_video {}".format(link)
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
