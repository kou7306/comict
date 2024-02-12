import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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
    
# yahoo image searchから画像をスクレイピングする関数
def image_scraping(url):
    # Chrome WebDriverをバックグラウンドで実行するためのオプションを設定
    #とりあえず可能な限りオプションを追加, headlessのみと時間はそう変わらない, 修正の余地あり
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')                      
    options.add_argument('--disable-extensions')               
    options.add_argument('--proxy-server="direct://"')         
    options.add_argument('--proxy-bypass-list=*')              
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_argument('--lang=ja')                          
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--log-level=3")
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.page_load_strategy = 'eager'

    # Webドライバーを起動
    driver = webdriver.Chrome(options=options)

    # WebページにアクセスしてHTMLデータを取得
    driver.get(url)
    html = driver.page_source
    
    # BeautifulSoupを使ってHTMLを解析
    soup = BeautifulSoup(html, 'html.parser')
    
    # 画像のURLを取得して保存
    img_tag = soup.find('img')
    image_url = img_tag['src']

    # Webドライバーを終了
    driver.quit()

    return image_url

def get_yahoo_book_cover(book_title):
    search_url=f"https://search.yahoo.co.jp/image/search?p={book_title}1巻"
    
    return image_scraping(search_url)