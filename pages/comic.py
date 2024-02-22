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
        comics_title = get_bookmarks(connected_user_ids)

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

@comic_bp.route('/comic', methods = ['GET','POST'])
def comic():
    user_id = session.get('user_id')
    logged_in = True if user_id else False
    return render_template("comic.html", logged_in=logged_in)
    
        
        # sort_book_urls = []
        # sort_title = []   
        # # レビュー数が多い漫画   
        # if sort_option == "reviews":

        #         top_comics_names = suggestion_doc_ref.document('all').get().to_dict()['most_review_comics']
        #         for title in top_comics_names:    
        #             sort_title.append(title)
        #             doc_ref=comics_doc_ref.document(title)
        #             comic_data=doc_ref.get().to_dict()
        #             if "image" in comic_data:
        #                 image=comic_data["image"]
        #             else:
        #                 image=get_google_book_cover(title)
                    
        #             sort_book_urls.append(image) 
        #         sort_data = list(zip(sort_title,sort_book_urls))

        # # 一週間以内のレビューが多い漫画
        # elif sort_option == "oneweek_review":

        #         top_comics_names = suggestion_doc_ref.document('oneweek').get().to_dict()['most_review_comics']
        #         for title in top_comics_names:    
        #             sort_title.append(title)
        #             doc_ref=comics_doc_ref.document(title)
        #             comic_data=doc_ref.get().to_dict()
        #             if "image" in comic_data:
        #                 image=comic_data["image"]
        #             else:
        #                 image=get_google_book_cover(title)
                    
        #             sort_book_urls.append(image) 
        #         sort_data = list(zip(sort_title,sort_book_urls))

        # # ブックマークが多い漫画
        # elif sort_option == "bookmarks":

        #         top_comics_names = suggestion_doc_ref.document('all').get().to_dict()['most_bookmark_comics']
        #         for title in top_comics_names:    
        #             sort_title.append(title)
        #             doc_ref=comics_doc_ref.document(title)
        #             comic_data=doc_ref.get().to_dict()
        #             if "image" in comic_data:
        #                 image=comic_data["image"]
        #             else:
        #                 image=get_google_book_cover(title)
                    
        #             sort_book_urls.append(image) 
        #         sort_data = list(zip(sort_title,sort_book_urls))

        # # 高評価の漫画
        # elif sort_option == "ratings":

        #         top_comics_names = suggestion_doc_ref.document('all').get().to_dict()['high_evaluate_comics']
        #         for title in top_comics_names:    
        #             sort_title.append(title)
        #             doc_ref=comics_doc_ref.document(title)
        #             comic_data=doc_ref.get().to_dict()
        #             if "image" in comic_data:
        #                 image=comic_data["image"]
        #             else:
        #                 image=get_google_book_cover(title)
                    
        #             sort_book_urls.append(image) 
        #         sort_data = list(zip(sort_title,sort_book_urls))
            
        # else:

        #     top_comics_names = suggestion_doc_ref.document('all').get().to_dict()['high_evaluate_comics']
            
        #     for title in top_comics_names:    
        #         sort_title.append(title)
             
                
        #         doc_ref=comics_doc_ref.document(title)
        #         comic_data=doc_ref.get().to_dict()
        #         if "image" in comic_data:             
        #             image=comic_data["image"]
        #         else:
                    
        #             image=get_google_book_cover(title)
                    
        #         sort_book_urls.append(image) 
                    
        #     sort_data = list(zip(sort_title,sort_book_urls))
        



        # if logged_in:
        #     user=user_doc_ref.document(user_id).get()


        #     # flagが2の時イントロダクションを表示
            
        #     # 漫画の画像取得
        #     favolite_book_urls = []
        #     book_urls=[]
        #     titles=[]
        #     if user.to_dict()['review_query'] != None:
        #         for id in user.to_dict()['review_query']:
        #             review=review_doc_ref.document(id).get()
        #             eval=review.to_dict()["evaluation"]
        #             # 4以上の評価のものだけ取得
        #             if(int(eval)>=4):
        #                 title=review.to_dict()["mangaTitle"]  
        #                 titles.append(title)
        #                 #image=get_rakuten_book_cover(title)
        #                 doc_ref=comics_doc_ref.document(title)
        #                 comic_data=doc_ref.get().to_dict()
        #                 if "image" in comic_data:
        #                     image=comic_data["image"]
        #                 else:
        #                     image=get_google_book_cover(title)
        #                 book_urls.append(image)
        #         data=list(zip(titles,book_urls))
        #     else:    
        #         data = []

        #     # お気に入り漫画の画像取得
        #     if user.to_dict()['user_query'] != None:
        #         for id in user.to_dict()['user_query']:
        #             if user_doc_ref.document(id).get().to_dict()["bookmark"] != None:
        #                 favorite_titles = user_doc_ref.document(id).get().to_dict()["bookmark"]
        #                 for title in favorite_titles:    
        #                     #image=get_rakuten_book_cover(title)
        #                     doc_ref=comics_doc_ref.document(title)
        #                     comic_data=doc_ref.get().to_dict()
        #                     if "image" in comic_data:
        #                         image=comic_data["image"]
        #                     else:
        #                         image=get_google_book_cover(title)
        #                     favolite_book_urls.append(image) 
        #     else:
        #         favolite_book_urls = []



                 
            # return render_template("comic.html",logged_in=logged_in,data=data,favolite_book_urls=favolite_book_urls,sort_data=sort_data,sort_option=sort_option)
    return render_template('comic.html',logged_in=logged_in, comics=comics_info)
