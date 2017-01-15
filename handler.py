import requests
import json

from services import create_new_image

def receive_message(event, token):
	sender_id = event['sender']['id']
	message = event['message']
	
	handler_message(message, sender_id, token)

def handler_message(message, sender_id, token):
	attachments = message.get("attachments", [])

	if attachments:
		load_attachments(attachments, sender_id, token)
	else:
		message = text_message(sender_id, "echo : " + message['text'])
		call_send_API(message, token)

def load_attachments(attachments, sender_id, token):
	for attachment in attachments:
		if attachment['type'] == "image":
			payload = attachment["payload"]
			url = payload["url"]

			print url

			new_url = create_new_image(url)
			message = image_message(sender_id, new_url)
			call_send_API(message, token)


def text_message(recipient_id, message_text):
	message_data = {
		'recipient': {'id': recipient_id},
		'message': { 'text': message_text}
	}
	return message_data

def image_message(recipient_id, url):
  message_data = {
      "recipient":{ "id":recipient_id},
      "message":{
      "attachment":{
          "type":"image",
              "payload":{
                  "url":url
              }
          }
	}
  }   
  return message_data

def call_send_API(data, token):
  res = requests.post('https://graph.facebook.com/v2.6/me/messages',
						params={ 'access_token': token},
						data= json.dumps( data ),
						headers={'Content-type': 'application/json'})

  if res.status_code == 200:
		print "Mensaje enviado exitosamente!"	