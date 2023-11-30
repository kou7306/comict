from flask import Flask, render_template, request, jsonify, redirect
import firebase_admin
from firebase_admin import credentials,firestore

#データベースの準備
cred = credentials.Certificate("key.json")

firebase_admin.initialize_app(cred)
db = firestore.client()

user_doc_ref = db.collection('user')

user_format={
    "gender":None,
    "mangaAnswer":[],
    "username":None,
}

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("question.html")


@app.route('/question', methods = ['GET', 'POST'])
def question():
    if request.method == 'GET':
        return render_template('templates/question.html')
    
    if request.method == 'POST':
        mangaAnswer = []

        #HTMLフォームからデータを受け取る
        for i in range(1,21):
            question_key = f'question-{i:02}'
            answer = request.form.get(question_key)
            answer=int(answer)
            mangaAnswer.append(answer)

        # データベースにデータを格納
        user_format['gender']=1
        user_format['mangaAnswer']=mangaAnswer
        user_format['username']="Syunsuke"

        user_document=user_doc_ref.document()
        user_document.set(user_format)

        return render_template("question.html")

if __name__ == '__main__':
    app.run(debug=True)