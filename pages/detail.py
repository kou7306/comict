from flask import Blueprint, render_template, request, redirect, session, jsonify
from firebaseSetUp import auth, db
from funcs.review_sort import review_sort

detail_bp = Blueprint('detail', __name__)
user_doc_ref = db.collection('user')
review_doc_ref=db.collection('review')
comics_doc_ref=db.collection('comics')

# 作品詳細ページ
@detail_bp.route('/<title>/detail')
def detail(title):
    # query = review_doc_ref.where('mangaTitle', '==', title).get()
    comics_doc = comics_doc_ref.document(title).get()
    user_id = session.get('user_id')
    
    if comics_doc.exists:
        comic_data = comics_doc.to_dict()
        url = comic_data.get("url", "#")
        bookmark_num = len(comic_data.get("bookmark", []))
        bookmarked = user_id in comic_data.get("bookmark", []) if user_id else False
    else:
        url = "#"
        bookmark_num = 0
        bookmarked = False
        
    if not user_id is None and not user_doc_ref.document(user_id).get().exists:
        return redirect("/login")
    
    logged_in = bool(user_id)
    
    # if user_id:
    #     logged_in = True
    #     current_bookmark = comic_data["bookmark"]
    #     # bookmarkに自分のIDが含まれているか
    #     if user_id in current_bookmark:
    #         bookmarked = True
    #     else:
    #         bookmarked = False
    # else:
    #     logged_in = False
    #     bookmarked = False
        
        
    # reviews = []
    # for doc in query:
    #     doc_id = doc.id
    #     doc_data = doc.to_dict()
    #     likes = doc_data.get('likes', [])
    #     like_count = len(likes)
    #     user_liked = user_id in likes if user_id else False

    #     reviews.append({
    #         "id": doc_id, 
    #         "data": doc_data,
    #         "like_count": like_count,
    #         "user_liked": user_liked
    #     })
        
    return render_template("detail.html",title=title, url=url, bookmark_num=bookmark_num, logged_in=logged_in, bookmarked=bookmarked)

@detail_bp.route('/review/<title>')
def get_reviews(title):
    sort_option = request.args.get('sort_option', 'newest')
    reviews = review_sort(sort_option, title)
    print("reviews:", reviews)
    
    return jsonify(reviews)