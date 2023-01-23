import requests
from urllib.parse import urlparse
import os
from time import sleep

url = "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/"

download = ""
num = 1
print('if you done with pasting urls, leave empty')
while 1:
    args = urlparse(input(f'url number {num}: ')).query[3:]
    if args != "":
        args = int(args)
        
        r = requests.post(url, data={'itemcount': '1', 'publishedfileids[0]': args}).content.decode("utf-8")
        r = eval(r)
        
        appid = r['response']['publishedfiledetails'][0]['consumer_app_id']
        contentid = r['response']['publishedfiledetails'][0]['publishedfileid']
        
        download += f"+workshop_download_item {appid} {contentid} "
        num += 1
    else:
        break


os.system(f"steamcmd +login anonymous {download}+quit")
sleep(10)
