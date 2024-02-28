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
            requested_user_id: user_id, //更新したいuser_id
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
        // 検索クエリが空の場合
        document.getElementById('message').textContent = '作品名を入力してください';
        return;
    } else {
        // クエリが空でない場合、メッセージをクリア
        document.getElementById('message').textContent = '';
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
function delete_manga(title){
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
const pageSize = 9;
let isLoading = false;
let hasMore = true;
let userId;

function fetchComics(userId, page=1) {
    if (isLoading || !hasMore) return;
    isLoading = true;
    document.getElementById('loadingIndicator').style.display = 'flex';

    fetch(`/api/favoriteAdd?user_id=${userId}&page=${page}&page_size=${pageSize}`)
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

            appendComicsToDom(data.comics, data.is_own);
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
let isFirstLoad = true;

function appendComicsToDom(comics, isOwn) {
    const contentContainer = document.querySelector('#comic-container');
    contentContainer.classList.add('grid', 'grid-cols-3', 'gap-8', 'p-12', 'max-w-screen-lg', 'mx-auto');

    // comics配列が空の場合、メッセージを表示
    if (isFirstLoad && comics.length === 0) {
        const noComicsMessage = document.createElement('div');
        noComicsMessage.classList.add('text-center', 'text-xl', 'col-span-4');
        noComicsMessage.textContent = 'お気に入り作品はありません'
        contentContainer.appendChild(noComicsMessage);
        isFirstLoad = false;
        return;
    }
    comics.forEach((comic) => {
        const deleteButtonHTML = isOwn ? `<button onclick="event.stopPropagation(); delete_manga('${comic.title}')" class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">削除</button>` : '';
        
        const mangaElement = document.createElement('div');
        mangaElement.classList.add('flex', 'flex-col', 'items-center', 'cursor-pointer', 'transform', 'transition', 'duration-500', 'hover:scale-110', 'rounded-lg', 'justify-self-center');
        mangaElement.innerHTML = `
            <div class="w-64 h-full flex justify-center items-center overflow-hidden rounded-lg">
                <img src="${comic.image}" alt="${comic.title}" style="width: 121px; height: 173px; object-fit: contain;" class="rounded-lg">
            </div>
            <div class="flex items-baseline gap-2">
                <h3 class="mt-2 text-xl text-center">${comic.title}</h3>
                ${deleteButtonHTML}
            </div>
        `;
        mangaElement.addEventListener('click', () => {
            window.location.href = `/${encodeURIComponent(comic.title)}/detail`;
        });
        contentContainer.appendChild(mangaElement);
        isFirstLoad = false;
    });
}

window.addEventListener('scroll', () => {
    const { scrollTop, scrollHeight, clientHeight } = document.documentElement;

    if (scrollTop + clientHeight >= scrollHeight - 5) {
        fetchComics(userId, currentPage);
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const addButton = document.getElementById('addButton');
    const modal = document.getElementById('modal');
    const closeModal = document.getElementById('closeModal');
    const pageInfo = document.getElementById('page-info');
    userId = pageInfo.getAttribute('data-user-id');
    // console.log("見たいユーザーのID:", userId);

    if (addButton) {
        addButton.addEventListener('click', () => {
            modal.style.display = 'flex';
        });
        
        closeModal.addEventListener('click', () => {
            document.getElementById('message').textContent = '';
            modal.style.display = 'none';
        });
    }

    // 初回の読み込み
    fetchComics(userId, currentPage);
});
