from firebaseSetUp import auth, db


# 漫画を検索する関数
def search_comics(query):
    if query=="":
        return []
    results = []
    # comicsから漫画を検索
    comics_ref = db.collection('comics')
    query_result = comics_ref.where('title', '>=', query).where('title', '<=', query + '\uf8ff').get()
    for doc in query_result:
        results.append(doc.to_dict())
    return results