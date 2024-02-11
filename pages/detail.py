from flask import Blueprint, render_template, request, redirect, session, flash, url_for, get_flashed_messages
from firebaseSetUp import auth, db

detail_bp = Blueprint('detail', __name__)
user_doc_ref = db.collection('user')
review_doc_ref=db.collection('review')
comics_doc_ref=db.collection('comics')

# 作品詳細ページ
@detail_bp.route('/<title>/detail')
def detail(title):
    user_id = session.get('user_id')

    comics_doc = comics_doc_ref.document(title)
        
    # ブックマークの状態を取得
    comics_data = comics_doc.get()
    if not user_id is None and not user_doc_ref.document(user_id).get().exists:
        return redirect("/login")
    if user_id:
        logged_in = True
        current_bookmark = comics_data.to_dict().get("bookmark", [])
        # bookmarkに自分のIDが含まれているか
        if user_id in current_bookmark:
            bookmarked = True
        else:
            bookmarked = False
    else:
        logged_in = False
        bookmarked = False
        
    # 詳細情報をwikiから取得
    query = review_doc_ref.where('mangaTitle', '==', title).get()
    url = comics_doc_ref.document(title).get().to_dict()["url"]
    bookmark_num = len(comics_doc_ref.document(title).get().to_dict()["bookmark"])

    
    return render_template("detail.html",title=title,query=query,url=url,bookmark_num=bookmark_num,logged_in=logged_in,bookmarked=bookmarked)
