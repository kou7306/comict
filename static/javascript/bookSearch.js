let page = 1;
searchEnd = false;

window.addEventListener('scroll', () => {
    let scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
    let clientHeight = document.documentElement.clientHeight;
    let scrollHeight = document.documentElement.scrollHeight || document.body.scrollHeight;

    if (scrollTop + clientHeight >= scrollHeight * 0.8) {
        searchBooks(page);
        page++;
    }
});

let currentResults = [];

async function searchBooks(page,searchTerm) {
    const searchType = document.getElementById('searchType').value;
    
    const sortOption = document.querySelector('select[name="sortOption"]').value;



    if (searchTerm !== '' && searchEnd) {
        $.ajax({
            type: 'POST',
            url: '/<user_id>/bookSearch',
            data: { 
                searchType: searchType,
                searchInput: searchTerm,
                sortOption: sortOption,
                page: page
            },
            success: (data) => {
                const appendResults = page > 1;
                displaySearchResults(data, appendResults);
                if (appendResults) {
                    currentResults.results = currentResults.results.concat(data.results);
                } else {
                    currentResults = data;
                }
            },
            error: (error) => {
                console.error('検索エラー:', error);
            }
        });
    } else {
        alert('検索キーワードを入力してください');
    }
}

function displaySearchResults(response, append=false) {

    const results = response.results;
    const numResults = response.num_results;
    const user_id = response.user_id;

    const resultsList = document.getElementById('searchResults');
    if (!append) {
        resultsList.innerHTML = '';
    }

    if ('error' in results) {
        alert(results.error);
    } else {

        results.forEach(result => {
            const listItem = document.createElement('li');
            const link = document.createElement('a');

            link.href = `/${user_id}/${result.id}/detail`;
            link.textContent = `${result.id} - ブックマーク数: ${result.bookmark.length}, レビュー数: ${result.reviews.length}`;
            
            listItem.appendChild(link);
            resultsList.appendChild(listItem);
        });
    }

    const messageEl = document.getElementById('message');
    if(numResults === 0) {
        messageEl.textContent = '検索結果がありません';
    } else {
        messageEl.textContent = `${numResults}件の検索結果`;
    }
}

// 記録ができているかアラートで確認
function test(){
    window.alert("作品名は「"+workName.value+"」、評価は「"+rate+"」、コメントは「"+comment.value+"」です");
}



//　作品名を一意に
async function search(page) {
    const query = document.getElementById('searchInput').value.trim();
    searchEnd = false;

    if (query.trim() === '') {
        // 検索クエリが空の場合は処理しない
        return;
    }

    try {
        // ローディング表示
        document.getElementById('loadingIndicator').style.display = 'block';


        const response = await fetch('/search?query=' + query);
        const data = await response.json();

        var selectedTitle = data.manga_title;
        if (selectedTitle == null) {
            // 検索結果が空の場合は処理しない
            alert('作品がありませんでした');
            return;
        }

        // 選択された作品名を検索欄に入力
        document.getElementById('searchInput').value = "";

  
        searchEnd = true;
        searchBooks(page, selectedTitle);
            

    } catch (error) {
        console.error('エラーが発生しました:', error);
        alert('エラーが発生しました');
    } finally {
        // ローディング非表示
        document.getElementById('loadingIndicator').style.display = 'none';

    }
}