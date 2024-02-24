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

# レビュー一覧
@review_bp.route('/review', methods=['GET', 'POST'])
def review():
    if request.method == 'GET':
        user_id = session.get('user_id')
        if user_id:
            logged_in = True
        else:
            logged_in = False
        sort_option = request.args.get('sort_option')


        reviews = review_sort(sort_option,None)
        return render_template("review.html", user_id=user_id, reviews=reviews, sort_option=sort_option, logged_in=logged_in, user_doc_ref=user_doc_ref, comics_doc_ref=comics_doc_ref)

    elif request.method == 'POST':
        user_id = session.get('user_id')
        if not user_id or not user_doc_ref.document(user_id).get().exists:
            return jsonify({"error": "Unauthorized"}), 401
        
        review_id = request.form.get('review_id')
        review_ref = db.collection('review').document(review_id)
        review_doc = review_ref.get()
    
        if review_doc.exists and user_doc_ref.document(user_id).get().exists:
            likes = review_doc.to_dict().get('likes', [])
            if user_id in likes:
                review_ref.update({'likes': firestore.ArrayRemove([user_id])})
                review_ref.update({'likes_count': firestore.Increment(-1)})
                return jsonify({'status': 'unliked'}), 200
            else:
                review_ref.update({'likes': firestore.ArrayUnion([user_id])})
                review_ref.update({'likes_count': firestore.Increment(1)})
                return jsonify({'status': 'liked'}), 200
        else:
            return jsonify({"error": "Review not found"}), 404


