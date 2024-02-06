let page = 1;

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

function searchBooks(page) {
    const searchType = document.getElementById('searchType').value;
    const searchTerm = document.getElementById('searchInput').value.trim();
    const sortOption = document.querySelector('select[name="sortOption"]').value;
    console.log(searchType, searchTerm, sortOption, page);

    if (searchTerm !== '') {
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
        console.log(results);
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