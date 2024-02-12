from flask import Blueprint, render_template, request, redirect, session, flash, url_for, get_flashed_messages,jsonify
from firebaseSetUp import auth, db
from funcs.matching import matching
from funcs.most_review_comics import most_review_comics

update_matching_bp = Blueprint('update_matching', __name__)
user_doc_ref = db.collection('user')
review_doc_ref=db.collection('review')
comics_doc_ref=db.collection('comics')
suggestion_doc_ref=db.collection('suggestion')


# 定期実行でリクエストされるエンドポイント
@update_matching_bp.route('/update_matching', methods=["POST"])
def update_matching():   
    all_user = user_doc_ref.stream()
    # 全ユーザーのマッチング結果を更新
    for user in all_user:
        user_id = user.id
        user_doc = user_doc_ref.document(user_id)
        # マッチング
        review_query, user_query =matching(user.to_dict()["mangaAnswer"],user_id)
        
        update_data = {"user_query":  user_query,"review_query":review_query}
        user_doc.update(update_data)

    
    # レビュー投稿数の多い漫画更新
        # レビュー数が多い漫画の表示
        # 一週間以内
        oneweek_top_comics = most_review_comics(10, 7)  # 上位 10 件の漫画を取得し、期間は過去 30 日間とします
   
        # 上位の漫画名のみを取り出す
        top_comics_names = [comic[0] for comic in oneweek_top_comics]
        suggestion_doc_ref.document("oneweek").update({"most_review_comics": top_comics_names})

        # 全期間
        all_top_comics = most_review_comics(10, None)
        top_comics_names = [comic[0] for comic in all_top_comics]
        suggestion_doc_ref.document("all").update({"most_review_comics": top_comics_names})      

    # ブックマークが多い漫画の更新  



    return jsonify({"message": "マッチングが更新されました。"})
