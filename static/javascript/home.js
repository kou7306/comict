window.addEventListener('load', function() {
	document.getElementById('loadingIndicator').style.display = 'none';
	overlay.style.display = "none";
  });
  
const mySwiper = new Swiper('.swiper', {
	slidesPerView: 2,
	slidesPerGroup: 2,
	spaceBetween: 16,
	grabCursor: true,
	pagination: {
		el: '.swiper-pagination',
		clickable: true,
	},
	navigation: {
		nextEl: '.swiper-button-next',
		prevEl: '.swiper-button-prev',
	},
	breakpoints: {
		600: {
			slidesPerView: 4,
			lidesPerGroup: 4,
			spaceBetween: 24,
		},
		1025: {
			slidesPerGroup: 6,
			slidesPerView: 6,
			spaceBetween: 32,
		}
	},
});

function showAlert() {
	alert('ボタンがクリックされました！');
}
