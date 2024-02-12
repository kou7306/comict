from flask import Blueprint, render_template, request, redirect, session, flash, url_for, get_flashed_messages
from firebaseSetUp import auth, db
from funcs.wiki import get_manga_title,get_wikipedia_page_details
from firebase_admin import credentials, firestore
from datetime import datetime
from funcs.review_sort import review_sort

reviewAdd_bp = Blueprint('reviewAdd', __name__)
user_doc_ref = db.collection('user')
review_doc_ref=db.collection('review')
comics_doc_ref=db.collection('comics')

# レビューデータベースに入れるときのデータの型
review_format={
    "mangaTitle":None,
    "evaluation":None,
    "contents":None,
    "user_id":None,
}

# レビュー投稿
@reviewAdd_bp.route('/reviewAdd',methods=['GET','POST'])
def review():
    user_id = session.get('user_id')
    if not user_id is None and not user_doc_ref.document(user_id).get().exists:
        return redirect('/login?query=reviewAdd') 
    if request.method == 'GET':
        if user_id:
            logged_in = True
            return render_template("reviewAdd.html",user_id=user_id,logged_in=logged_in)
        else:
            logged_in = False
            return redirect("/login?query=reviewAdd")
    else:
        # formから取得
        manga_title = request.form['work_name']
        rating = request.form['rating']
        comment = request.form['comment_text']
        # Firestoreから指定したuser_idに対応するユーザーネームを取得
        user_doc = user_doc_ref.document(user_id)
        user=user_doc.get()
        

        # 入力されたレビューのデータ
        review_format["evaluation"]=rating
        review_format["mangaTitle"]=manga_title
        review_format["contents"]=comment
        review_format["user_id"]=user_id
        review_format["created_at"]= datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        review_document=review_doc_ref.document() 
        review_document.set(review_format)
        review_document_id = review_document.id

        # 作品データベースに初登録の作品なら追加
        # `comics`コレクションから`title`が`manga_title`と等しいドキュメントを検索
        query = comics_doc_ref.where('title', '==', manga_title).stream()


        # 検索結果がない場合の処理を追加
        if not any(query):
            url=get_wikipedia_page_details(manga_title)

            comics_doc_ref.document(manga_title).set({"title": manga_title,"bookmark":[],"url":url,"reviews":[review_document_id],"author":None})
        # 作品データベースに登録されている場合
        else:
            # 作品データベースの`reviews`フィールドに`id`を追加
            comics_doc_ref.document(manga_title).update({"reviews": firestore.ArrayUnion([review_document_id])})
            

        return redirect("/reviewAdd")


