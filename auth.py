from flask import Blueprint, render_template, request, redirect, session, flash, url_for, get_flashed_messages
from firebaseSetUp import auth, db

auth_bp = Blueprint('auth', __name__)

user_doc_ref = db.collection('user')

# ユーザーデータベースにいれるときのデータの型
user_format={
    "gender":None,
    "mangaAnswer":[],
    "favorite_manga":[],
    "username":None,
    "follow":[],
    "user_query":[],
    "review_query":[],
    "genre":None,   
}

# login
@auth_bp.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        username=request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
            # usernameが一致する最初のドキュメントを取得
            query = user_doc_ref.where('username', '==', username).limit(1)
            result = query.stream()

            # ドキュメントが存在すればそのIDを返す
            for doc in result:            
                return redirect(f'/{doc.id}/accesTest')
            flash("ユーザー名が登録されていません")
            return redirect("/")
        except:
                flash("ログインに失敗しました")
                return redirect("/")  
    else:
        messages = get_flashed_messages()
        return render_template("login.html", messages=messages)

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
    if request.method == 'POST':
        username=request.form.get('username')
        gender=request.form.get('gender')
        email = request.form.get('email')
        password = request.form.get('password')
        # usernameが重複していない場合
        if not is_username_duplicate(username):
            try:
                auth.create_user_with_email_and_password(email, password)
                
                # userのidを取得
                user_id=user_doc_ref.document().id
                # userデータベースに保存
                user_doc=user_doc_ref.document(user_id)
                user_format["username"]=username
                # デフォルトで外れ値を指定しておく
                user_format["mangaAnswer"]= [99.0 for x in range(140)]
                user_format["gender"]=gender
                user_doc.set(user_format)
                global flag
                flag=1
                flash("ユーザー登録が完了しました")
                return redirect(f"/{user_id}/genre")
            except:
                flash("ユーザー登録に失敗しました")
                return redirect("/")
            
        else:
            flash("ユーザーネームが重複しています")
            return redirect("/")    
    else:
        return render_template("userAdd.html")

@auth_bp.route("/logout")
def logput():
    session.pop('user', None)
    flash("ログアウトしました")
    return redirect('/')
