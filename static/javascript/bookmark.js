
document.addEventListener("DOMContentLoaded", function () {
    // ブックマークトグルボタンのクリックイベント
    document.getElementById("bookmarkToggle").addEventListener("click", function () {
        const user_id = this.getAttribute("user_id");
        // ローカルストレージから現在のブックマークの状態を取得
        const currentBookmarkState = localStorage.getItem("bookmarkState") === "true";
        const newBookmarkState = !currentBookmarkState;
        var bookmarkNumElement = document.getElementById('bookmark_num');
        // HTML要素を取得
        var h1Element = document.querySelector('.title1');

        // テキスト内容を取得
        var titleText = h1Element.textContent || h1Element.innerText;

        // 結果をコンソールに出力
        console.log(titleText);

        // ローカルストレージに新しいブックマークの状態を保存
        localStorage.setItem("bookmarkState", newBookmarkState);

        // ブックマークトグルボタンの状態を更新
        updateBookmarkButtonState(newBookmarkState);


        
        // サーバーにブックマークデータを送信
        fetch(`/${user_id}/bookmark`, {
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
            
            // ブックマーク数を更新

            console.log("Bookmark toggled:", data);
            bookmarkNumElement.textContent = `ブックマーク数：${data.bookmarked}`;
    
        })
        .catch(error => {
            console.error("Error toggling bookmark:", error);
        });
    });
});



// ブックマークトグルボタンの状態を更新する関数
function updateBookmarkButtonState(isBookmarked) {
    const button = document.getElementById("bookmarkToggle");
    button.textContent = isBookmarked ? "ブックマーク解除" : "ブックマーク";
    // 必要に応じて、ボタンのスタイルなども変更できます
}

document.addEventListener("DOMContentLoaded", function () {
    // ローカルストレージから現在のブックマークの状態を取得
    const currentBookmarkState = localStorage.getItem("bookmarkState") === "true";

    // ブックマークトグルボタンの状態を更新
    updateBookmarkButtonState(currentBookmarkState);
});