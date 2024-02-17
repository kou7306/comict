from flask import Blueprint, render_template, request, redirect, session, flash, url_for, get_flashed_messages
from firebaseSetUp import auth, db

auth_bp = Blueprint('auth', __name__)

user_doc_ref = db.collection('user')

# ユーザーデータベースにいれるときのデータの型
user_format={
    "mangaAnswer":[],
    "bookmark":[],
    "username":None,
    "follow":[],
    "user_query":[],
    "review_query":[],
    "genre":None,   
}

# login
@auth_bp.route("/login", methods=['POST', 'GET'])
def login():
    query = request.args.get('query')
    print(query)
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        
        
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
            # ユーザーの UID を取得
            user_id = user['localId']
            # userのidをセッションに保存
            session['user_id'] = user_id
            if user_doc_ref.document(user_id).get().exists: 
                if query == 'None':                      
                    return redirect('/')
                else:
                    return redirect(f'/{query}')
            else:
                flash("ユーザーが存在しません")
                return redirect(f"/login?query={query}")

        except:
                flash("ログインに失敗しました")
                return redirect(f"/login?query={query}")  
    else:
        messages = get_flashed_messages()
        return render_template("login.html", messages=messages,query=query)

# ユーザーネームの重複を確認する関数
def is_username_duplicate(username):
    # usersコレクションからユーザーネームが一致するドキュメントをクエリ
    query = user_doc_ref.where('username', '==', username)
    
    # クエリを実行して結果を取得
    query_result = query.stream()

    # クエリ結果が空でない場合は重複していると判断
    return any(query_result)

# ユーザー登録
@auth_bp.route("/userAdd", methods=['POST', 'GET'])
def userAdd():
    query = request.args.get('query')
    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')
        # usernameが重複していない場合

        try:
            user = auth.create_user_with_email_and_password(email, password)
            user_id = user['localId']  
            # userのidをセッションに保存
            session['user_id'] = user_id 
            # userデータベースに保存
            user_doc=user_doc_ref.document(user_id)
            user_format["username"]=user_id[:6]
            # デフォルトで外れ値を指定しておく
            user_format["mangaAnswer"]= [99.0 for x in range(140)]

            user_doc.set(user_format)
            session['flag'] = -2

            return redirect(f"/genre")
        except:
            flash("ユーザー登録に失敗しました")
            return redirect("/userAdd")
            
    
    else:
        
        return render_template("userAdd.html")

# logout
@auth_bp.route("/logout")
def logput():
    session.pop('user', None)
    session.pop('user_id', None)
    return redirect('/')

# パスワード再設定
@auth_bp.route("/reset", methods=['POST', 'GET'])
def reset():
    if request.method == 'POST':
        email = request.form.get('email')
        query = request.args.get('query')
        try:
            auth.send_password_reset_email(email)
            flash("パスワード再設定メールを送信しました")
            return redirect(f"/login?query={query}")
        except:
            flash("パスワード再設定メールの送信に失敗しました")
            return redirect(f"/login?query={query}")
    else:
        return render_template("reset.html")