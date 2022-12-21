import requests
from bs4 import BeautifulSoup
from mastodon import Mastodon


## Mastodon API config
token = ""
instance = ""

## Get info
url = "https://www.embalses.net/"

response = requests.request(method = "GET", url = url)
if response.status_code != 200:
    print("Error: " + response.content)
    exit(-1)

soup = BeautifulSoup(response.content, "html.parser")

text = soup.find(property="og:description")['content']
img  = soup.find(property="og:image")['content']

# Download image

response = requests.get(img)
if response.status_code:
    fp = open("image1.png", "wb")
    fp.write(response.content)
    fp.close()


# Upload image to Mastodon

mastodon = Mastodon(api_base_url=instance, access_token=token)
media = mastodon.media_post("image1.png", description="Estado de los embalses")
img_id = media["id"]

# Post update

mastodon.status_post(text, media_ids=[img_id])
