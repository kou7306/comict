from flask import Flask, render_template, request, jsonify, redirect, session, current_app,url_for, flash, get_flashed_messages
import faiss
import numpy as np
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
from bs4 import BeautifulSoup
import requests
import os
import wikipedia
from wiki import get_manga_title,get_wikipedia_page_details
from firebaseSetUp import auth, db
from pages.auth import auth_bp
from pages.home import home_bp
from funcs.get_book import get_rakuten_book_cover
from pages.genre import genre_bp
from pages.question import question_bp
from pages.review import review_bp
from pages.userpage import userpage_bp
from pages.reviewerpage import reviewerpage_bp
from pages.detail import detail_bp
from pages.favoriteAdd import favoriteAdd_bp
from pages.favoriteDelete import favoriteDelete_bp
from pages.bookSearch import bookSearch_bp
from pages.getTitle import getTitle_bp
from pages.bookmark import bookmark_bp


app = Flask(__name__)
app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)
app.register_blueprint(genre_bp)
app.register_blueprint(question_bp)
app.register_blueprint(review_bp)
app.register_blueprint(userpage_bp)
app.register_blueprint(reviewerpage_bp)
app.register_blueprint(detail_bp)
app.register_blueprint(favoriteAdd_bp)
app.register_blueprint(favoriteDelete_bp)
app.register_blueprint(bookSearch_bp)
app.register_blueprint(getTitle_bp)
app.register_blueprint(bookmark_bp)




app.secret_key = "secret"

if __name__ == '__main__':
    app.run(debug=True,port=8080)

# /fm8MhfrbKdJ5narcJvTm/home testへのURL