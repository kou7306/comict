from flask import Blueprint, request, session, jsonify, redirect
from firebase_admin import firestore
from firebaseSetUp import db

reviewLikes_bp = Blueprint('reviewLikes', __name__)
user_doc_ref = db.collection('user')

# いいね機能用のエンドポイント
@reviewLikes_bp.route("/reviewLike/<review_id>", methods=["POST"])
def toggle_likes(review_id):
    user_id = session.get("user_id")
    if not user_id or not user_doc_ref.document(user_id).get().exists:
        return jsonify({"error": "Unauthorized"}), 401
    
    review_ref = db.collection('review').document(review_id)
    review_doc = review_ref.get()
    
    if review_doc.exists:
        transaction = db.transaction()
        @firestore.transactional
        def update_likes_in_transaction(transaction, review_ref, user_id):
            review_doc = review_ref.get(transaction=transaction)
            likes = review_doc.to_dict().get('likes', [])
            if user_id in likes:
                likes.remove(user_id)
                transaction.update(review_ref, {'likes': likes, 'likes_count': firestore.Increment(-1)})
                return {'status': 'unliked'}
            else:
                likes.append(user_id)
                transaction.update(review_ref, {'likes': likes, 'likes_count': firestore.Increment(1)})
                return {'status': 'liked'}
        
        result = update_likes_in_transaction(transaction, review_ref, user_id)
        return jsonify(result), 200
    else:
        return jsonify({"error": "Review not found"}), 404