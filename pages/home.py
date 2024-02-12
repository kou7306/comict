from flask import Blueprint, render_template, request, redirect, session, flash, url_for, get_flashed_messages
from firebaseSetUp import auth, db
from funcs.get_book import get_rakuten_book_cover
from funcs.get_book import get_yahoo_book_cover

home_bp = Blueprint('home', __name__)
user_doc_ref = db.collection('user')
review_doc_ref=db.collection('review')
# ユーザーデータベースにいれるときのデータの型
user_format={
    "gender":None,
    "mangaAnswer":[],
    "bookmark":[],
    "username":None,
    "follow":[],
    "user_query":[],
    "review_query":[],
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
    # loginしている場合
    if logged_in:
        user=user_doc_ref.document(user_id).get()


        # flagが2の時イントロダクションを表示
        
        # 漫画の画像取得
        favolite_book_urls = []
        book_urls=[]
        titles=[]
        if user.to_dict()['review_query'] != None:
            for id in user.to_dict()['review_query']:
                review=review_doc_ref.document(id).get()
                eval=review.to_dict()["evaluation"]
                # 4以上の評価のものだけ取得
                if(int(eval)>=4):
                    title=review.to_dict()["mangaTitle"]  
                    titles.append(title)
                    #image=get_rakuten_book_cover(title)
                    image=get_yahoo_book_cover(title)
                    book_urls.append(image)
            data=list(zip(titles,book_urls))
        else:    
            data = []

        # フォロワーの情報を取得
        follow_data = []
        
        if user.to_dict()["follow"] != None:
            for follow_id in user.to_dict()["follow"]:
                if follow_id != "":
                    follow_doc = user_doc_ref.document(follow_id).get()
                    if follow_doc.exists:
                        follow_name = follow_doc.to_dict()["username"]
                        follow_data.append((follow_name, follow_id))
       
        else:
            follow_data = []
        # お気に入り漫画の画像取得
        if user.to_dict()['user_query'] != None:
            for id in user.to_dict()['user_query']:
                if user_doc_ref.document(id).get().to_dict()["bookmark"] != None:
                    favorite_titles = user_doc_ref.document(id).get().to_dict()["bookmark"]

                    for title in favorite_titles:    
                        image=get_rakuten_book_cover(title)
                        favolite_book_urls.append(image) 
        else:
            favolite_book_urls = []





        # セッションに保存されたフラグの値を取得し、1を加算して再度保存する
        flag = session.get('flag', 0)  # フラグが存在しない場合はデフォルト値として0を使用
        
        print(user_id)
        show_intro = flag == -2
        session['flag'] = flag + 1
        return render_template("home.html",user_id=user_id,user_doc_ref=user_doc_ref,follow_data=follow_data,user_query=user.to_dict()['user_query'],review_query=user.to_dict()['review_query'],data=data,favolite_book_urls=favolite_book_urls,username=user.to_dict()["username"],review_doc_ref=review_doc_ref,show_intro=show_intro,logged_in=logged_in)

    #loginしていない場合
    else:
           # テンプレートにログイン状態（logged_in）を渡す
        return render_template("home.html", logged_in=logged_in, review_doc_ref=review_doc_ref,user_doc_ref=user_doc_ref)
 