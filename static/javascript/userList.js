let currentPage = 1;
const pageSize = 8;
let isLoading = false;
let hasMore = true;

const tabs = document.querySelectorAll('.tab-item');
let activeTab = tabs[0];

function fetchUser(sortOption, page=1) {
    if (isLoading || !hasMore) return;
    isLoading = true;
    var overlay = document.getElementById("overlay");
    overlay.style.display = "block";
    document.getElementById('loadingIndicator').style.display = 'flex';

    fetch(`/api/user?sort_option=${sortOption}&page=${page}&page_size=${pageSize}`)
        .then(response => {
            if (!response.ok) {
                if (response.status === 401) {
                    return response.json().then(data => {
                        const errorMessage = data.message || 'ログインしてください';
                        hasMore = false;
                        throw new Error(errorMessage);
                    });
                }
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.users.length < pageSize) {
                hasMore = false;
            }

            appendUsersToDom(data.users);
            currentPage += 1;
            isLoading = false;
            document.getElementById('loadingIndicator').style.display = 'none';
            overlay.style.display = "none";

        })
        .catch(error => {
            isLoading = false;
            const messageContainer = document.querySelector('#error-message');
            if (messageContainer) {
                messageContainer.innerHTML = `<p>${error.message}</p>`;
            }
            document.getElementById('loadingIndicator').style.display = 'none';
            overlay.style.display = "none";

        });
}

function appendUsersToDom(users) {
    const contentContainer = document.querySelector('#user-container');
    contentContainer.classList.add('grid', 'grid-cols-4', 'p-12', 'max-w-4xl');

    // users配列が空の場合、メッセージを表示
    if (currentPage == 1 && users.length === 0) {
        const noUsersMessage = document.createElement('div');
        noUsersMessage.classList.add('text-center', 'text-xl', 'col-span-4');
        noUsersMessage.textContent = '条件にマッチするユーザーが見つかりません';
        contentContainer.appendChild(noUsersMessage);
        return;
    }

    users.forEach((user) => {
        
        const mangaElement = document.createElement('div');
        mangaElement.classList.add('flex', 'flex-col', 'items-center', 'cursor-pointer', 'transform', 'transition', 'duration-500', 'hover:scale-110', 'rounded-lg');
        mangaElement.innerHTML = `
            <div class="w-48 h-full flex justify-center items-center overflow-hidden rounded-lg">
                <img src="https://kotonohaworks.com/free-icons/wp-content/uploads/kkrn_icon_user_1.png"
                 alt="${user.title}" class="w-32 h-auto object-cover rounded-lg"
                >
            </div>
            <div class="flex items-baseline gap-2">
                <h3 class="mt-2 text-xl text-center">${user.username}</h3>
            </div>
        `;
        mangaElement.addEventListener('click', () => {
            window.location.href = `/${encodeURIComponent(user.user_id)}/userpage`;
        });
        contentContainer.appendChild(mangaElement);
    });
}

window.addEventListener('scroll', () => {
    const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
    const sortOption = activeTab.getAttribute('data-tab');

    if (scrollTop + clientHeight >= scrollHeight - 50) {
        fetchUser(sortOption, currentPage);
    }
});

document.addEventListener('DOMContentLoaded', () => {

    const defaultSortOption = "suggestions";

    tabs.forEach(tab => {
        if (tab.getAttribute('data-tab') === defaultSortOption) {
            tab.classList.add('bg-blue-500', 'text-white');
        } else {
            tab.classList.remove('bg-blue-500', 'text-white');
            tab.classList.add('hover:bg-blue-500');
        }
    });

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => {
                t.classList.remove('bg-blue-500', 'text-white');
                t.classList.add('hover:bg-blue-500');
            });

            tab.classList.add('bg-blue-500', 'text-white');
            tab.classList.remove('hover:bg-blue-500');

            activeTab = tab;
            const sortOption = tab.getAttribute('data-tab');
            const contentContainer = document.querySelector('#user-container');
            const messageContainer = document.querySelector('#error-message');
            messageContainer.innerHTML = '';
            contentContainer.innerHTML = '';
            currentPage = 1;
            hasMore = true;
            fetchUser(sortOption, currentPage);
        });
    });

    // 初回の読み込み
    fetchUser(defaultSortOption, currentPage);
});