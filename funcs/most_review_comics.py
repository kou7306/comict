from firebase_admin import firestore
from firebaseSetUp import db
from datetime import datetime, timedelta
from pytz import timezone

# 日本時間のタイムゾーンを取得
jst = timezone('Asia/Tokyo')



review_doc_ref=db.collection('review')
comics_doc_ref=db.collection('comics')

# レビュー数が多い漫画を取得


def most_review_comics(num, date):
    # 漫画ごとのレビュー数を格納する辞書を作成
    comic_review_count = {}

    # 期間の開始日時を計算
    if date != None:
        start_date = datetime.now(jst) - timedelta(days=date)
    else:
        start_date = None

    # レビューの取得
    if start_date:
        reviews_query = review_doc_ref.where('created_at', '>=', start_date).stream()
    else:
        reviews_query = review_doc_ref.stream()

    # 各レビューの漫画IDを取得してカウント
    for review in reviews_query:      
        # 指定された期間内のレビューのみをカウント
    
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
