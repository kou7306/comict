from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/get_book_cover', methods=['POST'])
def get_book_cover():
    book_name = request.form.get('book_name')

    # Google Books APIへのリクエスト
    response = requests.get(
        'https://www.googleapis.com/books/v1/volumes', params={'q': book_name})

    # レスポンスのJSONデータを取得
    books_data = response.json()

    if 'items' in books_data and len(books_data['items']) > 0:
        first_book_info = books_data['items'][0]['volumeInfo']
        image_links = first_book_info.get('imageLinks', {})
        thumbnail_url = image_links.get('thumbnail', 'Image not available')
        return render_template('book_cover.html', thumbnail_url=thumbnail_url)
    else:
        return render_template('book_cover.html', error_message='Book not found')

if __name__ == '__main__':
    app.run(debug=True)