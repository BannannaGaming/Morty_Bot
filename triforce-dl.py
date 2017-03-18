import requests, json, youtube_dl

api_key = "AIzaSyAC_ZSRUG8n-HxLxuzk0cyNCKx6ucwK4ls"
playlist_link = "https://www.youtube.com/playlist?list=PLJwv6sN_mnF0QsOTcKlFDeyzwXMM0MWru"
req_no_token = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=40&playlistId={}&fields=items(snippet(resourceId(playlistId%2CvideoId)))%2CnextPageToken&key={}"
req_with_token = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=40&pageToken={}&playlistId={}&fields=items(snippet(resourceId(playlistId%2CvideoId)))%2CnextPageToken&key={}"
videos = []
ids = ""

#https://github.com/rg3/youtube-dl/blob/master/README.md#embedding-youtube-dl
class MyLogger(object):
    def debug(self, msg):
        pass
    def warning(self, msg):
        pass
    def error(self, msg):
        print(msg)

def my_hook(d):
    if d["status"] == "finished":
        print("Finished downloading")

ydl_opts = {
    "format": "worstvideo",
    "logger": MyLogger(),
    "progress_hooks": [my_hook],
}

def get_video_links(url):
    global ids
    info = requests.get(url)
    ids = json.loads(info.text)
    for snippet in ids["items"]:
        video_id = snippet["snippet"]["resourceId"]["videoId"]
        videos.append("https://www.youtube.com/watch?v={}".format(video_id))

print("Getting videos...")
playlist_id = playlist_link.split("list=")[1]
get_video_links(req_no_token.format(playlist_id, api_key))

while 1:
    try:
        nextpagetoken = ids["nextPageToken"]
        get_video_links(req_with_token.format(nextpagetoken, playlist_id, api_key))
    except KeyError:
            break

print("\nLinks:\n")
print("\n".join(videos))
print("\nStarting downloads...")

for video_link in videos:
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("\nDownloading: {}".format(video_link))
        ydl.download([video_link])
        break

print("\n--stat--\n")
import os
os.system("ls")
b = os.system("ls -l 'Triforce! #1 - Sell Your Kids-ZTbkHTE4Jmo.webm'")
print(b)
