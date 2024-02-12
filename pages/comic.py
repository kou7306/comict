from flask import Blueprint, render_template, request, redirect, session, flash, url_for, get_flashed_messages
from firebaseSetUp import auth, db
from funcs.get_book import get_yahoo_book_cover
from funcs.get_book import get_rakuten_book_cover

comic_bp = Blueprint('comic', __name__)   

user_doc_ref = db.collection('user')
review_doc_ref=db.collection('review')

@comic_bp.route('/comic', methods = ['GET','POST'])
def comic():
    if request.method == 'GET':
        user_id = session.get('user_id')
        if not user_id is None and not user_doc_ref.document(user_id).get().exists:
            return redirect("/login")
        if user_id:
            logged_in = True
        else:
            logged_in = False
        if logged_in:
            user=user_doc_ref.document(user_id).get()


            # flagが2の時イントロダクションを表示
            
            # 漫画の画像取得
            favolite_book_urls = []
            book_urls=[]
            titles=[]
            if user.to_dict()['review_query'] != None:
                for id in user.to_dict()['review_query']:
                    review=review_doc_ref.document(id).get()
                    eval=review.to_dict()["evaluation"]
                    # 4以上の評価のものだけ取得
                    if(int(eval)>=4):
                        title=review.to_dict()["mangaTitle"]  
                        titles.append(title)
                        #image=get_rakuten_book_cover(title)
                        image=get_yahoo_book_cover(title)
                        book_urls.append(image)
                data=list(zip(titles,book_urls))
            else:    
                data = []

            # お気に入り漫画の画像取得
            if user.to_dict()['user_query'] != None:
                for id in user.to_dict()['user_query']:
                    if user_doc_ref.document(id).get().to_dict()["bookmark"] != None:
                        favorite_titles = user_doc_ref.document(id).get().to_dict()["bookmark"]
                        for title in favorite_titles:    
                            image=get_rakuten_book_cover(title)
                            favolite_book_urls.append(image) 
            else:
                favolite_book_urls = []
            
            return render_template("comic.html",logged_in=logged_in,data=data,favolite_book_urls=favolite_book_urls)
        else:
            return render_template('comic.html',logged_in=logged_in)
