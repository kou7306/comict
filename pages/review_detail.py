from flask import Blueprint, render_template, request, redirect, session, flash, url_for, get_flashed_messages
from firebaseSetUp import auth, db


review_detail_bp = Blueprint('review_detail', __name__)   

user_doc_ref = db.collection('user')
review_doc_ref=db.collection('review')


# レビュー詳細
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
        review_data = review.to_dict()
        review_data['review_id'] = review_id
        
        likes = review_data.get('likes', [])
        if user_id in likes:
            review_data['liked'] = True
        else:
            review_data['liked'] = False
            
        r_user_id = review_data.get('user_id')
        if r_user_id:
            user_doc = user_doc_ref.document(r_user_id).get()
            if user_doc.exists:
                user_data = user_doc.to_dict()
                r_username = user_data.get('username')
                review_data['username'] = r_username

        return render_template("review_detail.html",review=review_data,logged_in=logged_in,user_doc_ref=user_doc_ref)
