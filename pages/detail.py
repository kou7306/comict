from flask import Blueprint, render_template, request, redirect, session, flash, url_for, get_flashed_messages
from firebaseSetUp import auth, db

detail_bp = Blueprint('detail', __name__)
user_doc_ref = db.collection('user')
review_doc_ref=db.collection('review')
comics_doc_ref=db.collection('comics')

# 作品詳細ページ
@detail_bp.route('/<title>/detail')
def detail(title):
    query = review_doc_ref.where('mangaTitle', '==', title).get()
    comics_doc = comics_doc_ref.document(title).get()
    user_id = session.get('user_id')
    
    if comics_doc.exists:
        comic_data = comics_doc.to_dict()
        url = comic_data["url"]
        bookmark_num = len(comic_data.get("bookmark", []))
    else:
        url = "#"
        bookmark_num = 0
        
    if not user_id is None and not user_doc_ref.document(user_id).get().exists:
        return redirect("/login")
    
    if user_id:
        logged_in = True
        current_bookmark = comic_data["bookmark"]
        # bookmarkに自分のIDが含まれているか
        if user_id in current_bookmark:
            bookmarked = True
        else:
            bookmarked = False
    else:
        logged_in = False
        bookmarked = False
        
        
    reviews = []
    for doc in query:
        doc_id = doc.id
        doc_data = doc.to_dict()
        likes = doc_data.get('likes', [])
        like_count = len(likes)
        user_liked = user_id in likes if user_id else False

        reviews.append({
            "id": doc_id, 
            "data": doc_data,
            "like_count": like_count,
            "user_liked": user_liked
        })
        
    return render_template("detail.html",title=title, url=url, bookmark_num=bookmark_num, reviews=reviews, logged_in=logged_in, bookmarked=bookmarked)