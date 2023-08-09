$(document).ready(function() {
  $('.book').on('click', function() {
    var title = $(this).find('.book-title').text();
    var imgSrc = $(this).find('.book-img').attr('src');
    var author = $(this).find('.book-author').text();
    var publisher = $(this).find('.book-publisher').text();
    var publishedDate = $(this).find('.book-publishedDate').text();
    var pageCount = $(this).find('.book-pageCount').text();
    var description = $(this).find('.book-description').text();

    $("#show-book-title").text(title);
    $("#show-book-img").attr("src", imgSrc);
    $("#show-book-author").text("著者: " + author);
    $("#show-book-publisher").text("出版社: " + publisher);
    $("#show-book-publishedDate").text("出版日: " + publishedDate);
    $("#show-book-pageCount").text("ページ数: " + pageCount);
    $("#show-book-description").text(description);

    $('#overlay').fadeIn();
  });

  $('#closeOverlay').on('click', function() {
      $('#overlay').fadeOut();
  });
});