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


# 新しく入力されたデータ
answer =  [1.0, 5.0, 3.0, 0.0, 2.0, 3.0, 5.0, 3.0, 4.0, 0.0, 1.0, 1.0, 3.0, 5.0, 4.0, 5.0, 4.0, 5.0, 3.0, 0.0]

# データベースにあるすべてのユーザーデータを取得
all_user_vector=[]
for user in all_user:
    all_user_vector.append(user.to_dict()["mangaAnswer"])

# Faissインデックスの作成
dimension = len(all_user_vector[0])  # ベクトルの次元数
index = faiss.IndexFlatL2(dimension)
index.add(np.array(all_user_vector, dtype=np.float32))

@app.route('/')
def home():
    return redirect("/review")


# マッチング処理
@app.route('/match')
def find_nearest():

    # マッチング
    # 最近傍のベクトルを検索
    _, indices = index.search(np.array([answer], dtype=np.float32), k=2)
    # 結果の値だけを取り出す
    nearest_values = [all_user_vector[i] for i in indices[0]]


    # データベースにデータを格納する処理
    user_format['gender']=1
    user_format['mangaAnswer']=answer
    user_format['username']="Kota"

    user_document=user_doc_ref.document() 
    user_document.set(user_format)

    # -----------------

    # マッチング結果の出力
    print(nearest_values)

    return render_template("home.html")

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
