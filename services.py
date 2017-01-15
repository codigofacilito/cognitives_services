import os

CLIENT_ID = os.environ.get("IMGUR_CLIENT_ID")
CLIENT_SECRET = os.environ.get("IMGUR_CLIENT_SECRET")
MICROSOFT_KEY = os.environ.get("MICROSOFT_KEY")

ROOT_PATH = "images" #Path Relativo!

def new_path(path = "new"):
	import datetime
	return "{}/{}/{}.jpg".format(ROOT_PATH, path, datetime.datetime.now())

def get_emoji_path():
	return "{}/{}/{}".format(ROOT_PATH, "emojis", "emoji.png")

def download_image(url):
	import urllib

	path = new_path("downloads")
	image = open(path, "wb")
	image.write( urllib.urlopen( url ).read() )
	image.close()
	return path

def get_faces(url):
	import requests
	import json

	res = requests.post("https://api.projectoxford.ai/face/v1.0/detect",
		params = {"returnFaceId": "true", "returnFaceLandmarks": "false"},
		data =  json.dumps( {"url" : url }  ) ,
		headers = { "Content-Type": "application/json", "Ocp-Apim-Subscription-Key" : MICROSOFT_KEY })

	if res.status_code == 200:
		return [ face["faceRectangle"] for face in json.loads( res.text ) ]

def add_emoji(path = "", faces = []):
	from PIL import Image

	background = Image.open(path)
	foreground = Image.open(get_emoji_path())

	if faces:
		for face in faces:
			foreground_resize = foreground.resize(  (face["width"], face["height"]) )
			background.paste( foreground_resize, (face["left"], face["top"]), foreground_resize)

		path = new_path("news")
		background.save(path)
		return path


def upload_image(path = ""):
	from imgurpython import ImgurClient
	
	if path:
		client = ImgurClient(CLIENT_ID, CLIENT_SECRET)
		response = client.upload_from_path(path)
		return response["link"]


def create_new_image(url):
	new_path = download_image(url)
	new_path = add_emoji(new_path, get_faces(url))
	return upload_image(new_path)


if __name__ == "__main__":
	print create_new_image("https://scontent.xx.fbcdn.net/v/t34.0-12/16128206_215236158939081_1753194069_n.png?_nc_ad=z-m&oh=70f54f930dcb98ec40a780ac7be6d30d&oe=587E768C")

