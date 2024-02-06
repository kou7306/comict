from flask import Flask, render_template, request, jsonify, redirect, session, current_app,url_for, flash, get_flashed_messages
import pyrebase
import faiss
import numpy as np
import firebase_admin
from firebase_admin import credentials,firestore
from bs4 import BeautifulSoup
import requests
import os
import wikipedia
from wiki import get_manga_title,get_wikipedia_page_details



# # サービス アカウント キー ファイルへのパスを環境変数から取得


# firebase_admin_key_path = os.environ.get('FIREBASE_ADMIN_KEY_PATH')
app = Flask(__name__)

# Firebase Admin SDK を初期化
cred = credentials.Certificate("key.json")

firebase_admin.initialize_app(cred)
db = firestore.client()
user_doc_ref = db.collection('user')

all_user = user_doc_ref.stream()

review_doc_ref=db.collection('review')

comics_doc_ref=db.collection('comics')

is_following=False




# ユーザーデータベースにいれるときのデータの型
user_format={
    "gender":None,
    "mangaAnswer":[],
    "favorite_manga":[],
    "username":None,
    "follow":[],
    "user_query":[],
    "review_query":[],
    "genre":None,   
}

# レビューデータベースに入れるときのデータの型
review_format={
    "mangaTitle":None,
    "evaluation":None,
    "contents":None,
    "username":None,
}

