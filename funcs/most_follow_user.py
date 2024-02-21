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

        follower = user_doc_ref.where('follow', 'array_contains', user.id).stream()
        # 検索結果のドキュメントの数を数える
        follow_count = sum(1 for _ in follower)
        user_follow_counts.append({"user_id": user.id, "follow_count": follow_count})

    # フォロワー数でユーザーをソート
    sorted_users = sorted(user_follow_counts, key=lambda user: user["follow_count"], reverse=True)

    return sorted_users






