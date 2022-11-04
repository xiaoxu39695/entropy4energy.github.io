(() => {
  function automaticSlideShow() {
    // Checked: play
    if (document.getElementById('slideshow_main_play').checked) {
      const slides = document.querySelectorAll('#slideshow_main input[type=radio]');
      for (let i = 0; i < slides.length; i++) {
        if (slides[i].checked) {
          if (i === slides.length - 1) {
            slides[0].checked = true;
          } else {
            slides[i + 1].checked = true;
          }
          break;
        }
      }
    }
    setTimeout(automaticSlideShow, 7000);
  }

  setTimeout(automaticSlideShow, 7000);
})();
