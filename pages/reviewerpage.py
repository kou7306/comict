from flask import Blueprint, render_template, request, redirect, session, flash, url_for, get_flashed_messages,jsonify
from firebaseSetUp import auth, db
from bs4 import BeautifulSoup
import requests
import json

reviewerpage_bp = Blueprint('reviewerpage', __name__)

user_doc_ref = db.collection('user')
review_doc_ref=db.collection('review')

is_following=False

# reviewer page
@reviewerpage_bp.route('/<reviewer_id>/userpage', methods = ['GET','POST'])
def reviewer(reviewer_id):
    user_id = session.get('user_id')

    if request.method == 'GET':
        if not user_id is None and not user_doc_ref.document(user_id).get().exists:
            return redirect("/login")
        if user_id:
            logged_in = True
        else:
            logged_in = False    
        # レビュワーの情報をとってくる
        reviewer_doc = user_doc_ref.document(reviewer_id).get()
        reviewername=reviewer_doc.to_dict()["username"]
        review_data=reviewer_doc.to_dict()
        # 特定のユーザーネームに一致するレビュー情報を取得
        query = review_doc_ref.where('username', '==', reviewername).get()
        if user_id:
            # そのユーザーをフォローしてるか
            user_doc = user_doc_ref.document(user_id)
            # 'follow' フィールド中に 'reviewername' が含まれているか確認
            is_following = any(user == reviewername for user in user_doc.get().to_dict()['follow'])
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


        favorite_titles = reviewer_doc.to_dict().get('favorite_manga', [])  # favorite_titlesが存在しない場合は空のリストを使う
        return render_template("reviewerpage.html",query=query,username=reviewername,reviewer_id=reviewer_id,user_id=user_id,is_following=is_following,favorite_titles=favorite_titles,rev_combined_list=rev_combined_list,rev_genre_choice=rev_genre_choice,logged_in=logged_in)
    else:
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
        
