from firebase_admin import firestore
from firebaseSetUp import db
from datetime import datetime, timedelta

review_doc_ref=db.collection('review')
comics_doc_ref=db.collection('comics')

# レビュー数が多い漫画を取得


def most_review_comics(num, date):
    # 漫画ごとのレビュー数を格納する辞書を作成
    comic_review_count = {}

    # 期間の開始日時を計算
    if date!=None:
        start_date = datetime.now() - timedelta(days=date)
    else:
        start_date = None

    # 全てのレビューを取得
    all_reviews = review_doc_ref.stream()

    # 各レビューの漫画IDを取得してカウント
    for review in all_reviews:
        # レビューの投稿日時を取得
        review_date = review.to_dict()["created_at"].to_datetime() 

        # 指定された期間内のレビューのみをカウント
        if not start_date or review_date >= start_date:
            comicTitle = review.to_dict()["mangaTitle"]
            if comicTitle in comic_review_count:
                comic_review_count[comicTitle] += 1
            else:
                comic_review_count[comicTitle] = 1

    # レビュー数で辞書をソート
    sorted_comic_review_count = sorted(comic_review_count.items(), key=lambda x: x[1], reverse=True)

    # 上位の漫画IDとレビュー数を取得
    top_comics = sorted_comic_review_count[:num]

    print(top_comics)

    return top_comics
