from flask import Blueprint, render_template, request, redirect, session, flash, url_for, get_flashed_messages, jsonify
from firebaseSetUp import auth, db
from funcs.wiki import get_manga_title,get_wikipedia_page_details
from firebase_admin import credentials, firestore
from datetime import datetime
from funcs.review_sort import review_sort

review_bp = Blueprint('review', __name__)   

user_doc_ref = db.collection('user')
review_doc_ref=db.collection('review')
comics_doc_ref=db.collection('comics')

# レビュー取得用エンドポイント
@review_bp.route('/api/reviews', methods=['POST'])
def fetch_reviews():
    user_id = session.get('user_id')
    logged_in = True if user_id else False
    
    data = request.get_json()
    sort_option = data.get('sortOption', 'evaluation_desc')
    last_review_id = data.get('lastReviewId', None)
    
    # print('sort_option:', sort_option)
    # print('last_review_id:', last_review_id)
    
    reviews = review_sort(sort_option, last_review_id)
    
    response_data = {
        'logged_in': logged_in,
        'reviews': reviews
    }
    
    return jsonify(response_data)

# レビュー一覧レンダリング用
@review_bp.route('/review', methods=['GET'])
def review():
    if request.method == 'GET':
        user_id = session.get('user_id')
        if user_id:
            logged_in = True
        else:
            logged_in = False
            
        return render_template("review.html", user_id=user_id, logged_in=logged_in)



