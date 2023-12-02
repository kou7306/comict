from flask import Flask, render_template, request, jsonify, redirect, session, url_for, flash, get_flashed_messages
import pyrebase
import faiss
import numpy as np
import firebase_admin
from firebase_admin import credentials,firestore
from bs4 import BeautifulSoup


# データベースの準備等
cred = credentials.Certificate("key.json")

firebase_admin.initialize_app(cred)
db = firestore.client()

user_doc_ref = db.collection('user')
all_user = user_doc_ref.get()

review_doc_ref=db.collection('review')


# ユーザーデータベースにいれるときのデータの型
user_format={
    "gender":None,
    "mangaAnswer":[],
    "username":None,
    "フォロワー数":0,
    "フォロー数":0,
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

@app.route("/<user_id>/accesTest")
def accesTest(user_id):
    if 'user' in session:
        return redirect(f"/{user_id}/question")
    else:
        flash("ログインしてください")
        return redirect("/")

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
    query = user_doc_ref .where('username', '==', username)
    
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
                user_format["mangaAnswer"]=[99.0,99.0,99.0,99.0,99.0,99.0,99.0,99.0,99.0,99.0,99.0,99.0,99.0,99.0,99.0,99.0,99.0,99.0,99.0,99.0]
                user_format["gender"]=gender
                user_doc.set(user_format)

                flash("ユーザー登録が完了しました")
                return redirect(f"/{user_id}/question")
            except:
                flash("ユーザー登録に失敗しました")
                print(user_id)
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



# アンケート回答を受信
@app.route('/<user_id>/question', methods = ['GET','POST'])
def question(user_id):
    if request.method == 'GET':
        return render_template("question.html",user_id=user_id)
    else:
        mangaAnswer = []

        #HTMLフォームからデータを受け取る
        for i in range(1,21):
            question_key = f'question-{i:02}'
            answer = request.form.get(question_key)
            answer=float(answer)
            mangaAnswer.append(answer)
            
        # Firestoreから指定したuser_idに対応するユーザーネームを取得
        user_doc_ref = db.collection('user').document(user_id)
        user_doc=user_doc_ref.get()
        # データベースにデータを格納
        user_format['gender']=user_doc.to_dict()["gender"]
        user_format['mangaAnswer']=mangaAnswer
        user_format['username']=user_doc.to_dict()["username"]
        user_doc_ref.set(user_format)


        # マッチング
        # データベースにあるすべてのユーザーデータを取得
        all_user_vector=[]
        all_users=[]
        for user in all_user:
            all_user_vector.append(user.to_dict()["mangaAnswer"])
            all_users.append(user.to_dict())

        # Faissインデックスの作成
        dimension = len(all_user_vector[0])  # ベクトルの次元数
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(all_user_vector, dtype=np.float32))
        # 最近傍のベクトルを検索
        _, indices = index.search(np.array([mangaAnswer], dtype=np.float32), k=2)
        # 結果の値だけを取り出す
        nearest_values_users = [all_users[i] for i in indices[0]]
        # 対象ユーザーのレビューした作品名を取り出す
        title_data=[]
        for user in nearest_values_users:
            # usernameが一致するレビューデータをすべて取り出す
            query = review_doc_ref.where('username', '==', user["username"])
            # クエリを実行して結果を取得
            query_result = query.get()

            # 一人のレビュワーの全てのレビューした漫画のデータを取り出す
            for doc in query_result:
                title_data.append(doc.to_dict()["mangaTitle"])
        return render_template("home.html",user_id=user_id,review_users=nearest_values_users,title_data=title_data)


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
        user_doc_ref = db.collection('user').document(user_id)
        user_doc=user_doc_ref.get()

        # 入力されたレビューのデータ
        review_format["evaluation"]=rating
        review_format["mangaTitle"]=work_name
        review_format["contents"]=comment
        review_format["username"]=user_doc.to_dict()["username"]
        review_document=review_doc_ref.document() 
        review_document.set(review_format)
        return redirect(f"/{user_id}/review")




@app.route('/home')
def iho():
    return render_template("home.html")


@app.route('/<user_id>/userpage', methods=['GET', 'POST'])
def user_page(user_id):   
    user_doc_ref = db.collection('user').document(user_id)
    user_doc=user_doc_ref.get()
    user_data=user_doc.to_dict()
    username=user_doc.to_dict()["username"]
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

    return render_template("userpage.html", query=query,username=username, user_id=user_id, result=result, combined_list=combined_list)

if __name__ == '__main__':
    app.run(debug=False)
