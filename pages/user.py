from flask import Blueprint, render_template, request, redirect, session, flash, url_for, get_flashed_messages
from firebaseSetUp import auth, db


user_bp = Blueprint('user', __name__)
user_doc_ref = db.collection('user')


@user_bp.route('/user')
def user():
    # セッションからユーザーIDを取得（未ログインの場合はNoneが返る）
    user_id = session.get('user_id')
    if not user_id is None and not user_doc_ref.document(user_id).get().exists:
        return redirect('/login') 
    # ユーザーIDの有無に応じて、テンプレートに渡す変数を設定
    if user_id:
        logged_in = True
    else:
        logged_in = False
    if logged_in:
        user=user_doc_ref.document(user_id).get()
        # フォロワーの情報を取得
        follow_data = []
        
        if user.to_dict()["follow"] != None:
            for follow_id in user.to_dict()["follow"]:
                if follow_id != "":
                    print(follow_id)
                    follow_doc = user_doc_ref.document(follow_id).get()
                    if follow_doc.exists:
                        follow_name = follow_doc.to_dict()["username"]
                        follow_data.append((follow_name, follow_id))
                    print(follow_data)
        else:
            follow_data = []
        return render_template("user.html",user_id=user_id,user_doc_ref=user_doc_ref,follow_data=follow_data,user_query=user.to_dict()['user_query'],username=user.to_dict()["username"],logged_in=logged_in)        
    else:
        return render_template("user.html",logged_in=logged_in)