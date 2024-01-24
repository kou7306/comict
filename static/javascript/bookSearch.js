let page = 1;

window.addEventListener('scroll', () => {
    if (this.scrollTop + this.clientHeight >= (this.scrollHeight) * 0.8) {
        searchBooks(page);
        page++;
    }
});

function searchBooks(page) {
    const searchTerm = document.getElementById('searchInput').value.trim().toLowerCase();

    if (searchTerm !== '') {
        $.ajax({
            type: 'POST',
            url: '/<user_id>/bookSearch',
            data: { 
                searchInput: searchTerm,
                page: page
            },
            success: (data) => {
                displaySearchResults(data);
            },
            error: (error) => {
                console.error('検索エラー:', error);
            }
        });
    } else {
        alert('検索キーワードを入力してください');
    }
}

function displaySearchResults(response) {

    const results = response.results;
    const numResults = response.num_results;
    const user_id = response.user_id

    const resultsList = document.getElementById('searchResults');
        resultsList.innerHTML = '';

        if ('error' in results) {
            alert(results.error);
        } else {
            results.forEach(result => {
                const listItem = document.createElement('li');
                const link = document.createElement('a');

                link.href = `/${user_id}/${result.title}/detail`;
                link.textContent = result.title;
                
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