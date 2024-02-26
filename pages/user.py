from flask import Blueprint, render_template, request, redirect, session, jsonify
from firebaseSetUp import auth, db
from funcs.most_follow_user import most_follow_user
from funcs.most_review_user import most_review_users
from funcs.search_user import search_user

user_bp = Blueprint('user', __name__)
user_doc_ref = db.collection('user')
suggestion_doc_ref=db.collection('suggestion')

# user_idからフォローしている人のuser_idをとってくる
def get_follow_user_id(user_id):
    user_doc = user_doc_ref.document(user_id).get()
    user_data = user_doc.to_dict()
    
    if user_data and "follow" in user_data:
        return user_data["follow"]
    else:
        return []

# user_idからマッチングしたユーザーのuser_idをとってくる
def get_matching_user_id(user_id):
    user_doc = user_doc_ref.document(user_id).get()
    user_data = user_doc.to_dict()
    
    if user_data and "user_query" in user_data:
        return user_data["user_query"]
    else:
        return []

# ユーザー取得用API
@user_bp.route('/api/user', methods = ['GET'])
def fetch_user():
    user_id = session.get('user_id')
    logged_in = True if user_id else False
        
    sort_option = request.args.get('sort_option', 'suggestions')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 8))
    
    print("sort_option:", sort_option)
    
    if (sort_option == "suggestions" or sort_option == "follows")and not logged_in:
        return jsonify({'message': 'ログインすると見ることができるようになります！'}), 401
    
    # ソートオプションに基づいたユーザーのidをとってくる
    requested_user_id = []
    if sort_option == "rising":
        user_data = most_review_users(7)
        requested_user_id = [user_id for user_id, _ in user_data]
    elif sort_option == "review-count":
        user_data = most_review_users()
        requested_user_id = [user_id for user_id, _ in user_data]
    elif sort_option == "follows":
        requested_user_id = get_follow_user_id(user_id)
    elif sort_option == "popularity":
        user_data = most_follow_user()
        requested_user_id = [user["user_id"] for user in user_data]
    elif sort_option == "suggestions":
        requested_user_id = get_matching_user_id(user_id)
        
    # print('user_id:', requested_user_id)

    
    # ページネーションのための処理
    start = (page - 1) * page_size
    end = start + page_size
    
    # user_idからユーザーの情報をとってくる
    user_info = []
    for user_id in requested_user_id[start:end]:
        user_data = search_user(user_id)
        user_info.append(user_data)
        
    # print("user:", user_info)
        
    return jsonify({'users': user_info})

@user_bp.route('/user')
def user():
    # セッションからユーザーIDを取得（未ログインの場合はNoneが返る）
    user_id = session.get('user_id')
    if not user_id is None and not user_doc_ref.document(user_id).get().exists:
        return redirect('/login') 

    logged_in = True if user_id else False
    return render_template('user.html', logged_in=logged_in)