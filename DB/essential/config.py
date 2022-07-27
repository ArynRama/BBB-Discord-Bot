import os
import json
import pyrebase
from discord import Color

preConf = os.getenv("FB_Info")
firebaseConfig = json.loads(preConf)

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
authed = auth.sign_in_with_email_and_password(os.getenv("FB_Email"), os.getenv("FB_Pass"))
db = firebase.database()
idToken = auth.refresh(authed["refreshToken"])["idToken"]

def botcolor():
    r = int(db.child('settings').child('botcolor1').get(idToken).val())
    g = int(db.child('settings').child('botcolor2').get(idToken).val())
    b = int(db.child('settings').child('botcolor3').get(idToken).val())
    color = Color.from_rgb(r, g, b)
    return color


def devs():
    list = []
    devs = db.child("devs").get(idToken).val()
    for dev in devs:
        list.append(dev)
    return list
