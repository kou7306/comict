from flask import Flask, render_template, request, redirect, session, url_for, flash, get_flashed_messages
import pyrebase

app = Flask(__name__)

config = {
    "apiKey": "AIzaSyBPva6sGWXi6kjmk8mjWWVCGEKKEBIfTIY",
    "authDomain": "giikucamp12.firebaseapp.com",
    "projectId": "giikucamp12",
    "storageBucket": "giikucamp12.appspot.com",
    "messagingSenderId": "755980381836",
    "appId": "1:755980381836:web:acdae710db8366cc4095a9",
    "measurementId": "G-00EVCKC0JQ",
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

app.secret_key = "secret"

@app.route("/accesTest")
def accesTest():
    if 'user' in session:
        return render_template("accesTest.html")
    else:
        flash("ログインしてください")
        return redirect("/")

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
            return redirect(url_for('accesTest'))
        except:
            flash("ログインに失敗しました")
            return redirect("/")
    messages = get_flashed_messages()
    return render_template("login.html", messages=messages)

@app.route("/userAdd", methods=['POST', 'GET'])
def userAdd():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            auth.create_user_with_email_and_password(email, password)
            flash("ユーザー登録が完了しました")
            return redirect("/")
        except:
            flash("ユーザー登録に失敗しました")
            return redirect("/")
    else:
        return render_template("userAdd.html")

@app.route("/reset", methods=['POST', 'GET'])
def reset():
    if request.method == 'POST':
        email = request.form.get('email')
        try:
            auth.send_password_reset_email(email)
            flash("パスワード再設定メールを送信しました")
            return redirect("/")
        except:
            flash("パスワード再設定メールの送信に失敗しました")
            return redirect("/")
    else:
        return render_template("reset.html")

@app.route("/logout")
def logput():
    session.pop('user', None)
    flash("ログアウトしました")
    return redirect('/')

if __name__ == "__main__":
    app.run(port=5000, debug=True)
    