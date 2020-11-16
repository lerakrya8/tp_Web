$(".like-button").click(function () {
  $(this)
    .parent()
    .find(".like-button")
    .not(this)
    .removeClass("like-button--active");
  $(this).toggleClass("like-button--active");
});