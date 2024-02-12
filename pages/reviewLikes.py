from flask import Blueprint, request, session, jsonify, redirect
from firebase_admin import firestore
from firebaseSetUp import db

reviewLikes_bp = Blueprint('reviewLikes', __name__)
user_doc_ref = db.collection('user')

# いいね機能
@reviewLikes_bp.route("/reviewLike/<review_id>", methods=["POST"])
def toggle_likes(review_id):
    user_id = session.get("user_id")
    if not user_id or not user_doc_ref.document(user_id).get().exists:
        return jsonify({"error": "Unauthorized"}), 401
    
    review_ref = db.collection('review').document(review_id)
    review_doc = review_ref.get()
    
    if review_doc.exists:
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
    