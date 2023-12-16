import json

import requests
from bardapi import Bard, BardCookies
from bardapi.constants import SESSION_HEADERS


def initialize_bard_session(_1PSID, _1PSIDTS, _1PSIDCC):
    session = requests.Session()
    session.headers = SESSION_HEADERS
    session.cookies.set("__Secure-1PSID", _1PSID)
    session.cookies.set("__Secure-1PSIDTS", _1PSIDTS)
    session.cookies.set("__Secure-1PSIDCC", _1PSIDCC)
    session.headers = {
        "Host": "bard.google.com",
        "X-Same-Domain": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.4472.114 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Origin": "https://bard.google.com",
        "Referer": "https://bard.google.com/",
    }
session = requests.Session()
session.headers = SESSION_HEADERS

session.cookies.set("__Secure-1PSID","eAjOKiNPwlQLDpSFLWY8fpBHMd7hEVobhROPX7mRp6ZISrljhCT0_oOR8mB-kGVgm2waXg.")
session.cookies.set("__Secure-1PSIDTS", "sidts-CjEBPVxjSmsADUzw4772LBm7ev_yrlsdIZVcw3w3mcbjDK-unWx0FtMtN1o4L1pwsR02EAA")
session.cookies.set("__Secure-1PSIDCC", "ABTWhQEUfqGQFZ6kMocdbVq-C2pAGs2tFekv6XDQkJvp3wv80iOpoQOzv4BHxIB8Iw61UklPxxwt")
bard = Bard(token="eAjOKiNPwlQLDpSFLWY8fpBHMd7hEVobhROPX7mRp6ZISrljhCT0_oOR8mB-kGVgm2waXg.", session=session)
#bard = Bard(token="eAjOKiNPwlQLDpSFLWY8fpBHMd7hEVobhROPX7mRp6ZISrljhCT0_oOR8mB-kGVgm2waXg.", session=session)
#bard = BardCookies(token_from_browser=True,conversation_id='c_7a7d053b12de17bb')
def send_message(message):
    try:
        answer = bard.get_answer(message)['content']
        return answer
    except Exception as e:
        return str(e)


