import wikipedia
import requests

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
        

# 使用例
# get_wikipedia_page_details("One Piece")


def get_manga_title(title):
    wikipedia.set_lang('ja')

    # 最初の検索結果から漫画のカテゴリを取得
    search_response = wikipedia.search(title)

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
        

def get_manga_detail():
    wikipedia.set_lang('ja')

    

# 例として「ワンピース」の漫画のカテゴリと正確なページタイトルを取得
# get_manga_category_and_title('はがない')
