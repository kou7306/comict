from firebase_admin import firestore
from firebaseSetUp import db





review_doc_ref=db.collection('review')
comics_doc_ref=db.collection('comics')

# ブックマーク数が多い漫画を取得


def most_bookmark_comics(num):


    # 漫画ごとのタイトルとブックマーク数を格納するリスト
    comic_bookmarks = []

    # 漫画のデータを取得してリストに格納
    comics_query = comics_doc_ref.stream()
    for comic in comics_query:
        comic_data = comic.to_dict()
        comic_title = comic_data["title"]
        bookmark_num = len(comic_data.get("bookmark", []))
        comic_bookmarks.append({"title": comic_title, "bookmark_num": bookmark_num})

    # ブックマーク数で降順にソート
    sorted_comic_bookmarks = sorted(comic_bookmarks, key=lambda x: x["bookmark_num"], reverse=True)


    return sorted_comic_bookmarks[:num]
