import json
import requests
from bardapi import Bard
from bardapi.constants import SESSION_HEADERS

def initialize_bard_session(_1PSID, _1PSIDTS, _1PSIDCC):
    session = requests.Session()
    session.headers = SESSION_HEADERS
    session.cookies.set("__Secure-1PSID", "dQg50xvxqQlaPFv-HIPCMdHRatpM2rvBJsUtI6qK-x1MCrG20brE4QEXp9e61BEogRimVw.")
    session.cookies.set("__Secure-1PSIDTS", _1PSIDTS)
    session.cookies.set("__Secure-1PSIDCC","ABTWhQFWXTZGjlvHBw4FjCE-LVadjOUbeDK0N3E6Wzvj8OJ4LxPi-Ukt6jn8MGyomTgTv0M6Mpg")
    session.headers = {
        "Host": "bard.google.com",
        "X-Same-Domain": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.4472.114 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Origin": "https://bard.google.com",
        "Referer": "https://bard.google.com/",
    }
from bardapi import Bard, BardCookies
session = requests.Session()
session.headers = SESSION_HEADERS
session.cookies.set("__Secure-1PSID","eAjOKiNPwlQLDpSFLWY8fpBHMd7hEVobhROPX7mRp6ZISrljhCT0_oOR8mB-kGVgm2waXg.")
session.cookies.set("__Secure-1PSIDTS", "sidts-CjEBPVxjSm_Q832mLrShRGWALxOfRnviRH_m1ROkPyx56DKCQmTQcQ4tf4JaRZ8K1pM2EAA")
session.cookies.set("__Secure-1PSIDCC", "ABTWhQEvH8DO0UmeMYGu9rut4p5ZgqDmtBylgjBLnpg-6z2FyegLko12IospIt19I3dZ0vjKUvZj")

#bard = Bard(token="dQg50xvxqQlaPFv-HIPCMdHRatpM2rvBJsUtI6qK-x1MCrG20brE4QEXp9e61BEogRimVw.", session=session)
bard = BardCookies(token_from_browser=True,conversation_id='c_7a7d053b12de17bb')

def send_message(message):
    try:
        answer = bard.get_answer(message)['content']
        return answer
    except Exception as e:
        return str(e)


