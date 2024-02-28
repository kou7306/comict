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
    search_results = wikipedia.search(title)


    

    for result in search_results:
        # 正確なページタイトルを取得
        try:
            page = wikipedia.page(result)
        except wikipedia.exceptions.DisambiguationError as e:
            # 曖昧性のあるページの場合、漫画カテゴリに属する最初の候補を選択
            for option in e.options:
                try:
                    option_page = wikipedia.page(option)
                    if any('漫画' in category for category in option_page.categories):
                        print(f'入力されたタイトル "{title}" の正確なページタイトル: {option}')
                        return option
                except wikipedia.exceptions.PageError:
                    continue
        except wikipedia.exceptions.PageError:
            continue

        # カテゴリが「漫画」のものを検索
        if any('漫画' in category for category in page.categories):
            print(f'入力されたタイトル "{title}" の正確なページタイトル: {page.title}')
            return page.title

    print(f'入力されたタイトル "{title}" に対応する漫画のページが見つかりませんでした。')
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
