from firebase_admin import firestore
from firebaseSetUp import db

# データベース参照の取得
review_doc_ref = db.collection('review')

def high_evaluate_comics():
# 漫画ごとの評価の平均を格納するリスト
    comic_avg_ratings = []

    # レビューデータを取得して処理
    reviews_query = review_doc_ref.stream()
    for review in reviews_query:
        review_data = review.to_dict()
        comic_title = review_data["mangaTitle"]
        rating = review_data["evaluation"]

        # 漫画ごとにレビューの評価を格納するリストを作成
        if not any(comic["title"] == comic_title for comic in comic_avg_ratings):
            comic_avg_ratings.append({"title": comic_title, "ratings": [rating]})
        else:
            for comic in comic_avg_ratings:
                if comic["title"] == comic_title:
                    comic["ratings"].append(rating)

    # 漫画ごとの評価の平均を計算
    for comic in comic_avg_ratings:
        avg_rating = sum(comic["ratings"]) / len(comic["ratings"])
        comic["avg_rating"] = avg_rating
        del comic["ratings"]

    return comic_avg_ratings
