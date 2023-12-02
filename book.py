import requests

def get_rakuten_book_cover(book_title):
    api_key = '1078500249535096776'
    base_url = 'https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404'

    params = {
        'format': 'json',
        'applicationId': api_key,
        'title': book_title,
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if 'Items' in data and data['Items']:
        first_item = data['Items'][0]['Item']
        small_image_url = first_item.get('smallImageUrl', 'Image not available')
        return small_image_url
    else:
        return 'Book not found'

# 例: "ワンピース"という本の表紙画像のURLを取得
book_cover_url = get_rakuten_book_cover('OnePiece')
print(book_cover_url)