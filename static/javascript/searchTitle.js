async function searchTitle() {
    var overlay = document.getElementById("overlay");
    overlay.style.display = "block";
    document.getElementById('loadingIndicator').style.display = 'flex';
    var title = document.getElementById('searchInput').value;
    
    // titleをAPIに渡す処理をここに記述する
    //　正式名称に変換

    const response = await fetch('/search?query=' + title);
    const data = await response.json();
    console.log(data);

    var selectedTitle = data.manga_title;
    var is_exist = data.is_exist;
    if (selectedTitle == null || is_exist == false) {
        document.getElementById('loadingIndicator').style.display = 'none';
        // 検索結果が空の場合は処理しない
        alert('作品がありませんでした');
        
        return;
    }
    else {
        document.getElementById('loadingIndicator').style.display = 'none';
        // 選択された作品名を検索欄に入力
        document.getElementById('searchInput').value = "";
        // 漫画のページに遷移
        window.location.href = `/${selectedTitle}/detail`;
        return;
    }



}