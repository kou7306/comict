function searchBooks() {
    const searchTerm = document.getElementById('searchInput').value.trim().toLowerCase();

    if (searchTerm !== '') {
        $.ajax({
            type: 'POST',
            url: '/<user_id>/bookSearch',
            data: { searchInput: searchTerm},
            success: function(data) {
                displaySearchResults(data);
            },
            error: function(error) {
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

    const resultsList = document.getElementById('searchResults');
        resultsList.innerHTML = '';

        if ('error' in results) {
            alert(results.error);
        } else {
            results.forEach(result => {
                const listItem = document.createElement('li');
                listItem.textContent = result.title;
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