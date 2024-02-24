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
          <a href="/review_detail?review_id=${review.id}" class="block hover:scale-105">
            <li class="my-4 p-4 bg-zinc-700">
              <p>タイトル：${review.mangaTitle}</p>
              <p>${review.username}</p>
              ${Array(review.evaluation).fill().map(() => '<span class="text-yellow-400">★</span>').join('')}
              <p style="word-wrap: break-word;">${review.contents}</p>
              <p>いいね数：${review.likes_count}</p>
            </li>
          </a>`;
          container.appendChild(reviewElement);
        });
      })
      .catch(error => console.error('Error fetching reviews:', error));
  }
  
  document.addEventListener('DOMContentLoaded', fetchAndDisplayReviews);
  document.getElementById('sortOption').addEventListener('change', fetchAndDisplayReviews);
