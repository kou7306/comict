from flask import Blueprint, render_template, request, redirect, session, jsonify
from firebaseSetUp import auth, db
from funcs.get_book import get_google_book_cover
from funcs.get_book import get_rakuten_book_cover
from funcs.most_review_comics import most_review_comics
from funcs.high_evaluate_comics import high_evaluate_comics
from funcs.most_bookmark_comics import most_bookmark_comics
from funcs.search import search_comics

comic_bp = Blueprint('comic', __name__)   

user_doc_ref = db.collection('user')
review_doc_ref=db.collection('review')
comics_doc_ref=db.collection('comics')
suggestion_doc_ref=db.collection('suggestion')


# マッチングしたユーザーとフォローしたユーザーを取得する
def get_user_queries_and_follows(user_id):
    user_doc = user_doc_ref.document(user_id).get()
    if user_doc.exists:
        user_data = user_doc.to_dict()
        user_queries = user_data.get('user_query', [])
        follows = user_data.get('follow', [])
        connected_user_ids = user_queries + follows
        return connected_user_ids
    else:
        return []
    
# ユーザーidからブックマーの作品をとってくる
def get_bookmarks(connected_user_ids):
    bookmarks = []
    for user_id in connected_user_ids:
        user_doc = user_doc_ref.document(user_id).get()
        if user_doc.exists:
            user_data = user_doc.to_dict()
            user_bookmarks = user_data.get('bookmark', [])
            bookmarks.extend(user_bookmarks)
    return bookmarks

# review_queryに含まれるレビューを取ってくる
def get_review_query(user_id):
    user_doc = user_doc_ref.document(user_id).get()
    if user_doc.exists:
        user_data = user_doc.to_dict()
        review_query = user_data.get('review_query', [])
        return review_query
    else:
        return []

# review_queryの中で★４以上の漫画のタイトルを取ってくる
def review_get_manga_title(review_ids):
    manga_titles = []
    for review_id in review_ids:
        review_query = review_doc_ref.document(review_id)
        review_doc = review_query.get()
        
        if review_doc.exists:
            reivew_data = review_doc.to_dict()
            if reivew_data['evaluation'] >= 4:
                manga_titles.append(reivew_data['mangaTitle'])    
    
    return manga_titles
            
# 漫画取得用API
@comic_bp.route('/api/comics', methods = ['GET'])
def api_comics():
    user_id = session.get('user_id')
    logged_in = True if user_id else False
        
    sort_option = request.args.get('sort_option', 'recommendations')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 8))
    
    # print(sort_option)
    
    if sort_option == "recommendations" and not logged_in:
        return jsonify({'message': 'ログインすると見ることができるようになります！'}), 401
    
    # ソートオプションに基づいた漫画のタイトルをとってくる
    comics_title = []
    if sort_option == "trending":
        comics_data = most_review_comics(7)
        comics_title = [title for title, _ in comics_data]
    elif sort_option == "reviews":
        comics_data = most_review_comics()
        comics_title = [title for title, _ in comics_data]
    elif sort_option == "bookmarks":
        comics_data = most_bookmark_comics()
        comics_title = [comic["title"] for comic in comics_data]
    elif sort_option == "ratings":
        comics_data = high_evaluate_comics()
        comics_title = [comic["title"] for comic in comics_data]
    elif sort_option == "recommendations":
        connected_user_ids = get_user_queries_and_follows(user_id)
        review_ids = get_review_query(user_id)
        comics_title = get_bookmarks(connected_user_ids) + review_get_manga_title(review_ids)

    # print("comics_data:", comics_title)
    
    # ページネーションのための処理
    start = (page - 1) * page_size
    end = start + page_size
    
    # 本の名前から本の情報をとってくる
    comics_info = []
    for title in comics_title[start:end]:
        comics_data = search_comics(title)
        comics_info.extend(comics_data)
        
    # print("comics:", comics_info)
        
    return jsonify({'comics': comics_info})

@comic_bp.route('/comic', methods = ['GET'])
def comic():
    user_id = session.get('user_id')
    logged_in = True if user_id else False
    return render_template("comic.html", logged_in=logged_in)