from flask import Flask,current_app,Blueprint, render_template, request, redirect, url_for, flash

review_bp = Blueprint('review', __name__)

with current_app.app_context():
    db = current_app.config['firestore_client']

user_doc_ref = db.collection('user')

all_user = user_doc_ref.stream()

review_doc_ref=db.collection('review')
# レビューデータベースに入れるときのデータの型
review_format={
    "mangaTitle":None,
    "evaluation":None,
    "contents":None,
    "username":None,
}

# レビュー投稿
@review_bp.route('/<user_id>/review',methods=['GET','POST'])
def review(user_id):
    if request.method == 'GET':
        return render_template("review.html",user_id=user_id)
    else:
        # formから取得
        work_name = request.form['work_name']
        rating = request.form['rating']
        comment = request.form['comment_text']
        # Firestoreから指定したuser_idに対応するユーザーネームを取得
        user_doc = user_doc_ref.document(user_id)
        user=user_doc.get()

        # 入力されたレビューのデータ
        review_format["evaluation"]=rating
        review_format["mangaTitle"]=work_name
        review_format["contents"]=comment
        review_format["username"]=user.to_dict()["username"]
        review_document=review_doc_ref.document() 
        review_document.set(review_format)
        return redirect(f"/{user_id}/review")