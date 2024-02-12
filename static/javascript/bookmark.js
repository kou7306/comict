
document.addEventListener("DOMContentLoaded", function () {
    // ブックマークトグルボタンのクリックイベント
    document.getElementById("bookmarkToggle").addEventListener("click", function () {

    
        var bookmarkNumElement = document.getElementById('bookmark_num');
        // HTML要素を取得
        var h1Element = document.querySelector('.titleName');

        // テキスト内容を取得
        var titleText = h1Element.textContent || h1Element.innerText;


        
        // サーバーにブックマークデータを送信
        fetch(`/bookmark`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                title: titleText,  // ブックマーク対象の漫画のタイトルなど、必要な情報を追加
            }),
        })
        .then(response => response.json())
        .then(data => {
            // ログインしていない場合はログインページにリダイレクト
            console.log(data.bookmarknum);
            if (data.bookmarknum == -1) {
                window.location.href = '/login?query=bookmark';
            }
            else{

                // ブックマークの状態を反転
                // const newBookmarkState = !currentBookmarkState;


                // ブックマークトグルボタンの状態を更新
                // updateBookmarkButtonState(newBookmarkState);

                // ブックマーク数を更新

                console.log("Bookmark toggled:", data);
                bookmarkNumElement.textContent = `ブックマーク数：${data.bookmarknum}`;
                document.getElementById("bookmarkToggle").textContent = data.bookmarked ? "ブックマーク解除":"ブックマーク";
    
            }

  
        })
        .catch(error => {
            console.error("Error toggling bookmark:", error);
        });
    });
});



// ブックマークトグルボタンの状態を更新する関数
// function updateBookmarkButtonState(isBookmarked) {
//     const button = document.getElementById("bookmarkToggle");
//     button.textContent = isBookmarked ? "ブックマーク" : "ブックマーク解除";
//     // 必要に応じて、ボタンのスタイルなども変更できます
// }

// document.addEventListener("DOMContentLoaded", function () {
//     // ローカルストレージから現在のブックマークの状態を取得
//     const currentBookmarkState = localStorage.getItem("bookmarkState") === "true";
//     console.log(currentBookmarkState);
//     // ブックマークトグルボタンの状態を更新
//     updateBookmarkButtonState(currentBookmarkState);
// });