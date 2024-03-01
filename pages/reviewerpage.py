from flask import Blueprint, render_template, request, redirect, session, flash, url_for, get_flashed_messages,jsonify
from firebaseSetUp import auth, db
from bs4 import BeautifulSoup
import requests
import json
from funcs.review_sort_user import review_sort_for_user

reviewerpage_bp = Blueprint('reviewerpage', __name__)

user_doc_ref = db.collection('user')
review_doc_ref=db.collection('review')
comic_doc_ref = db.collection('comics') 

is_following=False
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

# reviewer page
@reviewerpage_bp.route('/<reviewer_id>/userpage', methods = ['GET','POST'])
def reviewer(reviewer_id):
    user_id = session.get('user_id')
    if user_id:
        logged_in = True
    else:
        logged_in = False   
    if request.method == 'GET':
        if user_id is not None and user_id == reviewer_id:
            return redirect(url_for('userpage.user_page'))
 
        # レビュワーの情報をとってくる
        reviewer_doc = user_doc_ref.document(reviewer_id).get()
        reviewername=reviewer_doc.to_dict()["username"]
        review_data=reviewer_doc.to_dict()
        # 特定のユーザーネームに一致するレビュー情報を取得
        query = review_doc_ref.where('user_id', '==', reviewer_id).stream()
        review_num = sum(1 for _ in query)
        reviews = review_sort_for_user(reviewer_id,logged_in,None)

        if user_id:
            # そのユーザーをフォローしてるか
            user_doc = user_doc_ref.document(user_id)
            # 'follow' フィールド中に 'reviewername' が含まれているか確認
            is_following = any(user == reviewer_id for user in user_doc.get().to_dict()['follow'])
        else:
            is_following = False

        #アンケート結果の取得・表示
        rev_genre_value=review_data.get("genre")
        rev_start_question = 20 * (int(rev_genre_value) - 1)
        rev_end_question = rev_start_question + 20

        rev_html_file_path=f"templates/question{rev_genre_value}.html"
        with open(rev_html_file_path, 'r', encoding='utf-8') as file:
            rev_html_code = file.read()
        result = review_data.get('mangaAnswer')

        #アンケートの設問を格納する配列
        rev_question = []
        soup = BeautifulSoup(rev_html_code, 'html.parser')

        #アンケートの設問を取得
        rev_h2_elems = soup.find_all('h2')
        for h2 in rev_h2_elems:
            rev_question.append(h2.text)
    
        #アンケートの回答を取得
        rev_answer = result[rev_start_question:rev_end_question]

        #設問と回答をタプル化
        rev_combined_list = zip(rev_question, rev_answer)

        #選択したジャンルを取得
        genre_list = ["バトル", "スポーツ", "恋愛", "ミステリー", "コメディ", "SF", "歴史"]
        rev_genre_choice = genre_list[int(rev_genre_value)-1]
        updated_combined_list = []
        for q, ans in rev_combined_list:
            color = get_bar_color(ans)
            width = get_bar_width(ans)
            updated_combined_list.append((q, ans, color, width))

        #ブックマークをデータベースから取得
        favorite_comic =[]
        favorite_titles = reviewer_doc.to_dict()["bookmark"]
        for title in favorite_titles[:4]:
            title_doc = comic_doc_ref.document(title).get()
            if title_doc.exists:
                title_data = title_doc.to_dict()
                favorite_comic.append(title_data)

        

        follower = user_doc_ref.where('follow', 'array_contains', reviewer_id).stream()
        # 検索結果のドキュメントの数を数える
        follower_num = sum(1 for _ in follower)
       

        return render_template("reviewerpage.html",reviews=reviews,username=reviewername,reviewer_id=reviewer_id,user_id=user_id,is_following=is_following,favorite_comic=favorite_comic,rev_combined_list=rev_combined_list,rev_genre_choice=rev_genre_choice,logged_in=logged_in,follower_num=follower_num,combined_list=updated_combined_list,user_doc_ref=user_doc_ref,review_doc_ref=review_doc_ref,comic_doc_ref=comic_doc_ref,review_num=review_num)
    
    else:
        if not logged_in:
            return redirect(url_for('auth.login'))
        data = request.get_json()
        is_following = data.get('is_following')
        if not user_id:
            return jsonify({'isFollowing': -1})
        else:
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
        
