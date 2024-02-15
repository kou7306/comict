from flask import jsonify, request,Blueprint
from firebaseSetUp import db
from funcs.review_sort import review_sort

load_more_data_bp = Blueprint('load_more_data', __name__)

@load_more_data_bp.route('/load-more-data', methods=['POST'])
def load_more_data():
    sort_option = request.json.get('sort_option')
    start_after = request.json.get('start_after')

    # start_afterが指定されていればそれを使ってデータを取得し、そうでなければ先頭から取得する
    reviews = review_sort(sort_option,start_after)



    return jsonify(reviews)
