// 作品名のID取得
const workName = document.getElementById("work");
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
  if(workName.value && rate>=1){
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
}

// 記録ができているかアラートで確認
function test(){
    window.alert("作品名は「"+workName.value+"」、評価は「"+rate+"」、コメントは「"+comment.value+"」です");
}