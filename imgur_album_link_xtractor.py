from imgurpython import ImgurClient
import os

client_id     = os.environ["imgr_id"]
client_secret = os.environ["imgr_secret"]

def get_links(ID):
    client = ImgurClient(client_id, client_secret)
    lis = []
    try:
        for image in client.get_album_images(ID):
            data = ("{}\n".format(image.link))
            lis.append(data)
        return lis

    except imgurpython.helpers.error.ImgurClientError:
        return ["Error"]
