from flask import Blueprint, render_template, request, redirect, session, flash, url_for, get_flashed_messages,jsonify
from firebaseSetUp import auth, db
from funcs.wiki import get_manga_title,get_wikipedia_page_details


getTitle_bp = Blueprint('getTitle', __name__)

comic_doc_ref = db.collection('comics') 
# 漫画の正式タイトルを取得
@getTitle_bp.route('/search', methods=['GET'])
def search():
    
    query = request.args.get('query')


    
    if query:
        manga_title = get_manga_title(query)
      

        if comic_doc_ref.document(manga_title).get().exists:
            return jsonify({'manga_title': manga_title, 'is_exist': True})
        elif comic_doc_ref.where('title', '>=', query).where('title', '<=', query + '\uf8ff').stream().exists():
            return jsonify({'manga_title': query, 'is_exist': True})  
        else:
            return jsonify({'manga_title': manga_title, 'is_exist': False})
        
    else:
        return jsonify({'manga_title': None, 'is_exist': False})
