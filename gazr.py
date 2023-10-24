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
import argparse
import json
import mechanize
import http.cookiejar as cookielib
import requests
from bs4 import BeautifulSoup
from settings import (
    S_LOGIN,
    S_PASSWORD,
    STELLARIUM_SERVER,
    STELLARIUM_PORT,
    USER_LIST
)

stel_headers = {'User-Agent': "GAZR (X11;U;Linux MyKernelMyBusiness; Insider-Powered) Skinwalker/2023101420-1 gazr.py"}

ap = argparse.ArgumentParser()
ap.add_argument("-h", help="This message")
ap.add_argument("-m", "--mode", type=int, default="1", help="1-defined users, 2-open access")
args = vars(ap.parse_args())

def get_streamID():
    """ Get current Stream ID from the YouTube channel """
    user_agent = [
        (
            "User-agent",
            "GAZR (X11;U;Linux MyKernelMyBusiness; Insider-Powered) Skinwalker/20221214-1 gazr.py",
        )
    ]

    cj = cookielib.CookieJar()
    br = mechanize.Browser()
    br.set_cookiejar(cj)
    br.set_handle_robots(False)
    br.addheaders = user_agent
    br.open("https://skinwalker-ranch.com/ranch-webcam-livestream/")

    br.select_form(name="mepr_loginform")
    br.form["log"] = S_LOGIN
    br.form["pwd"] = S_PASSWORD
    br.submit()

    soup = BeautifulSoup(br.response().read(), features="html5lib")
    for item in soup.find_all("iframe"):
        if "embed" in item.get("src"):
            stream_url = item.get("src")
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
                    if c.author.name in USER_LIST or c.author.isChatModerator or c.author.isChatOwner:
                        logging.info(f"CAM: {c.message}")
                        request = c.message.split()
                        user_mode = args["mode"]
                        if user_mode == 1: 
                            if c.author.name in USER_LIST or c.author.isChatModerator or c.author.isChatOwner:
                                process_request(yt_user, request)
                        elif user_mode == 2:
                            process_request(yt_user, request)

            elif not chat.is_alive:
                logging.debug("NOT is_alive caught.")
                main()

def process_request(yt_user, target):
    """ Process CAM request """
    tlist = target[1:]
    if "SKY" in target[0]:
        print(f"SKY Command Issued by {yt_user}")
        horizon_check(target)
    if "ZOOMIN" in target[0]:
        print("ZOOMIN Command Issued")
        print("Not Implemented")
    if "ZOOMOUT" in target[0]:
        print("ZOOMOUT Command Issued")
        print("Not Implemented")
    if "HOME" in target[0]:
        print("HOME Command Issued")
        print("Not Implemented")

def horizon_check(target):
    target_string = target[1:]
    ts_joined = ' '.join(target_string)
    check_url = f"http://{STELLARIUM_SERVER}:{STELLARIUM_PORT}/api/objects/info?name={ts_joined}&format=json"
    print(f"Checking object at {check_url}")
    object = requests.get(check_url)
    object_json = json.loads(object.content)
    if object_json['above-horizon']:
        focus_stellarium(target)
    else:
        print("Request below horizon ignored.")

def zoom_stellarium(set_fov):
    """ Set field of view values through Stellarium API """
    with requests.Session() as s:
        tlist = target[1:]
        """ Tell Stellarium to search for and focus on an object """
        payload = "target=%s" % (' '.join(tlist))
        url = f"http://{STELLARIUM_SERVER}:{STELLARIUM_PORT}/api/scripts/direct"
        r = s.post(url, headers=stel_headers, params=payload)
        """ Tell Stellarium to slew telescope to selected object """
        move_payload = "id=actionMove_Telescope_To_Selection_1"
        move_url = f"http://{STELLARIUM_SERVER}:{STELLARIUM_PORT}/api/stelaction/do"
        move_r = s.post(move_url, headers=stel_headers, params=move_payload)
        print(f"Command sent to {move_url} requesting telescope focus on {payload}.")

def focus_stellarium(target):
    """ Use HTTP POST Method to focus on object and slew telescope """
    with requests.Session() as s:
        tlist = target[1:]
        """ Tell Stellarium to search for and focus on an object """
        payload = "target=%s" % (' '.join(tlist))
        url = f"http://{STELLARIUM_SERVER}:{STELLARIUM_PORT}/api/main/focus"
        r = s.post(url, headers=stel_headers, params=payload)
        """ Tell Stellarium to slew telescope to selected object """
        move_payload = "id=actionMove_Telescope_To_Selection_1"
        move_url = f"http://{STELLARIUM_SERVER}:{STELLARIUM_PORT}/api/stelaction/do"
        move_r = s.post(move_url, headers=stel_headers, params=move_payload)
        print(f"Command sent to {move_url} requesting telescope focus on {payload}.")


def main():
    logging.basicConfig(level=logging.ERROR)
    log = logging.getLogger()

    print("Starting GAZR - Gazing Adaptive Zoom Robot")
    YouTube_ID = get_streamID()
    print("Reading Stream Chat. Ready to Gaze...")
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
