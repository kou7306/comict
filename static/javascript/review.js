// 作品名のID取得
const workName = document.getElementById("searchInput");
//検索終了フラグ
let searchEnd = false;
// ★のボタンのIDを配列で取得
const starbuttons  =
[document.getElementById("starbutton_1"),
document.getElementById("starbutton_2"),
document.getElementById("starbutton_3"),
document.getElementById("starbutton_4"),
document.getElementById("starbutton_5")]
// コメントのID取得
const comment = document.getElementById("comment");
// 記録ボタンのID取得
const submitbutton = document.getElementById("submitbutton");

// 記録ボタンは非活性にしておく
submitbutton.disabled=true;

// star_update関数以外で★の数を使うため
let rate = 0;

// 作品名が入力された時の処理
function inputFunction(){
  if(searchEnd && rate>=1){
    submitbutton.disabled=false;
  }
}

// ★のボタンが押された時の処理
function star_update(n){
    rate = n;
    // ★のボタンに一つづつ色を付けていく
    for (let i=1;i<=5;i++){
        if (i<=rate){
            starbuttons[i-1].style.color = "#ffcd00";
        } else {
            starbuttons[i-1].style.color = "gray";
        }
    }
    inputFunction();
    // rating_input の値を更新
    const ratingInput = document.getElementById('rating_input');
    ratingInput.value = rate;
}

// 記録ができているかアラートで確認
function test(){
    window.alert("作品名は「"+workName.value+"」、評価は「"+rate+"」、コメントは「"+comment.value+"」です");
}

// rateをPOSTで送る



async function search() {
    var query = document.getElementById('searchInput').value;
    searchEnd = false;
    if (query.trim() === '') {
        // 検索クエリが空の場合は処理しない
        return;
    }

    try {
        // ローディング表示
        document.getElementById('loadingIndicator').style.display = 'block';
        // 検索欄を無効化
        document.getElementById('searchInput').disabled = true;

        const response = await fetch('/search?query=' + query);
        const data = await response.json();

        var selectedTitle = data.manga_title;
        if (selectedTitle == null) {
            // 検索結果が空の場合は処理しない
            alert('検索結果がありませんでした');
            return;
        }

        // 選択された作品名を検索欄に入力
        document.getElementById('searchInput').value = selectedTitle;

        // ユーザーに確認
        var confirmation = confirm('選択された作品名: ' + selectedTitle + ' でよろしいですか？');

        if (confirmation) {
            // その後の処理を実行
            searchEnd = true;
            inputFunction();
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
        // 検索欄を有効化
        document.getElementById('searchInput').disabled = false;
    }
}