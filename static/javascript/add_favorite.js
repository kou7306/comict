searchEnd = false;
// 作品名が入力された時の処理
function inputFunction(user_id,title){
  if(searchEnd){
    // POSTリクエストのオプションを設定
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json', // コンテントタイプをJSONに設定
            // 必要に応じて他のヘッダーを追加
        },
        body: JSON.stringify({
            title: title,
            // 他に送りたいデータがあればここに追加
        }),
        credentials: 'same-origin' // CSRF対策
    };

    // fetch APIを使用してリクエストを送信
    url = "/favoriteAdd";   
    fetch(url, options)
        .then(response => response.json()) // レスポンスのJSONを解析
        .then(data => {
            location.reload();
        })
        .catch(error => {
            console.error('Error:', error); // エラーをコンソールに表示
        });
  }
}


// 記録ができているかアラートで確認
function test(){
    window.alert("作品名は「"+workName.value+"」、評価は「"+rate+"」、コメントは「"+comment.value+"」です");
}




async function search(user_id) {
    var query = document.getElementById('favorite_title').value;
    searchEnd = false;

    if (query.trim() === '') {
        // 検索クエリが空の場合は処理しない
        return;
    }

    try {
        // ローディング表示
        document.getElementById('modalLoadingIndicator').style.display = 'flex';
        // 検索欄を無効化
        document.getElementById('modal').disabled = true;

        const response = await fetch('/search?query=' + query);
        const data = await response.json();

        var selectedTitle = data.manga_title;
        if (selectedTitle == null) {
            // 検索結果が空の場合は処理しない
            alert('作品がありませんでした');
            return;
        }

        // 選択された作品名を検索欄に入力
        document.getElementById('favorite_title').value = "";

        // ユーザーに確認
        var confirmation = confirm('選択された作品名: ' + selectedTitle + ' でよろしいですか？');

        if (confirmation) {
            // その後の処理を実行
            searchEnd = true;
            inputFunction(user_id,selectedTitle);
        } else {
            // キャンセル時の処理
            alert('キャンセルしました');
        }

    } catch (error) {
        console.error('エラーが発生しました:', error);
        alert('エラーが発生しました');
    } finally {
        // ローディング非表示
        document.getElementById('modalLoadingIndicator').style.display = 'none';

    }
}


// ブックマークの削除
function delete_manga(user_id,title){
   
    // POSTリクエストのオプションを設定
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json', // コンテントタイプをJSONに設定
            // 必要に応じて他のヘッダーを追加
        },
        body: JSON.stringify({
            title: title,
            // 他に送りたいデータがあればここに追加
        }),
        credentials: 'same-origin' // CSRF対策
    };

    // fetch APIを使用してリクエストを送信
    url =  "/favoriteDelete";   
    fetch(url, options)
        .then(response => response.json()) // レスポンスのJSONを解析
        .then(data => {
            location.reload(); // ページをリロードで更新
        })
        .catch(error => {
            console.error('Error:', error); // エラーをコンソールに表示
        });

  }

let currentPage = 1;
const pageSize = 8;
let isLoading = false;
let hasMore = true;

function fetchComics(page=1) {
    if (isLoading || !hasMore) return;
    isLoading = true;
    document.getElementById('loadingIndicator').style.display = 'flex';

    fetch(`/api/favoriteAdd?page=${page}&page_size=${pageSize}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.comics.length < pageSize) {
                hasMore = false;
            }

            appendComicsToDom(data.comics);
            currentPage += 1;
            isLoading = false;
            document.getElementById('loadingIndicator').style.display = 'none';

        })
        .catch(error => {
            isLoading = false;
            const messageContainer = document.querySelector('#error-message');
            if (messageContainer) {
                messageContainer.innerHTML = `<p>${error.message}</p>`;
            }
            document.getElementById('loadingIndicator').style.display = 'none';
            // document.getElementById('loadingIndicator').classList.add('hidden');

        });
}

function appendComicsToDom(comics) {
    const contentContainer = document.querySelector('#comic-container');
    contentContainer.classList.add('grid', 'grid-cols-4', 'gap-8', 'p-12');
    comics.forEach((comic) => {
        const mangaElement = document.createElement('div');
        mangaElement.classList.add('flex', 'flex-col', 'items-center', 'cursor-pointer', 'transform', 'transition', 'duration-500', 'hover:scale-110', 'rounded-lg');
        mangaElement.innerHTML = `
            <div class="w-64 h-full flex justify-center items-center overflow-hidden bg-gray-200 rounded-lg">
                <img src="${comic.image}" alt="${comic.title}" class="w-full h-auto object-cover rounded-lg">
            </div>
            <div class="flex items-baseline gap-2">
                <h3 class="mt-2 text-xl text-center">${comic.title}</h3>
            </div>
        `;
        mangaElement.addEventListener('click', () => {
            window.location.href = `/${encodeURIComponent(comic.title)}/detail`;
        });
        contentContainer.appendChild(mangaElement);
    });
}

window.addEventListener('scroll', () => {
    const { scrollTop, scrollHeight, clientHeight } = document.documentElement;

    if (scrollTop + clientHeight >= scrollHeight - 5) {
        fetchComics(currentPage);
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const addButton = document.getElementById('addButton');
    const modal = document.getElementById('modal');
    const closeModal = document.getElementById('closeModal');

    addButton.addEventListener('click', () => {
        modal.style.display = 'flex';
    });
    
    closeModal.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    // 初回の読み込み
    fetchComics(currentPage);
});
