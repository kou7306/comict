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
        return redirect(f"/login?query={title}/detail")
    
    logged_in = bool(user_id)

    # 作品の平均評価を取得
    reviews=review_doc_ref.stream()
    reviews_data=[]
    eval_sum,rev_sum,eval_avg=0,0,0

    for review in reviews:
        review_data=review.to_dict()
        reviews_data.append(review_data)
    
    for review in reviews_data:
        review_title=review.get('mangaTitle')
        if review_title==title:
            review_eval=review.get('evaluation')
            eval_sum+=review_eval
            rev_sum+=1
    if rev_sum!=0:
        eval_avg=eval_sum/rev_sum

    

        
    return render_template("detail.html",title=title, url=url, bookmark_num=bookmark_num, logged_in=logged_in, bookmarked=bookmarked,eval_avg=eval_avg,rev_sum=rev_sum)

@detail_bp.route('/review/<title>')
def get_reviews(title):
    sort_option = request.args.get('sort_option', 'newest')
    reviews = review_sort(sort_option,None,limit=None, title=title)
    
    return jsonify(reviews)