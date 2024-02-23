let currentPage = 1;
const pageSize = 8;
let isLoading = false;
let hasMore = true;

const tabs = document.querySelectorAll('.tab-item');
let activeTab = tabs[0];

function fetchComics(sortOption, page=1) {
    if (isLoading || !hasMore) return;
    isLoading = true;
    document.getElementById('loadingIndicator').classList.remove('hidden');

    fetch(`/api/comics?sort_option=${sortOption}&page=${page}&page_size=${pageSize}`)
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
            if (data.comics.length < pageSize) {
                hasMore = false;
            }

            appendComicsToDom(data.comics, sortOption);
            currentPage += 1;
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

let totalComicsCount = 0;

function appendComicsToDom(comics, sortOption) {
    const contentContainer = document.querySelector('#manga-content');
    contentContainer.classList.add('grid', 'grid-cols-4', 'gap-8', 'p-12');
    comics.forEach((comic) => {
        if (sortOption !== 'recommendations') {
            totalComicsCount += 1;
        }
        const mangaElement = document.createElement('div');
        mangaElement.classList.add('flex', 'flex-col', 'items-center', 'cursor-pointer', 'transform', 'transition', 'duration-500', 'hover:scale-110', 'rounded-lg');
        mangaElement.innerHTML = `
            <div class="w-64 h-full flex justify-center items-center overflow-hidden bg-gray-200 rounded-lg">
                <img src="${comic.image}" alt="${comic.title}" class="w-full h-auto object-cover rounded-lg">
            </div>
            <div class="flex items-baseline gap-2">
                ${sortOption !== 'recommendations' ? `<span class="font-black text-gray-400 text-3xl">${totalComicsCount}.</span>` : ''}
                <h3 class="mt-2 text-xl text-center">${comic.title}</h3>
            </div>
        `;
        mangaElement.addEventListener('click', () => {
            window.location.href = `/${encodeURIComponent(comic.title)}/detail`;
        });
        contentContainer.appendChild(mangaElement);
    });
}

window.addEventListener('scroll', () => {
    const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
    const sortOption = activeTab.getAttribute('data-tab');

    if (scrollTop + clientHeight >= scrollHeight - 5) {
        fetchComics(sortOption, currentPage);
    }
});

document.addEventListener('DOMContentLoaded', () => {

    const defaultSortOption = "recommendations";

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
            const contentContainer = document.querySelector('#manga-content');
            const messageContainer = document.querySelector('#error-message');
            messageContainer.innerHTML = '';
            contentContainer.innerHTML = '';
            currentPage = 1;
            totalComicsCount = 0;
            hasMore = true;
            fetchComics(sortOption, currentPage);
        });
    });

    // 初回の読み込み
    fetchComics(defaultSortOption, currentPage);
});