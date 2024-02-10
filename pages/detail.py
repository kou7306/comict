from flask import Blueprint, render_template, request, redirect, session, flash, url_for, get_flashed_messages
from firebaseSetUp import auth, db

detail_bp = Blueprint('detail', __name__)
user_doc_ref = db.collection('user')
review_doc_ref=db.collection('review')
comics_doc_ref=db.collection('comics')

# 作品詳細ページ
@detail_bp.route('/<user_id>/<title>/detail')
def detail(user_id,title):
    # 詳細情報をwikiから取得
    query = review_doc_ref.where('mangaTitle', '==', title).get()
    url = comics_doc_ref.document(title).get().to_dict()["url"]
    bookmark_num = len(comics_doc_ref.document(title).get().to_dict()["bookmark"])
    
    
    return render_template("detail.html",user_id=user_id,title=title,query=query,url=url,bookmark_num=bookmark_num)
