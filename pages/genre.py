from flask import Blueprint, render_template, request, redirect, session, flash, url_for, get_flashed_messages
from firebaseSetUp import auth, db

genre_bp = Blueprint('genre', __name__)
user_doc_ref = db.collection('user')
# ジャンル選択
@genre_bp.route("/genre",methods = ['GET',"POST"])
def genre():
    user_id = session.get('user_id')


    if request.method == 'GET':
        if not user_doc_ref.document(user_id).get().exists:
            return redirect("/login")
        # ログインしてない場合
        if not user_id:
            return redirect('/login')
        else:
            if user_id:
                logged_in = True
            else:
                logged_in = False
            return render_template("genre.html",user_id=user_id,logged_in=logged_in)
    else:
        # フォームからジャンルを取得し、データベースに追加
        genre = request.form['genre']
        update_data = {"genre":genre}
        user_doc = user_doc_ref.document(user_id)
        user_doc.update(update_data)
        return redirect(f'/{genre}/question')