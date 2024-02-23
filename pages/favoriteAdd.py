from flask import Blueprint, render_template, request, redirect, session, flash, url_for, get_flashed_messages,jsonify
from firebaseSetUp import auth, db
from firebase_admin import credentials, firestore
from funcs.wiki import get_manga_title,get_wikipedia_page_details
from funcs.get_book import get_google_book_cover

favoriteAdd_bp = Blueprint('favoriteAdd', __name__)
user_doc_ref = db.collection('user')
comics_doc_ref=db.collection('comics')

# 好きな作品を追加
@favoriteAdd_bp.route('/favoriteAdd', methods=['GET', 'POST'])
def add_manga():
    user_id = session.get('user_id')

    logged_in = True   
    user_doc = user_doc_ref.document(user_id)
    user=user_doc.get()
    favorite_titles = user.to_dict().get("bookmark", [])
    if request.method == 'GET':
        if not user_id is None and not user_doc_ref.document(user_id).get().exists:
            return redirect("/login?query=favoriteAdd")
        return render_template('favoriteAdd.html', user_id=user_id, favorite_titles=favorite_titles,logged_in=logged_in) 
    elif request.method == 'POST':
        data = request.get_json()
        manga_title = data.get('title') 
        print(manga_title)
        # ユーザードキュメントの更新
        user_doc.update({
            'bookmark': firestore.ArrayUnion([manga_title])
        })



        #　漫画テーブルの更新
        # `comics`コレクションから`title`が`manga_title`と等しいドキュメントを検索
        query = comics_doc_ref.where('title', '==', manga_title).stream()




        # 検索結果がない場合の処理を追加
        if not any(query):
            url=get_wikipedia_page_details(manga_title)
            image_url=get_google_book_cover(manga_title)
            print(url)
            print(image_url)

            comics_doc_ref.document(manga_title).set({"title": manga_title,"bookmark":[user_id],"url":url,"reviews":[],"author":None,"image":image_url})
        else:
            # comicsドキュメントのbookmarkを更新
            comics_doc_ref.document(manga_title).update({
            'bookmark': firestore.ArrayUnion([user_id])
        })
        # ユーザーデータの取得
        favorite_titles.append(manga_title)
        return jsonify({'favoriteTitles': favorite_titles})
