"""Log into nersc account and get newt session id."""

import getpass
import os

import requests


from .assets import NEWT_BASE_URL, REQUESTS_SESSION


class _LoginUtility(object):
    def __init__(self):
        user = input("Username: ")
        password = getpass.getpass(prompt="Password: ")
        otp = input("Enter one time password (for MFA) ")

        self.credentials = {
            "username": user,
            # NOTE: this gets stored at runtime, and isn't secure
            "password": password + str(otp),
        }

    def create_sessionid(self, file="~/.newt_sessionid"):
        url = "{}/login/".format(NEWT_BASE_URL)
        r = requests.post(url, data=self.credentials)
        r.raise_for_status()

        js = r.json()
        if not js.get("auth"):
            raise RuntimeError("NOT authenticated: ", r.text)

        # (else)
        session_id = js.get("newt_sessionid")
        print("newt_sessionid: {}".format(session_id))

        output_filename = os.path.expanduser(file)
        with open(output_filename, "w") as f:
            f.write(session_id)
            print("Wrote {}".format(output_filename))

        # Sanity check -- get user's scratch directory
        cookies = dict(newt_sessionid=session_id)
        data = {"executable": "echo $SCRATCH", "loginenv": "true"}
        machine = "cori"
        url = "%s/command/%s" % (NEWT_BASE_URL, machine)
        r = requests.post(url, data=data, cookies=cookies)
        r.raise_for_status()
        print(r.json())


def login(file="~/.newt_sessionid", newt_sessionid=None):
    """"""
    if newt_sessionid is None:
        path = os.path.expanduser(file)
        if not os.path.exists(path):
            # Perform the login
            _LoginUtility()

        with open(path) as f:
            newt_sessionid = f.read().strip()
    assert newt_sessionid is not None
    print("sending command...")

    url = "{}/login/".format(NEWT_BASE_URL)
    cookies = dict(newt_sessionid=newt_sessionid)
    r = requests.get(url, cookies=cookies)
    r.raise_for_status()

    js = r.json()
    # print('login reply', js)
    # Example reply:
    # {'username': 'johnt', 'session_lifetime': 976394, 'auth': True, 'newt_sessionid': '0fc3f5310b54310f08bdcbf690d5c255'}
    if "auth" not in js or not js["auth"]:
        print("Reply:", js)
        raise Exception("User not logged in. Try agin.")

    if hasattr(js, "session_lifetime") and js["session_lifetime"] < 300:
        print("Reply:", js)
        template = "Session lifetime about to expire ({} sec)"
        raise Exception(template.format(js["session_lifetime"]))

    REQUESTS_SESSION.cookies.set("newt_sessionid", newt_sessionid)
    print("OK")
    return True
