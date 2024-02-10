from flask import Blueprint, render_template, request, redirect, session, flash, url_for, get_flashed_messages
from firebaseSetUp import auth, db
from bs4 import BeautifulSoup
import requests

userpage_bp = Blueprint('userpage', __name__)

user_doc_ref = db.collection('user')
review_doc_ref=db.collection('review')

# ユーザーページ
@userpage_bp .route('/<user_id>/userpage', methods=['GET', 'POST'])
def user_page(user_id):   

    user_doc = user_doc_ref.document(user_id)
    user=user_doc.get()
    user_data=user.to_dict()
    username=user_data["username"]
    # 特定のユーザーネームに一致するドキュメントを取得
    query = review_doc_ref.where('username', '==', username).get()

    # アンケート結果の取得・表示
    genre_value=user_data.get("genre")
    start_question = 20 * (int(genre_value) - 1)
    end_question = start_question + 20

    html_file_path=f"templates/question{genre_value}.html"
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_code = file.read()
    result = user_data.get('mangaAnswer')

    #アンケートの設問を格納する配列
    question = []
    soup = BeautifulSoup(html_code, 'html.parser')

    #アンケートの設問を取得
    h2_elems = soup.find_all('h2')
    for h2 in h2_elems:
        question.append(h2.text)
    
    #アンケートの回答を取得
    answer = result[start_question:end_question]

    #設問と回答をタプル化
    combined_list = zip(question, answer)

    #選択したジャンルを取得
    genre_list = ["バトル", "スポーツ", "恋愛", "ミステリー", "コメディ", "SF", "歴史"]
    genre_choice = genre_list[int(genre_value)-1]

    #ブックマークをデータベースから取得
    favorite_titles = user_data["favorite_manga"]

    # フォローしたユーザーのIDを取得
    follow_data = []
    for follow_id in user_data["follow"]:
        follow_doc = user_doc_ref.document(follow_id).get()
        if follow_doc.exists:
            follow_name = follow_doc.to_dict()["username"]
            follow_data.append((follow_name, follow_id))
 
 

 


    return render_template("userpage.html", myreview_query=query,username=username, user_id=user_id,favorite_titles=favorite_titles,follow_data=follow_data,result=result, combined_list=combined_list, genre_choice=genre_choice)


