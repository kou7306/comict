from firebase_admin import firestore
from firebaseSetUp import db

user_doc_ref = db.collection('user')

def most_follow_user():
    # ユーザーのリストを取得
    users = user_doc_ref.stream()

    # フォロワー数が多い順にユーザーをソート
    sorted_users = sorted(users, key=lambda user: len(user.get("follow", [])), reverse=True)

    return sorted_users



