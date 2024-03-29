document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('reviewForm').addEventListener('submit', function(event) {
        event.preventDefault(); // デフォルトのフォーム送信を防止
        validateAndSubmit(); // バリデーション関数を呼び出し
    });
});

function star_update(rating) {
    for (let i = 1; i <= 5; i++) {
        const star = document.getElementById('starbutton_' + i);
        star.style.color = i <= rating ? 'gold' : 'gray';
    }
    document.getElementById('rating_input').value = rating;
}

function validateAndSubmit() {
    const title = document.getElementById('work_name').value;
    const rating = document.getElementById('rating_input').value;
    const comment = document.getElementById('comment').value;
    const errorMessage = document.getElementById('errorMessage');
    const submitButton = document.getElementById('submitbutton');

    errorMessage.textContent = '';

    // バリデーションチェック
    if (!title || rating == '0') {
        errorMessage.textContent = 'タイトル、評価を入力してください';
    } else {
        submitButton.disabled = true;
        submitButton.value = '送信中...';
        
        // フォーム送信
        document.getElementById('reviewForm').submit(); // バリデーションが成功した場合のみフォームを送信
    }
}

// 戻るボタン
function goBack(mangaTitle) {
    // console.log("戻るボタンが動作しています");
    const encodedTitle = encodeURIComponent(mangaTitle);
    location.href = `/${encodedTitle}/detail`;
}