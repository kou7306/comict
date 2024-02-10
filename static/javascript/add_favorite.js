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
        document.getElementById('loadingIndicator').style.display = 'block';
        // 検索欄を無効化
        document.getElementById('add_favorite_form').disabled = true;

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
        document.getElementById('loadingIndicator').style.display = 'none';

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
