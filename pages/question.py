from flask import Blueprint, render_template, request, redirect, session, flash, url_for, get_flashed_messages
from firebaseSetUp import auth, db
from funcs.matching import matching

question_bp = Blueprint('question', __name__)
user_doc_ref = db.collection('user')

# アンケート回答を受信
@question_bp.route('/<genre>/question', methods = ['GET','POST'])
def question(genre):
    user_id = session.get('user_id')
    if request.method == 'GET':
        if not user_doc_ref.document(user_id).get().exists:
            return redirect('/login') 
        if user_id:
            logged_in = True
        else:
            logged_in = False
        return render_template("question"+ genre + '.html',user_id=user_id,genre=genre,logged_in=logged_in)
    else:

        #長さ20*８のリストを作成し、０で初期化する
        mangaAnswer = [0.0] *140

        genre=int(genre)
        first_index = 20 * (genre - 1)

        #HTMLフォームからデータを受け取る
        for i in range(1,20):
            question_key = f'question-{i:02}'
            answer = request.form[question_key]
            answer=float(answer)
            mangaAnswer[first_index + (i-1)]=answer
            
        # Firestoreから指定したuser_idに対応するユーザーネームを取得
        user_doc = user_doc_ref.document(user_id)
        user=user_doc.get()
        # データベースにデータを格納

        user_doc.update({'mangaAnswer':mangaAnswer,'username':user.to_dict()["username"]})
        # マッチング
        review_query, user_query =matching(user.to_dict()["mangaAnswer"],user_id)
       
        update_data = {"user_query":  user_query,"review_query":review_query}
        user_doc.update(update_data)
     
        
        return redirect('/home')