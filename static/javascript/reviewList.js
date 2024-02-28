// レビュー一覧用javaScriptファイル
let lastReviewId;
let isLoading = false;
let hasMore = true;
const pageSize = 4;

// レビューをとってくる関数
function fetchReviews() {
    if (isLoading || !hasMore) return;
    isLoading = true;
    document.getElementById('loadingIndicator').classList.remove('hidden');

    const sortOption = document.getElementById('sort_option').value;

    fetch('/api/reviews', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            sortOption: sortOption,
            lastReviewId: lastReviewId,
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.reviews.length < pageSize) {
            hasMore = false;
        }

        appendReviewsToDom(data.reviews, data.logged_in);
        console.log('data:', data);
        console.log('data.logged_in:', data.logged_in);

        if (data.reviews.length > 0) {
            lastReviewId = data.reviews[data.reviews.length - 1].id;
            // console.log('lastReviewId:', lastReviewId);
        }

        isLoading = false;
        document.getElementById('loadingIndicator').classList.add('hidden');
        
    })
    .catch(error => {
        isLoading = false;
            const messageContainer = document.querySelector('#error-message');
            if (messageContainer) {
                messageContainer.innerHTML = `<p>${error.message}</p>`;
            }
            document.getElementById('loadingIndicator').classList.add('hidden');
    });
}

// レビューを作成、追加する関数
function appendReviewsToDom(data, loggedIn) {
    const contentContainer = document.querySelector('#review-container');
    data.forEach(review => {
        const reviewElement = document.createElement('div');
        reviewElement.classList.add('review', 'rounded-lg', 'over-flow-hidden', 'shadow-lg', 'm-2', 'p-4', 'transition', 'duration-500', 'hover:shadow-2xl');

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

        const reviewContent = `
            <div class="flex flex-col md:flex-row bg-zinc-700 text-white p-4 rounded-lg">
                <div class="md:w-1/4 flex justify-center items-center p-2">
                    <img src="${review.image}" alt="${review.mangaTitle}" style="width: 121px; height: 173px; object-fit: contain;" class="rounded-lg hover:scale-110 cursor-pointer transition-transform duration-300 review-image">
                </div>
                <div class="md:w-3/4 md:pl-4">
                    <p class="font-semibold">${review.mangaTitle}</p>
                    <p class="text-sm mt-2">${review.username}</p>
                    <span class="text-yellow-400 mt-2 text-xl">${'★ '.repeat(review.evaluation)}</span>
                    <p class="text-sm mt-2">${formattedDate}</p>
                    <p class="text-sm mt-2" style="word-wrap: break-word;">${review.contents}</p>
                    <div class="flex items-center mt-2">
                        ${likeElement}
                        <p id="likes-count-${review.id}" class="text-sm ml-4">${review.likes_count}</p>
                    </div>
                </div>
            </div>
        `;

        reviewElement.innerHTML = reviewContent;
        reviewElement.querySelector('.review-image').addEventListener('click', (e) => {
            e.stopPropagation();
            window.location.href = `/${encodeURIComponent(review.mangaTitle)}/detail`;
        });
        contentContainer.appendChild(reviewElement);
    });
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

// 無限スクロール機能
window.addEventListener('scroll', () => {
    const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
    if (scrollTop + clientHeight >= scrollHeight - 5 && !isLoading) {
        fetchReviews();
    }
});

// ロード時の操作
document.addEventListener('DOMContentLoaded', () => {
    fetchReviews(); 
});

// ソートオプションが変更された時の操作
document.getElementById('sort_option').addEventListener('change', () => {
    const contentContainer = document.querySelector('#review-container');
    contentContainer.innerHTML = '';

    lastReviewId = null
    hasMore = true;
    fetchReviews();
})