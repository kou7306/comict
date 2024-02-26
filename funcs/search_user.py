from firebaseSetUp import db


# ユーザーを取得する関数
def search_user(user_id):
    user_doc_ref = db.collection('user')
    user_doc = user_doc_ref.document(user_id).get()
    
    if user_doc.exists:
        user_data = user_doc.to_dict()
        user_data['user_id'] = user_id
        return user_data
    else:
        return None