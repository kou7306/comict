from flask import Flask, render_template, request, jsonify, redirect, session, url_for, flash, get_flashed_messages
import pyrebase
import faiss
import numpy as np
import firebase_admin
from firebase_admin import credentials,firestore
from bs4 import BeautifulSoup
import requests
import os


# # サービス アカウント キー ファイルへのパスを環境変数から取得
# firebase_admin_key_path = os.environ'FIREBASE_ADMIN_KEY_PATH')

# Firebase Admin SDK を初期化
cred = credentials.Certificate('key.json')

firebase_admin.initialize_app(cred)
db = firestore.client()

user_doc_ref = db.collection('user')

all_user = user_doc_ref.stream()

review_doc_ref=db.collection('review')

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
}

# レビューデータベースに入れるときのデータの型
review_format={
    "mangaTitle":None,
    "evaluation":None,
    "contents":None,
    "username":None,
}

app = Flask(__name__)
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
    for user in all_user:
        if(user.id!=user_id): # 自分以外
            all_user_vector.append(user.to_dict()["mangaAnswer"])
            all_users.append(user.to_dict())
    if(all_user_vector != []):
        # Faissインデックスの作成
        dimension = len(all_user_vector[0])  # ベクトルの次元数
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(all_user_vector, dtype=np.float32))
        
        # 最近傍のベクトルを検索
        _, indices = index.search(np.array([mangaAnswer], dtype=np.float32), k=5)
        
        # 結果の値だけを取り出す
        nearest_values_users = [all_users[i] for i in indices[0]]
        
        # 対象ユーザーのレビューした情報のIDを取り出す
        review_query_results = []
        user_query_results = []
        
        for user in nearest_values_users:
            # usernameが一致するレビューデータをすべて取り出す
            review_query_result = review_doc_ref.where('username', '==', user["username"]).stream()
            print(user_query_result)
            print(review_query_result)
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
        if(user.to_dict()["mangaAnswer"]==[99.0 for x in range(160)]):
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
    book_urls=[]
    titles=[]
    for id in user.to_dict()['review_query']:
        review=review_doc_ref.document(id).get()
        title=review.to_dict()["mangaTitle"]  
        titles.append(title)
        image=get_rakuten_book_cover(title)
        book_urls.append(image)
    data=list(zip(titles,book_urls))

    # フォロワーの情報を取得
    reviewer_queries=[]  
    for follower in user.to_dict()["follow"]:
        reviewer_queries.append(user_doc_ref.where('username', '==', follower).get())
    
    return render_template("home.html",user_id=user_id,user_doc_ref=user_doc_ref,reviewer_query=reviewer_queries,user_query=user.to_dict()['user_query'],review_query=user.to_dict()['review_query'],data=data)



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
                user_format["mangaAnswer"]= [99.0 for x in range(160)]
                user_format["gender"]=gender
                user_doc.set(user_format)

                flash("ユーザー登録が完了しました")
                return redirect(f"/{user_id}/question")
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
        mangaAnswer = [0] *160
        genre=int(genre)
        first_index = 20 * (genre - 1)

        #HTMLフォームからデータを受け取る
        for i in range(1,6):
            question_key = f'question-{i:02}'
            answer = request.form[question_key]
            answer=float(answer)
            mangaAnswer[first_index + (i-1)]=answer
            
        # Firestoreから指定したuser_idに対応するユーザーネームを取得
        user_doc = user_doc_ref.document(user_id)
        user=user_doc.get()
        # データベースにデータを格納
        user_format['gender']=user.to_dict()["gender"]
        user_format['mangaAnswer']=mangaAnswer
        user_format['username']=user.to_dict()["username"]


        # マッチング
        review_query, user_query =matching(user.to_dict()["mangaAnswer"],user_id)
        user_format['user_query']=user_query
        user_format['review_query']=review_query
        user_doc.set(user_format)
        # 漫画の画像取得
        book_urls=[]
        titles=[]
        for id in review_query:
            review=review_doc_ref.document(id).get()
            title=review.to_dict()["mangaTitle"]  
            titles.append(title)
            image=get_rakuten_book_cover(title)
            book_urls.append(image)
        data=list(zip(titles,book_urls))

        # フォロワーの情報を取得
        reviewer_queries=[]  
        for follower in user.to_dict()["follow"]:
            reviewer_queries.append(user_doc_ref.where('username', '==', follower).get())

        username=user.to_dict()["username"]
        
        return render_template("home.html",user_id=user_id,user_doc_ref=user_doc_ref,reviewer_query=reviewer_queries,user_query=user_query,review_query=review_query,data=data,username=username)


       

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
        return redirect(f"/{user_id}/review")






