# GAZR - Gazing Adaptive Zoom Robot
#
# Read chat from YouTube Live Stream and relay hashtags to  
#      Stellarium remote control and SlewTelescopeToSelectedObject 
# Contributing Insiders:
#      Robert Davies <robert.kris.davies@gmail.com>, Insider Discord
#      @johns67467 - Insider Discord
#      @We Have Fun - Kris - Insider Discord
#      @John Neiberger - Insider Discord

import re
import sys
import time
import pytchat
import logging
import datetime
import mechanize
import pandas as pd
import http.cookiejar as cookielib
import requests
from bs4 import BeautifulSoup
from settings import (
    s_login,
    s_password,
    stellarium_server,
    stellarium_port
)


def get_streamID():
    """ Get current Stream ID from the YouTube channel"""
    user_agent = [
        (
            "User-agent",
            "GAZR (X11;U;Linux MyKernelMyBusiness; Insider-Powered) Skinwalker/20221214-1 reapr.py",
        )
    ]

    cj = cookielib.CookieJar()
    br = mechanize.Browser()
    br.set_cookiejar(cj)
    br.set_handle_robots(False)
    br.addheaders = user_agent
    br.open("https://skinwalker-ranch.com/ranch-webcam-livestream/")

    br.select_form(name="mepr_loginform")
    br.form["log"] = s_login
    br.form["pwd"] = s_password
    br.submit()

    soup = BeautifulSoup(br.response().read(), features="html5lib")
    for item in soup.find_all("iframe"):
        if "embed" in item.get("src"):
            stream_url = item.get("src")
    """ 2023/1/23 -- strips true colors show up. I could have used ("htps:/wyoubecmlivha?=") """
    """ This makes it buggy if the streamID contains ANY of those letters. """
    #stream_ID = stream_url.strip("https://www.youtube.com/live_chat?v=")
    stream_ID = stream_url[36:]
    return stream_ID[:11]


def read_chat(YouTube_ID):
    """Monitor YouTube chat for new action messages"""
    chat = pytchat.create(video_id="https://www.youtube.com/watch?v=" + YouTube_ID)
    while chat.is_alive():
        for c in chat.get().sync_items():
            # Lets read all chat if we set logging to INFO
            logging.info(f"{c.datetime} [{c.author.name}]- {c.message}")
            yt_datetime = c.datetime
            yt_user = c.author.name
            yt_msg = c.message
            # See tag, label it ship it off
            tag_list = ["SKY", "ZOOMIN", "ZOOMOUT", "HOME"]
            tag = re.findall(
                r"^#(?=(" + "|".join(tag_list) + r"):)+", c.message.upper()
            )

            if tag:
                yt_tag = tag[0]
                if yt_tag in tag_list:
                    if c.author.isChatModerator or c.author.isChatOwner:
                        print(f"CAM: {c.message}")
                        request = c.message.split()
                        process_request(request)
            elif not chat.is_alive:
                print("NOT is_alive caught.")
                main()

def process_request(target):
    """ Process CAM request """
    print(target)
    tlist = target[1:]
    print(','.join(tlist))
    if "SKY" in target[0]:
        print("SKY Command Issued")
        focus_stellarium(target)
    if "ZOOMIN" in target[0]:
        print("ZOOMIN Command Issued")
        print("Not Implemented")
    if "ZOOMOUT" in target[0]:
        print("ZOOMOUT Command Issued")
        print("Not Implemented")
    if "HOME" in target[0]:
        print("HOME Command Issued")
        print("Not Implemented")

def focus_stellarium(target):
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}
    with requests.Session() as s:
        tlist = target[1:]
        payload = "target=%s" % (','.join(tlist))
        print(payload)
        url = "http://{}:{}/api/main/focus".format(stellarium_server, stellarium_port)
        r = s.post(url, headers=headers, params=payload)
        move_payload = "id=actionMove_Telescope_To_Selection_1"
        move_url = "http://{}:{}/api/stelaction/do".format(stellarium_server, stellarium_port)
        move_r = s.post(move_url, headers=headers, params=payload)
        print("Command sent to {}".format(move_url))


def main():
    logging.basicConfig(level=logging.ERROR)
    log = logging.getLogger()

    print("Starting GAZR - Gazing Adaptive Zoom Robot")
    YouTube_ID = get_streamID()

    try:
        read_chat(YouTube_ID)
        sys.exit(1)
    except Exception as e:
        print(e)
        print("*** TIMEOUT ***")
        time.sleep(1)
        read_chat(YouTube_ID)
        pass


if __name__ == "__main__":
    main()
