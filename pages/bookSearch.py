from flask import Blueprint, render_template, request, redirect, session, flash, url_for, get_flashed_messages, jsonify
from firebaseSetUp import auth, db

bookSearch_bp = Blueprint('bookSearch', __name__)
comics_doc_ref=db.collection('comics')


PER_PAGE = 10

# 作品検索機能
def search_books(search_type, search_input, sort_option, page):
        
    # Firestoreクエリを作成
    if search_type == "title":
        query = comics_doc_ref.where('title', '>=', search_input).where('title', '<=', search_input + '\uf8ff')

    elif search_type == "author":
        query = comics_doc_ref.where('author', '>=', search_input).where('author', '<=', search_input + '\uf8ff')
    
    
    start_index = (page - 1) * PER_PAGE
    query = query.offset(start_index).limit(PER_PAGE)
    
    docs = query.stream()
    
    # クエリ結果をリストに変換
    results = [{'id': doc.id, **doc.to_dict()} for doc in docs]
    
    # ソート処理
    if sort_option == "b_asc":
        results = sorted(results, key=lambda x: len(x['bookmark']))
    elif sort_option == "b_desc":
        results = sorted(results, key=lambda x: len(x['bookmark']), reverse=True)
    elif sort_option == "r_asc":
        results = sorted(results, key=lambda x: len(x['reviews']))
    elif sort_option == "r_desc":
        results = sorted(results, key=lambda x: len(x['reviews']), reverse=True)
        
    return results, len(results)


# 作品検索
@bookSearch_bp.route('/<user_id>/bookSearch', methods=['POST', 'GET'])
def BookSearch(user_id):
    if request.method == 'POST':

        search_type = request.form.get('searchType')

        search_input = request.form.get('searchInput').strip()
        sort_option = request.form.get('sortOption')
        page = request.args.get('page', 1)
        print(search_input)

        if search_input:
            results, num_results = search_books(search_type, search_input, sort_option, page)
            if num_results == 0:
                results = []
            
            response = {
                "results": results,
                "num_results": num_results,
                "user_id": user_id
            }
            
            return jsonify(response)
        else:
            return jsonify({"error": "検索ワードを入力してください"})
    else:
        return render_template('bookSearch.html',user_id=user_id)
