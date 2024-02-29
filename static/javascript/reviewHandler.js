// 漫画詳細画面での操作用
function fetchAndDisplayReviews() {
    const sortOption = document.getElementById('sortOption').value;
    const titleElement = document.querySelector('.titleName');
    const title = decodeURIComponent(titleElement.textContent);
    // console.log("title:", title);
  
    fetch(`/review/${title}?sort_option=${sortOption}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        const container = document.getElementById('reviewContainer');
        container.innerHTML = ''; // コンテナを空にする
        
        const loggedIn = data.logged_in;
  
        data.reviews.forEach(review => {
          // レビューごとの表示内容を生成
          // console.log('review:', review);
          const reviewElement = document.createElement('div');

          let likeElement;
          if (loggedIn) {
              likeElement = `<button id="like-button-${review.id}" class="focus:outline-none" onclick="handleLike('${review.id}')">
                                  ${review.liked ? '<span class="material-icons text-red-500">favorite</span>' : '<span class="material-icons">favorite_border</span>'}
                              </button>`;
          } else {
              likeElement = `${review.liked ? '<span class="material-icons text-red-500">favorite</span>' : '<span class="material-icons">favorite_border</span>'}`;
          }

          const formattedDate = new Date(review.created_at).toLocaleDateString('ja-JP', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
        });


        reviewElement.innerHTML = `
          <li class="my-8 p-4 bg-zinc-700">
            <span class="text-yellow-400 mt-2 text-xl">${'★ '.repeat(review.evaluation)}</span>
            <div class="flex items-center mt-2">
              <a href="/${review.user_id}/userpage" class="text-blue-500 hover:text-pink-400">${review.username}</a>
              <p class="mx-2">|</p>
              <p class="text-sm">${formattedDate}</p>
            </div>
            <p class="text-sm mt-2 break-words">${review.contents}</p>
            <div class="flex items-center mt-2">
              ${likeElement}
              <p id="likes-count-${review.id}" class="text-sm ml-4">${review.likes_count}</p>
            </div>
          </li>`;
          container.appendChild(reviewElement);
        });
      })
      .catch(error => console.error('Error fetching reviews:', error));
  }

  // いいねする関数
function handleLike(reviewId) {
  fetch(`/reviewLike/${reviewId}`, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
  })
  .then(response => {
      if (response.status === 401) {
          window.location.href = "/login?query=review_detail?review_id=" + reviewId;
      } else if (!response.ok) {
          throw new Error('Response was not ok');
      }
      return response.json();
  })
  .then(data => {
      updateLikeUI(reviewId, data);
  })
  .catch((error) => {
      console.error('Error:', error);
  });
}

// いいねのUIを変更する関数
function updateLikeUI(reviewId, data) {
  const likeButton = document.querySelector(`#like-button-${reviewId}`);
  const likesCountElemet = document.querySelector(`#likes-count-${reviewId}`);

  // 現在のいいね数を取得し、数値に変える
  let currentLikesCount = parseInt(likesCountElemet.textContent, 10);

  if (data.status === 'liked') {
      likeButton.innerHTML = '<span class="material-icons text-red-500">favorite</span>';
      currentLikesCount += 1;
  } else if (data.status === 'unliked') {
      likeButton.innerHTML = '<span class="material-icons">favorite_border</span>';
      currentLikesCount -= 1;
  }

  // 更新されたいいね数を表示要素に追加する
  likesCountElemet.textContent = currentLikesCount;
}

// 漫画詳細ページからレビューを投稿するページに遷移
function redirectToReviewAdd() {
  const titleElement = document.querySelector('.titleName');
  const title = decodeURIComponent(titleElement.textContent);
  location.href = '/reviewAdd/manga-detail?title=' + title;
}
  
document.addEventListener('DOMContentLoaded', fetchAndDisplayReviews);
document.getElementById('sortOption').addEventListener('change', fetchAndDisplayReviews);
