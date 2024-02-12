function toggleLike(reviewId) {

    fetch(`/reviewLike/${reviewId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (response.status === 401) {
            window.location.href = "/login?query=review";
        } else if (!response.ok) {
            throw new Error('Response was not ok');
        }
        return response.json();
    })
    .then(data => {
        const likeCountElement = document.querySelector(`#likeCount-${reviewId}`);
        let likeCount = parseInt(likeCountElement.textContent.replace('いいね数: ', ''), 10);

        const likeButton = document.querySelector(`#likeButton-${reviewId}`);

        if (data.status === 'liked') {
            likeCount += 1
            likeButton.textContent = 'いいねを取り消す';
        } else {
            likeCount -= 1;
            likeButton.textContent = 'いいね';
        }

        likeCountElement.textContent = `いいね数: ${likeCount}`;
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

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
          reviewElement.innerHTML = `
            <p>ユーザー名: <a href="/${review.user_id}/userpage">${review.username}</a></p>
            <p>評価: ${review.evaluation}</p>
            <p>${review.contents}</p>
            <p id="likeCount-${review.id}">いいね数: ${review.likes_count}</p>
            <button id="likeButton-${ review.id }" onclick="toggleLike('${ review.id }')">いいね</button>
          `;
          container.appendChild(reviewElement);
        });
      })
      .catch(error => console.error('Error fetching reviews:', error));
  }
  
  document.addEventListener('DOMContentLoaded', fetchAndDisplayReviews);
  document.getElementById('sortOption').addEventListener('change', fetchAndDisplayReviews);
  