from flask import Blueprint, render_template, request, redirect, session, flash, url_for, get_flashed_messages
from firebaseSetUp import auth, db

review_bp = Blueprint('review', __name__)   

user_doc_ref = db.collection('user')
review_doc_ref=db.collection('review')

@review_bp.route('/review', methods = ['GET','POST'])
def review():
    if request.method == 'GET':
        user_id = session.get('user_id')
        if user_id:
            logged_in = True
        else:
            logged_in = False
        return render_template("review.html",logged_in=logged_in)
