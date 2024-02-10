from flask import render_template, request, redirect, session, flash, url_for, get_flashed_messages
from firebaseSetUp import auth, db
import faiss
import numpy as np

user_doc_ref = db.collection('user')
review_doc_ref=db.collection('review')


# マッチング関数
def matching(mangaAnswer,user_id):
    # データベースにあるすべてのユーザーデータを取得
    all_user_vector = []
    all_users = []
    all_user = user_doc_ref.stream()
    
    if(all_user == []):
        print("データがありません")
    for user in all_user:
        print(user.to_dict()["mangaAnswer"])
        if(user.id!=user_id): # 自分以外
            
            print('データ',user.to_dict()["mangaAnswer"])
            all_user_vector.append(user.to_dict()["mangaAnswer"])
            all_users.append(user.to_dict())
    
    if(all_user_vector != []):
        # Faissインデックスの作成
        dimension = len(all_user_vector[0])  # ベクトルの次元数
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(all_user_vector, dtype=np.float32))
        
        # 最近傍のベクトルを検索
        _, indices = index.search(np.array([mangaAnswer], dtype=np.float32), k=1)
        
        # 結果の値だけを取り出す
        nearest_values_users = [all_users[i] for i in indices[0]]
        
        # 対象ユーザーのレビューした情報のIDを取り出す
        review_query_results = []
        user_query_results = []
        
        for user in nearest_values_users:
            # usernameが一致するレビューデータをすべて取り出す
            review_query_result = review_doc_ref.where('username', '==', user["username"]).stream()
            user_query_result = user_doc_ref.where('username', '==', user["username"]).stream()
            for doc in review_query_result:
                review_query_results.append(doc.id)
            for doc in user_query_result:
                user_query_results.append(doc.id)

        
        return review_query_results, user_query_results
    return None,None