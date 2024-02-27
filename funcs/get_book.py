import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
import urllib.request
from urllib.parse import quote
import httplib2
import json
import os
from firebaseSetUp import auth, db








# 楽天ブックスAPIを叩く関数
def get_rakuten_book_cover(book_title):
    api_key = '1078500249535096776'
    base_url = 'https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404'

    params = {
        'format': 'json',
        'applicationId': api_key,
        'title': f"{book_title}",
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if 'Items' in data and data['Items']:
        first_item = data['Items'][0]['Item']
        image_url = first_item.get('largeImageUrl', first_item.get('mediumImageUrl', 'Image not available'))
        return image_url
    else:
        return "no"
    
# custom search APIから画像検索を行う
def get_google_book_cover(book_title):

    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    print('kkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
    print('key'+GOOGLE_API_KEY)

    CUSTOM_SEARCH_ENGINE_ID = "3354fe1c38e254ad8"


   
   
   
    search_word=f"{book_title}1巻"
    url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={CUSTOM_SEARCH_ENGINE_ID}&searchType=image&q={search_word}&num=2"

    # APIリクエストを送信して検索結果を取得
    response = requests.get(url)
    data = response.json()

    # 最初にヒットした画像のURLを取得して返す
    if 'items:' in data and len(data['items']) > 0:
        image_url = data['items'][0]['link']
        print('img'+image_url)
        return image_url
    else:
        return None
