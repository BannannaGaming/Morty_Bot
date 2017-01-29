from imgurpython import ImgurClient
from imgurpython import helpers  # For error handling
import os

client_id     = os.environ["imgr_id"]
client_secret = os.environ["imgr_secret"]

async def get_links(ID):
    client = ImgurClient(client_id, client_secret)
    lis = []
    try:
        for image in client.get_album_images(ID):
            data = ("{}\n".format(image.link))
            lis.append(data)
        return lis

    except helpers.error.ImgurClientError:
        return ["Error"]
