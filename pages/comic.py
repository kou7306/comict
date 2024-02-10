from flask import Blueprint, render_template, request, redirect, session, flash, url_for, get_flashed_messages
from firebaseSetUp import auth, db

comic_bp = Blueprint('comic', __name__)   

user_doc_ref = db.collection('user')

@comic_bp.route('/comic', methods = ['GET','POST'])
def comic():
    if request.method == 'GET':
        user_id = session.get('user_id')
        if not user_doc_ref.document(user_id).get().exists:
            return redirect("/login")
        if user_id:
            logged_in = True
        else:
            logged_in = False
        return render_template("comic.html",logged_in=logged_in)
