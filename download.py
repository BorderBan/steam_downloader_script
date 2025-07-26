import requests
from urllib.parse import urlparse, parse_qs
import os
from time import sleep
import sys

def download(pairs: list) -> None:
    """Usage: [(appid1, contentid1), (appid2, contentid2), ...]"""
    download_list = ""
    for pair in pairs:
        if not (isinstance(pair, tuple) and len(pair) == 2):
            raise ValueError("Each item must be a tuple (appid, contentid)")
        appid, contentid = pair
        download_list += f"+workshop_download_item {appid} {contentid}"
    os.system(f"steamcmd +login anonymous {download_list} +quit")

def fetch_contentid(url: str) -> int:
    if not isinstance(url, str):
        raise TypeError("url must be str")
    parsed_url = urlparse(url)
    return int(parse_qs(parsed_url.query)["id"][0])

def fetch_appid(contentid: int) -> int:
    if not isinstance(contentid, int):
        raise TypeError("contentid must be int")
    response = requests.post(
        "https://api.steampowered.com/ISteamRemoteStorage/GetPublishedFileDetails/v1/",
        data={'itemcount': '1', 'publishedfileids[0]': contentid}
    )
    return response.json()['response']['publishedfiledetails'][0]['consumer_app_id']

if __name__ == "__main__":
    urls = []
    while 1:
        url_input = input("url(s):")
        if len(url_input) == 0:
            break
        else:
            urls.append(url_input)
    if len(urls) == 0:
        sys.exit()
    pairs = []
    for url in urls:
        contentid = fetch_contentid(url)
        appid = fetch_appid(contentid)
        pairs.append((appid, contentid))
