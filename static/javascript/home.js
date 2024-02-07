var swiper = new Swiper('.mySwiper', {
     effect: 'coverflow',
     slidesPerView: 2,
     breakpoints: {
          // 画面幅が630px以上のとき
          630: {
            slidesPerView: 5,
          },
     },
     spaceBetween: 0,
     grabCursor: true,
     centeredSlides: true,
     coverflowEffect: {
          rotate: 15,
          stretch: 0,
          depth: 300,
          modifier: 1,
          slideShadows: true,
     },
     loop: true,
});

function showAlert() {
    alert('ボタンがクリックされました！');
}

