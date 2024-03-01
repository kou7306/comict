from flask import Blueprint, render_template, request, redirect, session, flash, url_for, get_flashed_messages,jsonify
from firebaseSetUp import auth, db
from bs4 import BeautifulSoup
import requests
from funcs.review_sort_user import review_sort_for_user

userpage_bp = Blueprint('userpage', __name__)

user_doc_ref = db.collection('user')
review_doc_ref=db.collection('review')
comic_doc_ref = db.collection('comics')  

def get_bar_color(ans):
    if ans < 0:
        return 'bg-red-500'
    elif ans == 0:
        return 'bg-yellow-300'
    else:
        return 'bg-green-500'


def get_bar_width(ans):
    bar_width = ((ans + 5) / 10) * 100
    if bar_width < 5:
        return 5
    elif bar_width > 100:
        return 100
    else:
        return bar_width

# マイページ
@userpage_bp.route('/userpage', methods=['GET', 'POST'])
def user_page():   
    user_id = session.get('user_id')
    if not user_doc_ref.document(user_id).get().exists:
        return redirect("/login?query=userpage")
    if not user_id:
        return redirect('/login?query=userpage')
    user_id = session.get('user_id')
    if user_id:
        logged_in = True
    else:
        logged_in = False   
    user_doc = user_doc_ref.document(user_id)
    user=user_doc.get()
    user_data=user.to_dict()
    username=user_data["username"]
    # 特定のユーザーネームに一致するドキュメントを取得
    query = review_doc_ref.where('user_id', '==', user_id).stream()
    review_num = sum(1 for _ in query)
    reviews = review_sort_for_user(user_id,logged_in,None)

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
    combined_list = list(zip(question, answer))

    #選択したジャンルを取得
    genre_list = ["バトル", "スポーツ", "恋愛", "ミステリー", "コメディ", "SF", "歴史"]
    genre_choice = genre_list[int(genre_value)-1]
    
    updated_combined_list = []
    for q, ans in combined_list:
        color = get_bar_color(ans)
        width = get_bar_width(ans)
        updated_combined_list.append((q, ans, color, width))
    
    #ブックマークをデータベースから取得
    favorite_comic =[]
    favorite_titles = user_data["bookmark"]
    for title in favorite_titles[:4]:
        title_doc = comic_doc_ref.document(title).get()
        if title_doc.exists:
            title_data = title_doc.to_dict()
            favorite_comic.append(title_data)

    # フォローしたユーザーのIDを取得
    follow_data = []
    for follow_id in user_data["follow"]:
        follow_doc = user_doc_ref.document(follow_id).get()
        if follow_doc.exists:
            follow_name = follow_doc.to_dict()["username"]
            follow_data.append((follow_name, follow_id))

    follower = user_doc_ref.where('follow', 'array_contains', user_id).stream()
    # 検索結果のドキュメントの数を数える
    follower_num = sum(1 for _ in follower)

    return render_template("userpage.html", reviews=reviews,username=username, user_id=user_id,favorite_comic=favorite_comic,follow_data=follow_data,result=result, combined_list=updated_combined_list, genre_choice=genre_choice, logged_in=logged_in,follower_num=follower_num,user_doc_ref=user_doc_ref,review_doc_ref=review_doc_ref,comic_doc_ref=comic_doc_ref,review_num=review_num)
 

@userpage_bp.route('/edit/<user_id>', methods=['POST']) 
def edit_name(user_id): 
    data = request.json

    new_username = data.get("username")
    # print(new_username)
    # print(user_id)
    user_doc_ref.document(user_id).update({"username": new_username})
    return jsonify({"status": "success"})


