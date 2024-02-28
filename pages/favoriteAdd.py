from flask import Blueprint, render_template, request, redirect, session, flash, url_for, get_flashed_messages,jsonify
from firebaseSetUp import auth, db
from firebase_admin import credentials, firestore
from funcs.wiki import get_manga_title,get_wikipedia_page_details,get_manga_genre
from funcs.get_book import get_google_book_cover
from funcs.search import search_comics

favoriteAdd_bp = Blueprint('favoriteAdd', __name__)
user_doc_ref = db.collection('user')
comics_doc_ref=db.collection('comics')

# 好きな作品を返すAPI
@favoriteAdd_bp.route('/api/favoriteAdd', methods=['GET'])
def fetch_favorite_manga():
    session_user_id = session.get('user_id')
    requested_user_id = request.args.get('user_id')
    
    if session_user_id == requested_user_id:
        is_own = True
    else:
        is_own = False
    
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 8))
    
    user_doc = user_doc_ref.document(requested_user_id)
    user=user_doc.get()
    favorite_titles = user.to_dict().get("bookmark", [])
    
    # ページネーションのための処理
    start = (page - 1) * page_size
    end = start + page_size
    
    # 本の名前から本の情報をとってくる
    comics_info = []
    for title in favorite_titles[start:end]:
        comics_data = search_comics(title)
        comics_info.extend(comics_data)
        
    return jsonify({'comics': comics_info, 'is_own': is_own})
 
# 好きな作品を追加
@favoriteAdd_bp.route('/favoriteAdd', methods=['GET', 'POST'])
def add_manga():
    session_user_id = session.get('user_id')
    # 上の'user_id'とは別リソース
    view_user_id = request.args.get('user_id', default=session_user_id)
    
    if not session_user_id:
        # ユーザーがログインしていない場合はログインページへリダイレクト
        return redirect("/login?query=favoriteAdd")
    
    logged_in = True   
    user_doc = user_doc_ref.document(view_user_id)
    user=user_doc.get()
    
    if not user.exists:
        # ユーザードキュメントが存在しない場合の処理（エラーメッセージの表示など）
        return "User not found", 404
    
    favorite_titles = user.to_dict().get("bookmark", [])
   
    
    if request.method == 'GET':
        if not session_user_id is None and not user.exists:
            return redirect("/login?query=favoriteAdd")
        if session_user_id == view_user_id:
            # 自分のお気に入り作品を表示
            return render_template('favoriteAdd.html', user_id=session_user_id, logged_in=logged_in, is_own=True)
        else:
            # 他ユーザーのお気に入り作品を表示
            return render_template('favoriteAdd.html', user_id=view_user_id, logged_in=logged_in, is_own=False)

    elif request.method == 'POST':
        data = request.get_json()
        manga_title = data.get('title')
        requested_user_id = data.get('requested_user_id')
        
        # 更新しようとしているuser_idとログインしているuser_idが異なったら処理を終了する
        if session_user_id != requested_user_id:
            return jsonify({'error:' '権限がありません'}), 403
        else:
            user_doc = user_doc_ref.document(session_user_id)
        
        print(manga_title)
        # ユーザードキュメントの更新
        user_doc.update({
            'bookmark': firestore.ArrayUnion([manga_title])
        })



        #　漫画テーブルの更新
        # `comics`コレクションから`title`が`manga_title`と等しいドキュメントを検索
        query = comics_doc_ref.where('title', '==', manga_title).stream()




        # 検索結果がない場合の処理を追加
        if not any(query):
            url=get_wikipedia_page_details(manga_title)
            genre = get_manga_genre(manga_title)
            print("start_get_google_book_cover")
            image_url=get_google_book_cover(manga_title)
            

            comics_doc_ref.document(manga_title).set({"title": manga_title,"genre":genre,"bookmark":[session_user_id],"url":url,"reviews":[],"author":None,"image":image_url})
        else:
            # comicsドキュメントのbookmarkを更新
            comics_doc_ref.document(manga_title).update({
            'bookmark': firestore.ArrayUnion([session_user_id])
        })
        # ユーザーデータの取得
        favorite_titles.append(manga_title)
        return jsonify({'favoriteTitles': favorite_titles})
