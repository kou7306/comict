from flask import Flask, render_template, request, jsonify, redirect, session, url_for, flash, get_flashed_messages
import pyrebase
import faiss
import numpy as np
import firebase_admin
from firebase_admin import credentials,firestore

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

@app.route("/accesTest")
def accesTest():
    if 'user' in session:
        return redirect("/question")
    else:
        flash("ログインしてください")
        return redirect("/")

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
            return redirect(url_for('accesTest'))
        except:
            flash("ログインに失敗しました")
            return redirect("/")
    else:
        messages = get_flashed_messages()
        return render_template("login.html", messages=messages)

@app.route("/userAdd", methods=['POST', 'GET'])
def userAdd():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            auth.create_user_with_email_and_password(email, password)
            flash("ユーザー登録が完了しました")
            return redirect("/question")
        except:
            flash("ユーザー登録に失敗しました")
            return redirect("/")
    else:
        return render_template("userAdd.html")

@app.route("/logout")
def logput():
    session.pop('user', None)
    flash("ログアウトしました")
    return redirect('/')



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
}

# レビューデータベースに入れるときのデータの型
review_format={
    "mangaTitle":None,
    "evaluation":None,
    "contents":None,
    "username":None,
}


# 新しく入力されたテストデータ
# answer =  [1.0, 5.0, 3.0, 0.0, 2.0, 3.0, 5.0, 3.0, 4.0, 0.0, 1.0, 1.0, 3.0, 5.0, 4.0, 5.0, 4.0, 5.0, 3.0, 0.0]






# アンケート回答送信
@app.route('/question', methods = ['GET','POST'])
def question():
    if request.method == 'GET':
        return render_template("question.html")
    else:
        mangaAnswer = []

        #HTMLフォームからデータを受け取る
        for i in range(1,21):
            question_key = f'question-{i:02}'
            answer = request.form.get(question_key)
            answer=float(answer)
            mangaAnswer.append(answer)

        # データベースにデータを格納
        user_format['gender']=1
        user_format['mangaAnswer']=mangaAnswer
        user_format['username']="K"

        user_document=user_doc_ref.document()
        user_document.set(user_format)


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
     

        

        return render_template("home.html",review_users=nearest_values_users,title_data=title_data)


# レビュー投稿
@app.route('/review')
def review():
    # 入力されたレビューのデータ
    review_format["evaluation"]=4
    review_format["mangaTitle"]="ワンピース"
    review_format["contents"]="ああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああ"
    review_format["username"]="kota"
    review_document=review_doc_ref.document() 
    review_document.set(review_format)
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)
