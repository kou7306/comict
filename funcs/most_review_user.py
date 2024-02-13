from firebase_admin import firestore
from firebaseSetUp import db
from datetime import datetime, timedelta

user_doc_ref = db.collection('user')
review_doc_ref = db.collection('review')

def most_review_users(date):
    # 指定された日数前の日時を計算
    if date is not None:
        start_date = datetime.now() - timedelta(days=date)
    else:
        start_date = None

    # ユーザーごとのレビュー投稿数を格納する辞書を作成
    user_review_count = {}

    # レビューの取得
    if start_date:
        reviews_query = review_doc_ref.where('created_at', '>=', start_date).stream()
    else:
        reviews_query = review_doc_ref.stream()

    # レビューごとに投稿者のユーザーIDをカウント
    for review in reviews_query:
        user_id = review.to_dict()["user_id"]
        if user_id in user_review_count:
            user_review_count[user_id] += 1
        else:
            user_review_count[user_id] = 1

    # ユーザーをレビュー投稿数でソート
    sorted_users = sorted(user_review_count.items(), key=lambda x: x[1], reverse=True)

    return sorted_users
