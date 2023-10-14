const swiper = new Swiper(".swiper", {
  // Optional parameters
  direction: "horizontal",

  speed: 400,
  spaceBetween: 30,
  freeMode: true,
  slidesPerView: 2.5,

  // If we need pagination
  // pagination: {
  //   el: '.swiper-pagination',
  // },

  // Navigation arrows
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  autoplay: {
    delay: 2000,
  },
  // And if we need scrollbar
  // scrollbar: {
  //   el: '.swiper-scrollbar',
  // },
});
