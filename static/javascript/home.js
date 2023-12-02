let currentIndex = 0;
const cardsContainer = document.querySelector('.cards-container');
const cards = document.querySelectorAll('.card');
const cardWidth = cards[0].offsetWidth + 10; // カードの幅 + マージン

function showCards() {
  cardsContainer.style.transform = `translateX(${-currentIndex * cardWidth}px)`;
}

function nextCard() {
  currentIndex = (currentIndex + 1) % cards.length;
  showCards();
}

function prevCard() {
  currentIndex = (currentIndex - 1 + cards.length) % cards.length;
  showCards();
}

showCards();
