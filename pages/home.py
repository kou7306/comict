from flask import Blueprint, render_template, request, redirect, session, flash, url_for, get_flashed_messages
from firebaseSetUp import auth, db
from funcs.get_book import get_rakuten_book_cover
from funcs.search import search_comics
from funcs.wiki import get_manga_title
from funcs.review_sort import review_sort

home_bp = Blueprint('home', __name__)
user_doc_ref = db.collection('user')
review_doc_ref=db.collection('review')
comics_doc_ref=db.collection('comics')
suggestion_doc_ref=db.collection('suggestion')
# ユーザーデータベースにいれるときのデータの型
user_format={
    "gender":None,
    "mangaAnswer":[],
    "bookmark":[],
    "username":None,
    "follow":[],
    "user_query":[],
    "comic_query":[],
    "genre":None,   
}


@home_bp.route('/', methods=['POST', 'GET'])
def index():

    return redirect('/home')
    


@home_bp.route('/home', methods=['POST', 'GET'])
def home():
    # セッションからユーザーIDを取得（未ログインの場合はNoneが返る）
    user_id = session.get('user_id')
    if not user_id is None and not user_doc_ref.document(user_id).get().exists:
        return redirect('/login') 
    # ユーザーIDの有無に応じて、テンプレートに渡す変数を設定
    if user_id:
        logged_in = True
    else:
        logged_in = False

    # レビュー数が多い漫画の表示
    # 全期間
    all_review_book_urls = []
    all_review_book_title = []

    # 漫画の検索
    results = []
    if request.method == 'POST':
        search_query = request.form['search_query']
        #results = search_comics(search_query)
        wiki_result = get_manga_title(search_query)
        results=search_comics(wiki_result)

    # 上位の漫画名のみを取り出す
    top_comics_names = suggestion_doc_ref.document('all').get().to_dict()['most_review_comics'][:10]
    for title in top_comics_names:    
        all_review_book_title.append(title)
        doc_ref=comics_doc_ref.document(title)
        comic_data=doc_ref.get().to_dict()
        if comic_data is not None and "image" in comic_data:
            image=comic_data["image"]
        all_review_book_urls.append(image) 

    all_review_book = list(zip(all_review_book_title,all_review_book_urls))

    # 一週間以内
    week_review_book_urls = []
    week_review_book_title = []
    top_comics_names = suggestion_doc_ref.document('oneweek').get().to_dict()['most_review_comics'][:10]
    for title in top_comics_names:    
        week_review_book_title.append(title)
        doc_ref=comics_doc_ref.document(title)
        comic_data=doc_ref.get().to_dict()
        if comic_data is not None and "image" in comic_data:
            image=comic_data["image"]
        week_review_book_urls.append(image)
    week_review_book = list(zip(week_review_book_title,week_review_book_urls))
        

    # ブックマーク数が多い漫画の表示
    bookmark_book_urls = []
    bookmark_book_title = []
    top_comics_names = suggestion_doc_ref.document('all').get().to_dict()['most_bookmark_comics'][:10]
    for title in top_comics_names:    
        bookmark_book_title.append(title)
        doc_ref=comics_doc_ref.document(title)
        comic_data=doc_ref.get().to_dict()
        if comic_data is not None and "image" in comic_data:
            image=comic_data["image"]
        bookmark_book_urls.append(image)
    bookmark_book = list(zip(bookmark_book_title,bookmark_book_urls))


    # 高評価の漫画の表示
    high_evaluate_book_urls = []
    high_evaluate_book_title = []
    top_comics_names = suggestion_doc_ref.document('all').get().to_dict()['high_evaluate_comics'][:10]

    for title in top_comics_names:    
        high_evaluate_book_title.append(title)
        doc_ref=comics_doc_ref.document(title)
        comic_data=doc_ref.get().to_dict()
        if comic_data is not None and "image" in comic_data:
            image=comic_data["image"]
        high_evaluate_book_urls.append(image)
    high_evaluate_book = list(zip(high_evaluate_book_title,high_evaluate_book_urls))


    # ユーザー系
    # レビュー投稿数が多いユーザーの表示
    # 全期間
    all_review_users = suggestion_doc_ref.document('all').get().to_dict()['most_review_users'][:10]


    # 一週間以内
    oneweek_review_users  = suggestion_doc_ref.document('oneweek').get().to_dict()['most_review_users'][:10]


    # フォロワーが多いユーザーの表示
    most_follow_user = suggestion_doc_ref.document('all').get().to_dict()['most_follow_user'][:10]

    # 新着レビュー
    reviews = review_sort('newest',None,limit=5)[:5]

    
    # loginしている場合
    if logged_in:
        user=user_doc_ref.document(user_id).get()


        # flagが2の時イントロダクションを表示
        
        # 漫画の画像取得
        favolite_book_urls = []
        book_urls=[]
        titles=[]
        if user.to_dict()['comic_query'] != None:
            for id in user.to_dict()['comic_query']:
                
           
                title=comics_doc_ref.document(id).get().to_dict()["title"]
                titles.append(title)
                doc_ref=comics_doc_ref.document(title)
                comic_data=doc_ref.get().to_dict()
                if comic_data is not None and "image" in comic_data:
                    image=comic_data["image"]
                book_urls.append(image)
            data=list(zip(titles,book_urls))
        else:    
            data = []

        # フォロワーの情報を取得
        follow_data = []
        
        if user.to_dict()["follow"] != None:
            for follow_id in user.to_dict()["follow"]:
                if follow_id != None:
                    follow_data.append(follow_id)
  
        else:
            follow_data = []
        # お気に入り漫画の画像取得
        # if user.to_dict()['user_query'] != None:
        #     for id in user.to_dict()['user_query']:
        #         doc = user_doc_ref.document(id).get()
        #         if doc.exists and doc.to_dict()["bookmark"] is not None:
        #             favorite_titles = user_doc_ref.document(id).get().to_dict()["bookmark"]

        #             for title in favorite_titles:
        #                 favolite_book_urls.append(image) 
            
        # else:
        #     favolite_book_urls = []

        # マッチングしたユーザー
        if user.to_dict()['user_query'] != None:
            user_query = user.to_dict()['user_query']





        # セッションに保存されたフラグの値を取得し、1を加算して再度保存する
        flag = session.get('flag', 0)  # フラグが存在しない場合はデフォルト値として0を使用
        
        print(user_id)
        show_intro = flag == -2
        session['flag'] = flag + 1
        return render_template("home.html",user_id=user_id,user_doc_ref=user_doc_ref,follow_data=follow_data,user_query=user_query,comic_query=user.to_dict()['comic_query'],data=data,favolite_book_urls=favolite_book_urls,username=user.to_dict()["username"],review_doc_ref=review_doc_ref,show_intro=show_intro,logged_in=logged_in,all_review_book=all_review_book,week_review_book=week_review_book,bookmark_book=bookmark_book,high_evaluate_book=high_evaluate_book,all_review_users=all_review_users,oneweek_review_users=oneweek_review_users,most_follow_user=most_follow_user,results=results, comics_doc_ref=comics_doc_ref, reviews=reviews)

    #loginしていない場合
    else:
           # テンプレートにログイン状態（logged_in）を渡す
        return render_template("home.html", logged_in=logged_in, review_doc_ref=review_doc_ref,user_doc_ref=user_doc_ref,all_review_book=all_review_book,week_review_book=week_review_book,bookmark_book=bookmark_book,high_evaluate_book=high_evaluate_book,all_review_users=all_review_users,oneweek_review_users=oneweek_review_users,most_follow_user=most_follow_user,results=results, comics_doc_ref=comics_doc_ref, reviews=reviews)
 