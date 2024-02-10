from flask import Blueprint, render_template, request, redirect, session, flash, url_for, get_flashed_messages,jsonify
from firebaseSetUp import auth, db
from funcs.wiki import get_manga_title,get_wikipedia_page_details


getTitle_bp = Blueprint('getTitle', __name__)

# 漫画の正式タイトルを取得
@getTitle_bp.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    
    if query:
        manga_title = get_manga_title(query)
        return jsonify({'manga_title': manga_title})
