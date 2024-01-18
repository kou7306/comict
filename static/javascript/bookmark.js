
document.addEventListener("DOMContentLoaded", function () {
    // ブックマークトグルボタンのクリックイベント
    document.getElementById("bookmarkToggle").addEventListener("click", function () {
        // ローカルストレージから現在のブックマークの状態を取得
        const currentBookmarkState = localStorage.getItem("bookmarkState") === "true";
        const newBookmarkState = !currentBookmarkState;

        // ローカルストレージに新しいブックマークの状態を保存
        localStorage.setItem("bookmarkState", newBookmarkState);

        // ブックマークトグルボタンの状態を更新
        updateBookmarkButtonState(newBookmarkState);


        
        // サーバーにブックマークデータを送信
        fetch("/{{ user_id }}/bookmark", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                title: "{{ title }}",  // ブックマーク対象の漫画のタイトルなど、必要な情報を追加
            }),
        })
        .then(response => response.json())
        .then(data => {
            console.log("Bookmark toggled:", data);
            // 必要に応じてユーザーにフィードバックを表示するなどの処理を追加
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