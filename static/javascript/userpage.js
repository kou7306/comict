const modalOpen = document.getElementsByClassName('modal-open');
const dialog = document.getElementsByClassName('modal');
const modalClose = document.getElementsByClassName('modal-close');
const updateButton = document.getElementsByClassName('update-button');

modalOpen[0].addEventListener('click', () => {
    dialog[0].showModal();
});

modalClose[0].addEventListener('click', () => {
    dialog[0].close();
});

updateButton[0].addEventListener('click', () => {
    dialog[0].close();
});

