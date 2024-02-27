import wikipedia
import requests
from bs4 import BeautifulSoup

def get_wikipedia_page_details(title):
    endpoint = "https://ja.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "extracts|info|pageimages",
        "inprop": "url",
        "exintro": True,
        "explaintext": True,
        "piprop": "thumbnail",
        "pithumbsize": 300  # サムネイルのサイズを指定
    }

    response = requests.get(endpoint, params=params)
    data = response.json()
    
    page_id = list(data["query"]["pages"].keys())[0]
    page = data["query"]["pages"][page_id]

    url = page.get("fullurl", "")

    return url
        




def get_manga_title(title):
    wikipedia.set_lang('ja')

    # 最初の検索結果から漫画のカテゴリを取得
    search_response = wikipedia.search(title)

    print(search_response)

    while search_response:
        # 正確なページタイトルを取得
        try:
            page_title = wikipedia.page(search_response[0]).title
        except wikipedia.exceptions.DisambiguationError as e:
            # 曖昧性のあるページの場合、最初の候補を使用
            page_title = e.options[0]

        # ページ情報を取得
        page_data = wikipedia.page(page_title)
        categories = page_data.categories

 

       
        # カテゴリが「漫画」のものを検索
        for category in categories:
            
            if '漫画' in category:
                print(f'入力されたタイトル "{title}" の正確なページタイトル: {page_title}')
                return page_title
            

        # 次の検索結果を取得
        if len(search_response) > 1:
            search_response = wikipedia.search(search_response[1])
        else:
            print(f'入力されたタイトル "{title}" に関連する「漫画」のカテゴリは見つかりませんでした。')
            return None
    
    return None
        

def get_manga_detail():
    wikipedia.set_lang('ja')

    

# 例として「東リべ」の漫画のカテゴリと正確なページタイトルを取得
# get_manga_title('東リべ')　-->　入力されたタイトル "東リべ" の正確なページタイトル: 東京リベンジャーズが帰ってくる




# ジャンルを取得
def get_manga_genre(title):
    wikipedia.set_lang('ja')

    # 漫画のWikipediaページを検索
    search_results = wikipedia.search(title)
    print(search_results)

    

        # ページ情報を取得
    page = wikipedia.page(search_results[0])
    url = page.url

    # ページのHTMLを取得
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features='html.parser')


    # インフォボックスを探す
    infobox = soup.find('table', class_='infobox bordered')
   

    if infobox:
        # ジャンルの行を探す
        for row in infobox.find_all('tr'):
            header = row.find('th')
            if header and 'ジャンル' in header.get_text():
                genre_cell = row.find('td')
                if genre_cell:
                    return genre_cell.get_text().strip()

    return None
