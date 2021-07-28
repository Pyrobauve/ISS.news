from instabot import Bot
import os
import json
import urllib.request
from PIL import Image 
from PIL import ImageFont
from PIL import ImageDraw
from staticmap import StaticMap, CircleMarker
import config

bot = Bot()
bot.login(username = config.LOGIN, password = config.PASSWORD)

url_people = "http://api.open-notify.org/astros.json"
url_pos = "http://api.open-notify.org/iss-now.json"
data_people = urllib.request.urlopen(url_people)
data_pos = urllib.request.urlopen(url_pos)
resultat_people = json.loads(data_people.read())

resultat_pos = json.loads(data_pos.read())
number_people = resultat_people['number']
people_in = resultat_people['people']

pos_ISS = resultat_pos['iss_position']
lat = str(pos_ISS['latitude'])
lon = str(pos_ISS['longitude'])

m = StaticMap(250, 250, url_template='http://a.tile.osm.org/{z}/{x}/{y}.png')


coordinate = [float(lon), float(lat)]
marker_outline = CircleMarker((coordinate), 'white', 18)
marker = CircleMarker((coordinate), '#0036FF', 12)

m.add_marker(marker_outline)
m.add_marker(marker)

image = m.render(zoom=3)
image.save('marker.png')

font = ImageFont.truetype("font/times-ro.ttf", 24)
img = Image.new('RGB', (500, 500), color = (184,184,184))

draw = ImageDraw.Draw(img)

draw.rectangle((230, 67, 12, 488), outline=(57, 122, 0)) #rectangle peoples
draw.rectangle((230, 9, 12, 37), outline=(0, 0, 0)) #rectangle "number of people"
draw.rectangle((60, 67, 12, 45), outline=(57, 122, 0)) #rectangle "list"
draw.rectangle((305, 9, 400, 40), outline=(0, 0, 0)) #rectangle "position"
draw.rectangle((255, 40, 473, 100), outline=(0, 0, 0)) #rectangle latitude and longitude
draw.rectangle((320, 194, 385, 167), outline=(0, 0, 0)) # rectangle "Maps"
draw.rectangle((236, 453, 493, 194), outline=(0, 0, 0)) # rectangle map

a = 80
for p in people_in:
	draw.text((15, a),f"{p['name']}",(0,0,0),font=font)
	a = a + 25

draw.text((15, 20),"Number of people:",(0,0,0),font=font)
draw.text((199, 21),f"{number_people}",(255,0,0),font=font)
draw.text((15, 55),"List:",(57,122,0),font=font)
draw.text((332, 178),"Map",(0,0,0),font=font)
draw.text((313, 20),"Position",(0,0,0),font=font)
draw.text((260, 55),"Latitude:",(0,0,0),font=font)
draw.text((350, 55),f"{lat}",(255,0,0),font=font)
draw.text((260, 80),"Longitude:",(0,0,0),font=font)
draw.text((370, 80),f"{lon}",(255,0,0),font=font)

img.save('picture.png')

im1 = Image.open('marker.png')
im2 = Image.open('picture.png')

back_im = im2.copy()
back_im.paste(im1, (240, 200))
back_im.save('final.jpg', quality=95)

os.system("rm picture.png && rm marker.png")

bot.upload_photo("final.jpg")

os.system("rm -rf config && rm final.jpg.REMOVE_ME")
