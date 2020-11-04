$(function(){
    $('.like-toggle').click(function(){
      $(this).toggleClass('like-active');
      $(this).next().toggleClass('hidden');
    });
  });