import json
import requests
from bardapi import Bard
from bardapi.constants import SESSION_HEADERS

def initialize_bard_session(_1PSID, _1PSIDTS, _1PSIDCC):

from bardapi import Bard, BardCookies
session = requests.Session()
session.headers = SESSION_HEADERS

session.cookies.set("__Secure-1PSID","eAjOKiNPwlQLDpSFLWY8fpBHMd7hEVobhROPX7mRp6ZISrljhCT0_oOR8mB-kGVgm2waXg.")
session.cookies.set("__Secure-1PSIDTS", "sidts-CjEBPVxjSgSYvX_091bJQCoN5Q20Xs9Mjx1LZxewOhGWRKhIP9oaElq93hgGSAXf-w0DEAA")
session.cookies.set("__Secure-1PSIDCC", "ABTWhQG3k3nefXqouOlzCl42LDJE_2wVsa1m9z-yHN4Ax4jbpPQkMwNT3xy91CeufBZg-Jy1j4d4")

bard = Bard(token="eAjOKiNPwlQLDpSFLWY8fpBHMd7hEVobhROPX7mRp6ZISrljhCT0_oOR8mB-kGVgm2waXg.", session=session)

def send_message(message):
    try:
        answer = bard.get_answer(message)['content']
        return answer
    except Exception as e:
        return str(e)


