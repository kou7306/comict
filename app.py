from flask import Flask, render_template, request, jsonify, redirect, session, current_app,url_for, flash, get_flashed_messages



from firebaseSetUp import auth, db
from pages.home import home_bp
from pages.auth import auth_bp

from pages.check import check_bp
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
from pages.comic import comic_bp
from pages.reviewAdd import reviewAdd_bp
from pages.reviewLikes import reviewLikes_bp
from pages.update_matching import update_matching_bp
from pages.user import user_bp
from pages.review_detail import review_detail_bp
from pages.load_more_data import load_more_data_bp


app = Flask(__name__)
app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)
app.register_blueprint(check_bp)
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
app.register_blueprint(comic_bp)
app.register_blueprint(reviewAdd_bp)  
app.register_blueprint(reviewLikes_bp)  
app.register_blueprint(update_matching_bp)
app.register_blueprint(user_bp)
app.register_blueprint(review_detail_bp)
app.register_blueprint(load_more_data_bp)

app.secret_key = "secret"

if __name__ == '__main__':
    app.run(debug=True,port=8080)

# /fm8MhfrbKdJ5narcJvTm/home testへのURL