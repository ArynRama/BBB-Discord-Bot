import os
import pyrebase
from time import sleep, time

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
authentication = firebase.auth()
auth = authentication.sign_in_with_email_and_password(
    os.getenv("FB_Email"), os.getenv("FB_Pass"))
db = firebase.database()
idToken = auth['idToken']

while True:
    sleep(60 - time() % 60)

    authentication.refresh(auth['refreshToken'])
    idToken = auth['idToken']
