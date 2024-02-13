function fetchAndDisplayReviews() {
    const sortOption = document.getElementById('sortOption').value;
    const titleElement = document.querySelector('.titleName');
    const title = encodeURIComponent(titleElement.getAttribute('data-title'));
  
    fetch(`/review/${title}?sort_option=${sortOption}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(reviews => {
        const container = document.getElementById('reviewContainer');
        container.innerHTML = ''; // コンテナを空にする
  
        reviews.forEach(review => {
          // レビューごとの表示内容を生成
          const reviewElement = document.createElement('div');
          const likeButtonText = review.liked ? 'いいねを取り消す' : 'いいね';
          reviewElement.innerHTML = `
            <p>ユーザー名: <a href="/${review.user_id}/userpage">${review.username}</a></p>
            <p>評価: ${review.evaluation}</p>
            <p>${review.contents}</p>
            <p id="likeCount-${review.id}">いいね数: ${review.likes_count}</p>
            <button id="likeButton-${ review.id }" onclick="toggleLike('${ review.id }')">${likeButtonText}</button>
          `;
          container.appendChild(reviewElement);
        });
      })
      .catch(error => console.error('Error fetching reviews:', error));
  }
  
  document.addEventListener('DOMContentLoaded', fetchAndDisplayReviews);
  document.getElementById('sortOption').addEventListener('change', fetchAndDisplayReviews);
