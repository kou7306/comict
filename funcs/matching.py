from flask import render_template, request, redirect, session, flash, url_for, get_flashed_messages
from firebaseSetUp import auth, db
import faiss
import numpy as np

user_doc_ref = db.collection('user')
review_doc_ref=db.collection('review')
comic_doc_ref=db.collection('comics')



# マッチング関数
def matching(mangaAnswer,user_id,genre):
    # データベースにあるすべてのユーザーデータを取得
    all_user_vector = []
    all_users = []
    all_user = user_doc_ref.stream()
    
    if(all_user == []):
        print("データがありません")
    for user in all_user:

        if(user.id!=user_id): # 自分以外
            # ジャンルが一致するユーザーのみを取り出す
            if (int(user.to_dict()["genre"]) == genre):                  

                    all_user_vector.append(user.to_dict()["mangaAnswer"])
                    all_users.append(user.id)


   
    if(all_user_vector != []):
        # Faissインデックスの作成
        dimension = len(all_user_vector[0])  # ベクトルの次元数
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(all_user_vector, dtype=np.float32))
        
        # 最近傍のベクトルを検索
        _, indices = index.search(np.array([mangaAnswer], dtype=np.float32), k=10)
        
        # 結果の値だけを取り出す
        nearest_values_users = [all_users[i] for i in indices[0]]
        
        # 対象ユーザーのレビューした情報のIDを取り出す
        comic_query_results = []
        user_query_results = []


        
        
        for user_id in nearest_values_users:
            
            user_query_results.append(user_id)
            # usernameが一致するレビューデータをすべて取り出す
            review_query = review_doc_ref.where('user_id', '==', user_id).stream()

            for doc in review_query:
                eval=doc.to_dict()["evaluation"]
                if(int(eval)>=4):
                    # レビューした漫画を取り出す
                    comic = next(comic_doc_ref.where('title', '==', doc.to_dict()['mangaTitle']).limit(1).stream(), None)


                    if genre == 1:
                        if "バトル" in comic.to_dict()['genre'] or "アクション" in comic.to_dict()['genre'] or "格闘" in comic.to_dict()['genre']:
                            if comic.id not in comic_query_results:
                                comic_query_results.append(comic.id)
                    
                    elif genre == 2:
                        if "スポーツ" in comic.to_dict()['genre']:
                            if comic.id not in comic_query_results:
                                comic_query_results.append(comic.id)

                    elif genre == 3:
                        if "恋愛" in comic.to_dict()['genre'] or "ラブコメ" in comic.to_dict()['genre']:
                            if comic.id not in comic_query_results:
                                comic_query_results.append(comic.id)
                    
                    elif genre == 4:
                        if "ミステリー" in comic.to_dict()['genre'] or "サスペンス" in comic.to_dict()['genre'] or "ホラー" in comic.to_dict()['genre'] or "探偵" in comic.to_dict()['genre']:
                            if comic.id not in comic_query_results:
                                comic_query_results.append(comic.id)

                    elif genre == 5:
                        if "コメディー" in comic.to_dict()['genre'] or "ギャグ" in comic.to_dict()['genre']:
                            if comic.id not in comic_query_results:
                                comic_query_results.append(comic.id)
                    
                    elif genre == 6:
                        if "ファンタジー" in comic.to_dict()['genre'] or "SF" in comic.to_dict()['genre'] or "ロボット" in comic.to_dict()['genre']:
                            if comic.id not in comic_query_results:
                                comic_query_results.append(comic.id)

                    elif genre == 7:
                        if "歴史" in comic.to_dict()['genre'] or "時代" in comic.to_dict()['genre']:
                            if comic.id not in comic_query_results:
                                comic_query_results.append(comic.id)


            # お気に入り漫画の情報を取り出す
                favorite_query = user_doc_ref.document(user_id).get().to_dict()["bookmark"]
                for comic in favorite_query:
                    if genre == 1:
                        if "バトル" in comic.to_dict()['genre'] or "アクション" in comic.to_dict()['genre'] or "格闘" in comic.to_dict()['genre']:
                            if comic.id not in comic_query_results:
                                comic_query_results.append(comic.id)
                        
                    elif genre == 2:
                        if "スポーツ" in comic.to_dict()['genre']:
                            if comic.id not in comic_query_results:
                                comic_query_results.append(comic.id)

                    elif genre == 3:
                        if "恋愛" in comic.to_dict()['genre'] or "ラブコメ" in comic.to_dict()['genre']:
                            if comic.id not in comic_query_results:
                                comic_query_results.append(comic.id)
                    
                    elif genre == 4:
                        if "ミステリー" in comic.to_dict()['genre'] or "サスペンス" in comic.to_dict()['genre'] or "ホラー" in comic.to_dict()['genre'] or "探偵" in comic.to_dict()['genre']:
                            if comic.id not in comic_query_results:
                                comic_query_results.append(comic.id)

                    elif genre == 5:
                        if "コメディー" in comic.to_dict()['genre'] or "ギャグ" in comic.to_dict()['genre']:
                            if comic.id not in comic_query_results:
                                comic_query_results.append(comic.id)
                    
                    elif genre == 6:
                        if "ファンタジー" in comic.to_dict()['genre'] or "SF" in comic.to_dict()['genre'] or "ロボット" in comic.to_dict()['genre']:
                            if comic.id not in comic_query_results:
                                comic_query_results.append(comic.id)

                    elif genre == 7:
                        if "歴史" in comic.to_dict()['genre'] or "時代" in comic.to_dict()['genre']:
                            if comic.id not in comic_query_results:
                                comic_query_results.append(comic.id)

                for doc in review_query:
                    eval=doc.to_dict()["evaluation"]
                    if(int(eval)>=4):
                        # レビューした漫画を取り出す
                        comic = next(comic_doc_ref.where('title', '==', doc.to_dict()['mangaTitle']).limit(1).stream(), None)
                        if comic.id not in comic_query_results:
                            comic_query_results.append(comic.id)

                
                for comic in favorite_query:
                    if comic.id not in comic_query_results:
                        comic_query_results.append(comic.id)              


        
        return comic_query_results, user_query_results
    return [],[]