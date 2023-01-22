import requests
from urllib.parse import urlparse
import os
from time import sleep

url = "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"

args = int(urlparse(input('url: ')).query[3:])
r = requests.post(url, data={'itemcount': '1', 'publishedfileids[0]': args}).content.decode("utf-8")
r = eval(r)
appid = r['response']['publishedfiledetails'][0]['consumer_app_id']
contentid = r['response']['publishedfiledetails'][0]['publishedfileid']
os.system(f"steamcmd +login anonymous +workshop_download_item {appid} {contentid} +quit")
sleep(10)

