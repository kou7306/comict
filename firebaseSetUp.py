from flask import Blueprint
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore

firebase_bp = Blueprint('firebase_bp', __name__)

config = {
    "apiKey": "AIzaSyBPva6sGWXi6kjmk8mjWWVCGEKKEBIfTIY",
    "authDomain": "giikucamp12.firebaseapp.com",
    "projectId": "giikucamp12",
    "storageBucket": "giikucamp12.appspot.com",
    "messagingSenderId": "755980381836",
    "appId": "1:755980381836:web:acdae710db8366cc4095a9",
    "measurementId": "G-00EVCKC0JQ",
    "databaseURL": ""
}

# Firebase Admin SDK を初期化
cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# authenticationの設定
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()