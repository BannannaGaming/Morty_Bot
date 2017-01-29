from imgurpython import ImgurClient

client_id     = os.environ["imgr_id"]
client_secret = os.environ["imgr_secret"]

def get_links(ID):
    client = ImgurClient(client_id, client_secret)
    lis = []
    for image in client.get_album_images(ID):
        image_title = image.title if image.title else "Untitled"
        data = ("{} | Title:{}\n".format(image.link, image_title))
        lis.append(data)
    return lis
