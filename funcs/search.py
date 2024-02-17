from firebaseSetUp import auth, db


# 漫画を検索する関数
def search_comics(title):
    if title == "":
     return []
    results = []
    # Firebaseから一致する漫画を検索
    comics_ref = db.collection('comics')
    query_result = comics_ref.where('title', '==', title).get()
    for doc in query_result:
        results.append(doc.to_dict())
    return results