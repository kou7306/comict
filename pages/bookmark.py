from flask import Blueprint, render_template, request, redirect, session, flash, url_for, get_flashed_messages,jsonify
from firebaseSetUp import auth, db
from google.cloud.firestore import ArrayUnion, ArrayRemove

bookmark_bp = Blueprint('bookmark', __name__)
user_doc_ref = db.collection('user')
comics_doc_ref=db.collection('comics')

# ブックマーク機能
@bookmark_bp.route("/bookmark", methods=["POST"])
def toggle_bookmark():
    data = request.get_json()
    user_id = session.get("user_id")
    if not user_doc_ref.document(user_id).get().exists:
        return jsonify({"bookmarknum": -1, "bookmarked": False})
    # 漫画のタイトルを取得
    title = data.get("title")
    if not user_id:
        
        return jsonify({"bookmarknum": -1, "bookmarked": False})
    else:

        comics_doc = comics_doc_ref.document(title)
        
        # ブックマークの状態を取得
        comics_data = comics_doc.get()
        
        if comics_data.exists:
            current_bookmark = comics_data.to_dict().get("bookmark", [])
        else:
            current_bookmark = []

        user_doc = user_doc_ref.document(user_id)
        # 新しいユーザーIDをブックマークリストに追加
        if user_id not in current_bookmark:
            current_bookmark.append(user_id)
            comics_doc.update({"bookmark": current_bookmark})
            new_bookmark_value = len(current_bookmark) # ブックマーク数を取得
            
            # ユーザーテーブルのブックマークリストを更新
            user_doc.update({"bookmark": ArrayUnion([title])})
            bookmarked = True
            
        else:
            current_bookmark.remove(user_id)
            comics_doc.update({"bookmark": current_bookmark})
            new_bookmark_value = len(current_bookmark)

            # ユーザーテーブルのブックマークリストを更新
            user_doc.update({"bookmark": ArrayRemove([title])})
            bookmarked = False




        return jsonify({"bookmarknum": new_bookmark_value, "bookmarked": bookmarked})

