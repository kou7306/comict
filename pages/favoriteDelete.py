from flask import Blueprint, render_template, request, redirect, session, flash, url_for, get_flashed_messages, jsonify
from firebaseSetUp import auth, db
from google.cloud import firestore

favoriteDelete_bp = Blueprint('favoriteDelete', __name__)
user_doc_ref = db.collection('user')

# 好きな作品を削除
@favoriteDelete_bp.route('/favoriteDelete', methods=['POST'])
def delete_manga():
    user_id = session.get('user_id')
    user_doc = user_doc_ref.document(user_id)
    user=user_doc.get()
    favorite_titles = user.to_dict().get("bookmark", [])

    data = request.get_json()
    manga_title = data.get('title') 
    if favorite_titles != []:
        favorite_titles.remove(manga_title)
    # ユーザードキュメントの更新
    user_doc.update({
        'bookmark': favorite_titles
    })

    # comicsドキュメントのbookmarkを更新
    comics_doc_ref=db.collection('comics')
    comics_doc_ref.document(manga_title).update({
        'bookmark': firestore.ArrayRemove([user_id])
    })

    return jsonify({'favoriteTitles': favorite_titles})