config = {
    "apiKey": "AIzaSyBPva6sGWXi6kjmk8mjWWVCGEKKEBIfTIY",
    "authDomain": "giikucamp12.firebaseapp.com",
    "projectId": "giikucamp12",
    "storageBucket": "giikucamp12.appspot.com",
    "messagingSenderId": "755980381836",
    "appId": "1:755980381836:web:acdae710db8366cc4095a9",
    "measurementId": "G-00EVCKC0JQ",
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

app.secret_key = "secret"

# 楽天ブックスAPIを叩く関数
def get_rakuten_book_cover(book_title):
    api_key = '1078500249535096776'
    base_url = 'https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404'

    params = {
        'format': 'json',
        'applicationId': api_key,
        'title': book_title,
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if 'Items' in data and data['Items']:
        first_item = data['Items'][0]['Item']
        image_url = first_item.get('largeImageUrl', first_item.get('mediumImageUrl', 'Image not available'))
        return image_url
    else:
        return "no"



# マッチング関数
def matching(mangaAnswer,user_id):
    # データベースにあるすべてのユーザーデータを取得
    all_user_vector = []
    all_users = []
    all_user = user_doc_ref.stream()
    
    if(all_user == []):
        print("データがありません")
    for user in all_user:
        print(user.to_dict()["mangaAnswer"])
        if(user.id!=user_id): # 自分以外
            
            print('データ',user.to_dict()["mangaAnswer"])
            all_user_vector.append(user.to_dict()["mangaAnswer"])
            all_users.append(user.to_dict())
    
    if(all_user_vector != []):
        # Faissインデックスの作成
        dimension = len(all_user_vector[0])  # ベクトルの次元数
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(all_user_vector, dtype=np.float32))
        
        # 最近傍のベクトルを検索
        _, indices = index.search(np.array([mangaAnswer], dtype=np.float32), k=1)
        
        # 結果の値だけを取り出す
        nearest_values_users = [all_users[i] for i in indices[0]]
        
        # 対象ユーザーのレビューした情報のIDを取り出す
        review_query_results = []
        user_query_results = []
        
        for user in nearest_values_users:
            # usernameが一致するレビューデータをすべて取り出す
            review_query_result = review_doc_ref.where('username', '==', user["username"]).stream()
            user_query_result = user_doc_ref.where('username', '==', user["username"]).stream()
            for doc in review_query_result:
                review_query_results.append(doc.id)
            for doc in user_query_result:
                user_query_results.append(doc.id)

        
        return review_query_results, user_query_results
    return None,None




@app.route("/<user_id>/accesTest")
def accesTest(user_id):
    if 'user' in session:
        user=user_doc_ref.document(user_id).get()
        if(user.to_dict()["mangaAnswer"]==[99.0 for x in range(140)]):
            return redirect(f"/{user_id}/genre")
        else:
            return redirect(f"/{user_id}/home")

    else:
        flash("ログインしてください")
        return redirect("/")




# home
@app.route('/<user_id>/home')
def homepage(user_id):
    user=user_doc_ref.document(user_id).get()
    
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
                image=get_rakuten_book_cover(title)
                book_urls.append(image)
        data=list(zip(titles,book_urls))
    else:    
        data = []

    # フォロワーの情報を取得
    follow_data = []
    
    if user.to_dict()["follow"] != None:
        for follow_id in user.to_dict()["follow"]:
            if follow_id != "":
                print(follow_id)
                follow_doc = user_doc_ref.document(follow_id).get()
                if follow_doc.exists:
                    follow_name = follow_doc.to_dict()["username"]
                    follow_data.append((follow_name, follow_id))
                print(follow_data)
    else:
        follow_data = []
    # お気に入り漫画の画像取得
    if user.to_dict()['user_query'] != None:
        for id in user.to_dict()['user_query']:
            favorite_titles = user_doc_ref.document(id).get().to_dict()["favorite_manga"]
            if favorite_titles != None:
                for title in favorite_titles:    
                    image=get_rakuten_book_cover(title)
                    favolite_book_urls.append(image) 
    else:
        favolite_book_urls = []
    
    return render_template("home.html",user_id=user_id,user_doc_ref=user_doc_ref,follow_data=follow_data,user_query=user.to_dict()['user_query'],review_query=user.to_dict()['review_query'],data=data,favolite_book_urls=favolite_book_urls,username=user.to_dict()["username"],review_doc_ref=review_doc_ref)



@app.route("/reset", methods=['POST', 'GET'])
def reset():
    if request.method == 'POST':
        email = request.form.get('email')
        try:
            auth.send_password_reset_email(email)
            flash("パスワード再設定メールを送信しました")
            return redirect("/")
        except:
            flash("パスワード再設定メールの送信に失敗しました")
            return redirect("/")
    else:
        return render_template("reset.html")
    


# login
@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        username=request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
            # usernameが一致する最初のドキュメントを取得
            query = user_doc_ref.where('username', '==', username).limit(1)
            result = query.stream()

            # ドキュメントが存在すればそのIDを返す
            for doc in result:            
                return redirect(f'/{doc.id}/accesTest')
            flash("ユーザー名が登録されていません")
            return redirect("/")
        except:
                flash("ログインに失敗しました")
                return redirect("/")  
    else:
        messages = get_flashed_messages()
        return render_template("login.html", messages=messages)

# ユーザーネームの重複を確認する関数
def is_username_duplicate(username):
    # usersコレクションからユーザーネームが一致するドキュメントをクエリ
    query = user_doc_ref.where('username', '==', username)
    
    # クエリを実行して結果を取得
    query_result = query.stream()

    # クエリ結果が空でない場合は重複していると判断
    return any(query_result)

# ユーザー登録
@app.route("/userAdd", methods=['POST', 'GET'])
def userAdd():
    if request.method == 'POST':
        username=request.form.get('username')
        gender=request.form.get('gender')
        email = request.form.get('email')
        password = request.form.get('password')
        # usernameが重複していない場合
        if not is_username_duplicate(username):
            try:
                auth.create_user_with_email_and_password(email, password)
                
                # userのidを取得
                user_id=user_doc_ref.document().id
                # userデータベースに保存
                user_doc=user_doc_ref.document(user_id)
                user_format["username"]=username
                # デフォルトで外れ値を指定しておく
                user_format["mangaAnswer"]= [99.0 for x in range(140)]
                user_format["gender"]=gender
                user_doc.set(user_format)

                flash("ユーザー登録が完了しました")
                return redirect(f"/{user_id}/genre")
            except:
                flash("ユーザー登録に失敗しました")
                return redirect("/")
            
        else:
            flash("ユーザーネームが重複しています")
            return redirect("/")    
    else:
        return render_template("userAdd.html")

@app.route("/logout")
def logput():
    session.pop('user', None)
    flash("ログアウトしました")
    return redirect('/')

# ジャンル選択
@app.route("/<user_id>/genre",methods = ['GET',"POST"])
def genre(user_id):
    if request.method == 'GET':
        return render_template("genre.html",user_id=user_id)
    else:
        # フォームからジャンルを取得し、データベースに追加
        genre = request.form['genre']
        update_data = {"genre":genre}
        user_doc = user_doc_ref.document(user_id)
        user_doc.update(update_data)
        return redirect(f'/{user_id}/{genre}/question')



# アンケート回答を受信
@app.route('/<user_id>/<genre>/question', methods = ['GET','POST'])
def question(user_id,genre):
    if request.method == 'GET':
        return render_template("question"+ genre + '.html',user_id=user_id,genre=genre)
    else:

        #長さ20*８のリストを作成し、０で初期化する
        mangaAnswer = [0.0] *140

        genre=int(genre)
        first_index = 20 * (genre - 1)

        #HTMLフォームからデータを受け取る
        for i in range(1,20):
            question_key = f'question-{i:02}'
            answer = request.form[question_key]
            answer=float(answer)
            mangaAnswer[first_index + (i-1)]=answer
            
        # Firestoreから指定したuser_idに対応するユーザーネームを取得
        user_doc = user_doc_ref.document(user_id)
        user=user_doc.get()
        # データベースにデータを格納

        user_doc.update({'gender':  user.to_dict()["gender"],'mangaAnswer':mangaAnswer,'username':user.to_dict()["username"]})
        # マッチング
        review_query, user_query =matching(user.to_dict()["mangaAnswer"],user_id)
       
        update_data = {"user_query":  user_query,"review_query":review_query}
        user_doc.update(update_data)
     
        
        return redirect(f'/{user_id}/home')


       

# レビュー投稿
@app.route('/<user_id>/review',methods=['GET','POST'])
def review(user_id):
    if request.method == 'GET':
        return render_template("review.html",user_id=user_id)
    else:
        # formから取得
        work_name = request.form['work_name']
        rating = request.form['rating']
        comment = request.form['comment_text']
        # Firestoreから指定したuser_idに対応するユーザーネームを取得
        user_doc = user_doc_ref.document(user_id)
        user=user_doc.get()
        

        # 入力されたレビューのデータ
        review_format["evaluation"]=rating
        review_format["mangaTitle"]=work_name
        review_format["contents"]=comment
        review_format["username"]=user.to_dict()["username"]
        review_document=review_doc_ref.document() 
        review_document.set(review_format)

        # 作品データベースに初登録の作品なら追加
        if(comics_doc_ref.document(work_name).get().to_dict()==None):
            url=get_wikipedia_page_details(work_name)
            comics_doc_ref.document(work_name).set({"title": work_name,"bookmark":[],"url":url,"reviews":[],"author":None})
        return redirect(f"/{user_id}/review")





# ユーザーページ
@app.route('/<user_id>/userpage', methods=['GET', 'POST'])
def user_page(user_id):   

    user_doc = user_doc_ref.document(user_id)
    user=user_doc.get()
    user_data=user.to_dict()
    username=user.to_dict()["username"]
    # 特定のユーザーネームに一致するドキュメントを取得
    query = review_doc_ref.where('username', '==', username).get()

    # アンケート結果の取得・表示 ここの修正が必要
    # with open('templates/question1.html', 'r', encoding='utf-8') as file:
    #     html_code = file.read()
    # result = user_data.get('mangaAnswer')

    # #アンケートの設問と回答を格納する配列
    # question, answer = [], []
    # soup = BeautifulSoup(html_code, 'html.parser')

    # #アンケートの設問を取得
    # h2_elems = soup.find_all('h2')
    # for h2 in h2_elems:
    #     question.append(h2.text)

    # #アンケートの回答を取得
    # temp = []
    # for value_to_find in result:
    #     value_to_find=int(value_to_find)
    #     value_to_find=str(value_to_find)
    #     input_tags = soup.find_all('input', {'value': value_to_find})
    #     for input_tag in input_tags:
    #         label_tag = soup.find('label', {'for': input_tag.get('id')})
    #         if label_tag:
    #             temp.append(label_tag.text)
    # for i in range(5):
    #     answer.append(temp[i])

    # #設問と回答をタプル化
    # combined_list = zip(question, answer)

    #ブックマークをデータベースから取得
    favorite_titles = user_data["favorite_manga"]

    # フォローしたユーザーのIDを取得
    follow_data = []
    for follow_id in user_data["follow"]:
        follow_doc = user_doc_ref.document(follow_id).get()
        if follow_doc.exists:
            follow_name = follow_doc.to_dict()["username"]
            follow_data.append((follow_name, follow_id))
 
 

 


    return render_template("userpage.html", myreview_query=query,username=username, user_id=user_id, result="a", combined_list="a", favorite_titles=favorite_titles,follow_data=follow_data)


  
# reviewer page
@app.route('/<user_id>/<reviewer_id>/userpage', methods = ['GET','POST'])
def reviewer(user_id,reviewer_id):
    if request.method == 'GET':

        # レビュワーの情報をとってくる
        reviewer_doc = user_doc_ref.document(reviewer_id).get()
        reviewername=reviewer_doc.to_dict()["username"]
        # 特定のユーザーネームに一致するレビュー情報を取得
        query = review_doc_ref.where('username', '==', reviewername).get()

        # そのユーザーをフォローしてるか
        user_doc = user_doc_ref.document(user_id)
        # 'follow' フィールド中に 'reviewername' が含まれているか確認
        is_following = any(user == reviewername for user in user_doc.get().to_dict()['follow'])


        favorite_titles = reviewer_doc.to_dict().get('favorite_manga', [])  # favorite_titlesが存在しない場合は空のリストを使う
        return render_template("reviewerpage.html",query=query,username=reviewername,reviewer_id=reviewer_id,user_id=user_id,is_following=is_following,favorite_titles=favorite_titles)
    else:
        data = request.get_json()
        is_following = data.get('is_following')

        # フォロー状態をトグル
        is_following = not is_following
        # レビュワーの情報をとってくる
        # reviewer_doc = user_doc_ref.document(reviewer_id).get()
        # reviewername=reviewer_doc.to_dict()["username"]
        user_doc = user_doc_ref.document(user_id)
        user_data = user_doc.get().to_dict()
        current_follow = user_data.get("follow", [])
        if(is_following):
            print("reviewer_id",reviewer_id)
            current_follow.append(reviewer_id)
        else:
            current_follow.remove(reviewer_id)
        # 更新するデータを作成
        update_data = {"follow":  current_follow}
        # ドキュメントを更新
        user_doc.update(update_data)


        # フォロー状態をクライアントに返す
        return jsonify({'isFollowing': is_following})
    
# 作品詳細ページ
@app.route('/<user_id>/<title>/detail')
def detail(user_id,title):
    # 詳細情報をwikiから取得
    query = review_doc_ref.where('mangaTitle', '==', title).get()
    url = comics_doc_ref.document(title).get().to_dict()["url"]
    bookmark_num = len(comics_doc_ref.document(title).get().to_dict()["bookmark"])
    
    
    return render_template("detail.html",user_id=user_id,title=title,query=query,url=url,bookmark_num=bookmark_num)


# 好きな作品を追加
@app.route('/<user_id>/favoriteAdd', methods=['GET', 'POST'])
def add_manga(user_id):
    user_doc = user_doc_ref.document(user_id)
    user=user_doc.get()
    favorite_titles = user.to_dict().get("favorite_manga", [])
    if request.method == 'GET':
        return render_template('favoriteAdd.html', user_id=user_id, favorite_titles=favorite_titles) 
    elif request.method == 'POST':
        data = request.get_json()
        manga_title = data.get('title') 
        print(manga_title)
        # ドキュメントの更新
        user_doc.update({
            'favorite_manga': firestore.ArrayUnion([manga_title])
        })

        # ユーザーデータの取得
        user_data = user_doc.get().to_dict()
        favorite_titles = user_data.get('favorite_manga', [])  #favorite_mangaが存在しない場合は空のリストを使う
        return jsonify({'favoriteTitles': favorite_titles})

PER_PAGE = 10

# 作品検索機能
def search_books(search_type, search_input, sort_option, page):
        
    # Firestoreクエリを作成
    if search_type == "title":
        query = comics_doc_ref.where('title', '>=', search_input).where('title', '<=', search_input + '\uf8ff')

    elif search_type == "author":
        query = comics_doc_ref.where('author', '>=', search_input).where('author', '<=', search_input + '\uf8ff')
    
    
    start_index = (page - 1) * PER_PAGE
    query = query.offset(start_index).limit(PER_PAGE)
    
    docs = query.stream()
    
    # クエリ結果をリストに変換
    results = [{'id': doc.id, **doc.to_dict()} for doc in docs]
    
    # ソート処理
    if sort_option == "b_asc":
        results = sorted(results, key=lambda x: len(x['bookmark']))
    elif sort_option == "b_desc":
        results = sorted(results, key=lambda x: len(x['bookmark']), reverse=True)
    elif sort_option == "r_asc":
        results = sorted(results, key=lambda x: len(x['reviews']))
    elif sort_option == "r_desc":
        results = sorted(results, key=lambda x: len(x['reviews']), reverse=True)
        
    return results, len(results)

@app.route('/<user_id>/bookSearch', methods=['POST', 'GET'])
def BookSearch(user_id):
    if request.method == 'POST':
        search_type = request.form.get('searchType')
        search_input = request.form.get('searchInput').strip()
        sort_option = request.form.get('sortOption')
        page = request.args.get('page', 1)
        
        print(search_input)
        if search_input:
            results, num_results = search_books(search_type, search_input, sort_option, page)
            if num_results == 0:
                results = []
            
            response = {
                "results": results,
                "num_results": num_results,
                "user_id": user_id
            }
            
            return jsonify(response)
        else:
            return jsonify({"error": "検索ワードを入力してください"})
    else:
        return render_template('bookSearch.html',user_id=user_id)


# 漫画の正式タイトルを取得
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    
    if query:
        manga_title = get_manga_title(query)
        return jsonify({'manga_title': manga_title})


# ブックマーク機能
@app.route("/<user_id>/bookmark", methods=["POST"])
def toggle_bookmark(user_id):
    data = request.get_json()

    # 漫画のタイトルを取得
    title = data.get("title")

    # データベースでブックマークの状態をトグル

    comics_doc = comics_doc_ref.document(title)
    
    # ブックマークの状態を取得
    comics_data = comics_doc.get()
    
    if comics_data.exists:
        current_bookmark = comics_data.to_dict().get("bookmark", [])
    else:
        current_bookmark = []


    # 新しいユーザーIDをブックマークリストに追加
    if user_id not in current_bookmark:
        current_bookmark.append(user_id)
        comics_doc.update({"bookmark": current_bookmark})
        new_bookmark_value = len(current_bookmark) # ブックマーク数を取得
    else:
        current_bookmark.remove(user_id)
        comics_doc.update({"bookmark": current_bookmark})
        new_bookmark_value = len(current_bookmark)

    return jsonify({"bookmarked": new_bookmark_value})

if __name__ == '__main__':
    app.run(debug=True,port=8080)

# /fm8MhfrbKdJ5narcJvTm/home testへのURL