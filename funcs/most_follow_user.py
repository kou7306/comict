from firebase_admin import firestore
from firebaseSetUp import db

user_doc_ref = db.collection('user')

def most_follow_user():
    # ユーザーデータを取得
    users = user_doc_ref.stream()

    # ユーザーごとのフォロワー数を格納するリスト
    user_follow_counts = []

    # フォロワー数を取得してリストに格納
    for user in users:
        user_data = user.to_dict() 
        follow_count = len(user_data.get("follow", []))
        user_follow_counts.append({"user_id": user.id, "follow_count": follow_count})

    # フォロワー数でユーザーをソート
    sorted_users = sorted(user_follow_counts, key=lambda user: user["follow_count"], reverse=True)

    return sorted_users






