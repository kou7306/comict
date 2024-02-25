from flask import Blueprint, render_template, request, redirect, session, flash, url_for, get_flashed_messages
from firebaseSetUp import auth, db

check_bp = Blueprint('check', __name__)
user_doc_ref = db.collection('user')
# アンケートの確認
@check_bp.route("/check",methods = ['GET',"POST"])
def genre():
    user_id = session.get('user_id')


    if request.method == 'GET':
        if not user_doc_ref.document(user_id).get().exists:
            return redirect("/login?query=check")
        # ログインしてない場合
        if not user_id:
            return redirect('/login?query=check')
        else:
            if user_id:
                logged_in = True
            else:
                logged_in = False
            return render_template("check.html",user_id=user_id,logged_in=logged_in)
    else:
        # アンケートを開始
        return redirect('/genre')