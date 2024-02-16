function toggleLike(reviewId) {

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
        if (data.error != "Unauthorized") {
            const likeCountElement = document.querySelector(`#likeCount-${reviewId}`);
            let likeCount = parseInt(likeCountElement.textContent.replace('いいね数: ', ''), 10);

            const likeButton = document.querySelector(`#likeButton-${reviewId}`);
            const heartIcon = likeButton.querySelector('i');

            if (data.status == 'liked') {
                likeCount += 1
                likeButton.innerHTML = `
                <i class="material-icons" style="color: rgb(255, 73, 234);">favorite</i>
                `
            } else {
                console.log('unliked');
                likeCount -= 1;
                likeButton.innerHTML = `
                <i class="material-icons">favorite_border</i>
                `
            }
    
    
            likeCountElement.textContent = `いいね数: ${likeCount}`;
            console.log('Success:', data);
        }

    })
    .catch((error) => {
        console.error('Error:', error);
    });
}