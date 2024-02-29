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
    
    
    #if ans <= -4:
        #return 'bg-red-500'  # 1
    #elif ans <= -3:
        #return 'bg-red-400'  # 2
    #elif ans <= -2:
        #return 'bg-red-300'  # 3
    #elif ans <= -1:
        #return 'bg-orange-400'  # 4
    #elif ans < 0:
        #return 'bg-yellow-600'  # 5
    #elif ans == 0:
        #return 'bg-yellow-500'  # 6
    #elif ans <= 1:
        #return 'bg-lime-400'  # 7
    #elif ans <= 2:
        #return 'bg-green-400'  # 8
    #elif ans <= 3:
        #return 'bg-green-500'  # 9
    #else:
        #return 'bg-green-600'  # 10

def get_bar_width(ans):
    return ((ans + 5) / 10) * 100

# reviewer page
@reviewerpage_bp.route('/<reviewer_id>/userpage', methods = ['GET','POST'])
def reviewer(reviewer_id):
    user_id = session.get('user_id')

    if request.method == 'GET':
        if user_id is not None and user_id == reviewer_id:
            return redirect(url_for('userpage.user_page'))
        if user_id:
            logged_in = True
        else:
            logged_in = False    
        # レビュワーの情報をとってくる
        reviewer_doc = user_doc_ref.document(reviewer_id).get()
        reviewername=reviewer_doc.to_dict()["username"]
        review_data=reviewer_doc.to_dict()
        # 特定のユーザーネームに一致するレビュー情報を取得
        #query = review_doc_ref.where('user_id', '==', reviewer_id).get()
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

        return render_template("reviewerpage.html",reviews=reviews,username=reviewername,reviewer_id=reviewer_id,user_id=user_id,is_following=is_following,favorite_comic=favorite_comic,rev_combined_list=rev_combined_list,rev_genre_choice=rev_genre_choice,logged_in=logged_in,follower_num=follower_num,combined_list=updated_combined_list,user_doc_ref=user_doc_ref,review_doc_ref=review_doc_ref,comic_doc_ref=comic_doc_ref)
    
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
        
