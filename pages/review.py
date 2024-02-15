from flask import Blueprint, render_template, request, redirect, session, flash, url_for, get_flashed_messages
from firebaseSetUp import auth, db
from funcs.wiki import get_manga_title,get_wikipedia_page_details
from firebase_admin import credentials, firestore
from datetime import datetime
from funcs.review_sort import review_sort

review_bp = Blueprint('review', __name__)   

user_doc_ref = db.collection('user')
review_doc_ref=db.collection('review')


# レビュー一覧
@review_bp.route('/review')
def review():
    if request.method == 'GET':
        user_id = session.get('user_id')
        if not user_id is None and not user_doc_ref.document(user_id).get().exists:
            return redirect("/login")
       
        if user_id:
            logged_in = True
        else:
            logged_in = False
        sort_option = request.args.get('sort_option')
       

        reviews = review_sort(sort_option,None)

        return render_template("review.html", user_id=user_id, reviews=reviews, sort_option=sort_option, logged_in=logged_in, user_doc_ref=user_doc_ref)


