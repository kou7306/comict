from flask import Blueprint, render_template, request, redirect, session, flash, url_for, get_flashed_messages
from firebaseSetUp import auth, db


review_detail_bp = Blueprint('review_detail', __name__)   

user_doc_ref = db.collection('user')
review_doc_ref=db.collection('review')


# レビュー一覧
@review_detail_bp.route('/review_detail')
def review_detail():
    if request.method == 'GET':
        user_id = session.get('user_id')
        if not user_id is None and not user_doc_ref.document(user_id).get().exists:
            return redirect("/login")
       
        if user_id:
            logged_in = True
        else:
            logged_in = False
        
        review_id = request.args.get('review_id')
        review = review_doc_ref.document(review_id).get()

        return render_template("review_detail.html",review=review,logged_in=logged_in,user_doc_ref=user_doc_ref)
