from flask import Blueprint, render_template, request, redirect, session, flash, url_for, get_flashed_messages,jsonify
from firebaseSetUp import auth, db
from funcs.matching import matching

update_matching_bp = Blueprint('update_matching', __name__)
user_doc_ref = db.collection('user')
review_doc_ref=db.collection('review')
comics_doc_ref=db.collection('comics')


# 定期実行でリクエストされるエンドポイント
@update_matching_bp.route('/update_matching', methods=["POST"])
def update_matching():   
    all_user = user_doc_ref.stream()
    # 全ユーザーのマッチング結果を更新
    for user in all_user:
        user_id = user.id
        user_doc = user_doc_ref.document(user_id)
        # マッチング
        review_query, user_query =matching(user.to_dict()["mangaAnswer"],user_id)
        
        update_data = {"user_query":  user_query,"review_query":review_query}
        user_doc.update(update_data)
    return jsonify({"message": "マッチングが更新されました。"})