@app.route('/<user_id>/userpage', methods=['GET', 'POST'])
def user_page(user_id):   

    user_doc = user_doc_ref.document(user_id)
    user=user_doc.get()
    user_data=user.to_dict()
    username=user.to_dict()["username"]
    # 特定のユーザーネームに一致するドキュメントを取得
    query = review_doc_ref.where('username', '==', username).get()

    # アンケート結果の取得・表示
    with open('templates/question.html', 'r', encoding='utf-8') as file:
        html_code = file.read()
    result = user_data.get('mangaAnswer')

    #アンケートの設問と回答を格納する配列
    question, answer = [], []
    soup = BeautifulSoup(html_code, 'html.parser')

    #アンケートの設問を取得
    h2_elems = soup.find_all('h2')
    for h2 in h2_elems:
        question.append(h2.text)

    #アンケートの回答を取得
    temp = []
    for value_to_find in result:
        value_to_find=int(value_to_find)
        value_to_find=str(value_to_find)
        input_tags = soup.find_all('input', {'value': value_to_find})
        for input_tag in input_tags:
            label_tag = soup.find('label', {'for': input_tag.get('id')})
            if label_tag:
                temp.append(label_tag.text)
    for i in range(20):
        answer.append(temp[i])

    #設問と回答をタプル化
    combined_list = zip(question, answer)

    #好きな作品のリストをデータベースから取得
    favorite_titles = user.to_dict()["favorite_manga"]

    return render_template("userpage.html", query=query,username=username, user_id=user_id, result=result, combined_list=combined_list, favorite_titles=favorite_titles)


  
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
        reviewer_doc = user_doc_ref.document(reviewer_id).get()
        reviewername=reviewer_doc.to_dict()["username"]
        user_doc = user_doc_ref.document(user_id)
        user_data = user_doc.get().to_dict()
        current_follow = user_data.get("follow", [])
        if(is_following):

            current_follow.append(reviewername)
        else:
            current_follow.remove(reviewername)
        # 更新するデータを作成
        update_data = {"follow": current_follow}
        # ドキュメントを更新
        user_doc.update(update_data)


        # フォロー状態をクライアントに返す
        return jsonify({'isFollowing': is_following})
    
# 作品詳細ページ
@app.route('/<user_id>/<title>/detail')
def detail(user_id,title):
    query = review_doc_ref.where('mangaTitle', '==', title).get()
    
    
    return render_template("detail.html",user_id=user_id,title=title,query=query)


# 好きな作品を追加
@app.route('/<user_id>/favoriteAdd', methods=['GET', 'POST'])
def add_manga(user_id):
    user_doc = user_doc_ref.document(user_id)
    user=user_doc.get()
    favorite_titles =user.to_dict()["favorite_manga"]
    if request.method == 'GET':
        return render_template('favoriteAdd.html', user_id=user_id, favorite_titles=favorite_titles) 
    elif request.method == 'POST':
        manga_title = request.form['favorite_title'] # 'favorite_title'から取得
        # ドキュメントの更新
        user_doc.update({
            'favorite_manga': firestore.ArrayUnion([manga_title])
        })

        # ユーザーデータの取得
        user_data = user_doc.get().to_dict()
        favorite_titles = user_data.get('favorite_manga', [])  # favorite_mangaが存在しない場合は空のリストを使う
        return render_template('favoriteAdd.html', user_id=user_id, favorite_titles=favorite_titles) 

if __name__ == '__main__':
    app.run(debug=True,port=5002)