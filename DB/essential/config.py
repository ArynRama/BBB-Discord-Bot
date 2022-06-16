import pyrebase
from discord import Color

firebaseConfig = {
    "apiKey": "AIzaSyB1ujCtmCOnd7aMft806lJguZV3gXVt6l0",
    "authDomain": "discord-bot-database-b44ec.firebaseapp.com",
    "databaseURL": "https://discord-bot-database-b44ec-default-rtdb.firebaseio.com",
    "projectId": "discord-bot-database-b44ec",
    "storageBucket": "discord-bot-database-b44ec.appspot.com",
    "messagingSenderId": "769471483502",
    "appId": "1:769471483502:web:579519c2b0e9b39197a07f",
    "measurementId": "G-RPC6GZKFNR"
}

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()

def botcolor():
    r = int(db.child('settings').child('botcolor1').get().val())
    g = int(db.child('settings').child('botcolor2').get().val())
    b = int(db.child('settings').child('botcolor3').get().val())
    color = Color.from_rgb(r, g, b)
    return color


def devs():
    list = []
    devs = db.child("devs").get().val()
    for dev in devs:
        list.append(dev)
    return list
