from flask import Flask, render_template, request, jsonify, redirect
import faiss
import numpy as np
import firebase_admin
from firebase_admin import credentials,firestore

# データベースの準備等
cred = credentials.Certificate("key.json")

firebase_admin.initialize_app(cred)
db = firestore.client()

user_doc_ref = db.collection('user')
all_user = user_doc_ref.get()

review_doc_ref=db.collection('review')


app = Flask(__name__)
# ユーザーデータベースにいれるときのデータの型
user_format={
    "gender":None,
    "mangaAnswer":[],
    "username":None,
}

# レビューデータベースに入れるときのデータの型
review_format={
    "contents":None,
    "username":None,
}


# 新しく入力されたテストデータ
# answer =  [1.0, 5.0, 3.0, 0.0, 2.0, 3.0, 5.0, 3.0, 4.0, 0.0, 1.0, 1.0, 3.0, 5.0, 4.0, 5.0, 4.0, 5.0, 3.0, 0.0]



@app.route('/')
def home():
    return render_template("question.html")

# アンケート回答送信
@app.route('/question', methods = ['POST'])
def question():
    
    if request.method == 'POST':
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
        _, indices = index.search(np.array([mangaAnswer], dtype=np.float32), k=4)
        # 結果の値だけを取り出す
        nearest_values_users = [all_users[i] for i in indices[0]]
        

        return render_template("home.html",review_users=nearest_values_users)


# # ユーザーデータベースの参照
# user_doc_ref = db.collection('user')

# # 特定のusernameを持つデータを検索
# target_username = "Syunsuke"  # ここに検索したいusernameを指定

# # クエリの作成
# query = user_doc_ref.where('username', '==', target_username)

# レビュー投稿
@app.route('/review')
def review():
    # 入力されたレビューのデータ
    review_format["contents"]="ああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああああ"
    review_format["username"]="kota"
    review_document=review_doc_ref.document() 
    review_document.set(review_format)
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)
