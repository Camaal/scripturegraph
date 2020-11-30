$(document).ready(function () {

    // Modal about
    var modal = document.getElementById("about");
    var btn = document.getElementById("about_modal");
    var span = document.getElementsByClassName("close")[0];

    btn.onclick = function() {
      modal.style.display = "block";
    }

    span.onclick = function() {
      modal.style.display = "none";
    }

    window.onclick = function(event) {
      if (event.target == modal) {
        modal.style.display = "none";
      }
    }

    // Hide/Show sidenav
    $('.menu').on('click', function (){
        var x = document.getElementById("sidenav");
        if (x.style.display === "none") {
            x.style.display = "grid";
        } else {
            x.style.display = "none";
        }
    });

    // Main navigation functions
    $('.authorFilter').on('click', function (){
        var author_name = $(this).attr('author_name');

        var getBookByAuthor = $.ajax({
            url: '/filter_book_menu',
            type: 'POST',
            data: {author: author_name}
        });

        getBookByAuthor.done(function (data) {
            $('#book_menu').html(data);
        })
    });
    $('.bookFilter').on('click', function (){

        var book_id = $(this).attr('book_id');

        var getSourceByBook = $.ajax({
            url: '/filter_source',
            type: 'POST',
            data: {book: book_id}
        });

        getSourceByBook.done(function (data) {
            $('#source_text').html(data);
        });

        var getSourceBookName = $.ajax({
            url: '/filter_book_name',
            type: 'POST',
            data: {book: book_id}
        });

        getSourceBookName.done(function (data) {
            $('#sourceBookName').html(data);
        });

        var getAuthors = $.ajax({
            url: '/filter_author_menu',
            type: 'POST',
            data: {book: book_id}
        });

        getAuthors.done(function (data) {
            $('#author_menu').html(data);
        });

        var getChapters = $.ajax({
            url: '/filter_chapter_menu',
            type: 'POST',
            data: {book: book_id}
        });

        getChapters.done(function (data) {
            $('#chapter_menu').html(data);
        });
    });
    $('.verseFilter').on('click', function (){

        var verse_id = $(this).attr('verse_id');

        var getSourceByBook = $.ajax({
            url: '/filter_target',
            type: 'POST',
            data: {id: verse_id}
        });

        getSourceByBook.done(function (data) {
            $('#graph-container').html(data);
        })

    });

    var authorContainer = document.getElementById('author_menu');
    var authorbtns = authorContainer.getElementsByClassName('authorFilter');
    for (let i = 0; i < authorbtns.length; i++){
        authorbtns[i].addEventListener('click',function () {
            var current = document.getElementsByClassName('active');
            if (current.length > 0){
                current[0].className = current[0].className.replace(' active', '');
            }
            this.className += ' active';
        });
    }

    var bookContainer = document.getElementById('book_menu');
    var bookbtns = bookContainer.getElementsByClassName('bookFilter');
    for (let i = 0; i < bookbtns.length; i++){
        bookbtns[i].addEventListener('click',function () {
            var current = document.getElementsByClassName('active');
            if (current.length > 0){
                current[0].className = current[0].className.replace(' active', '');
            }
            this.className += ' active';
        });
    }

    var chapterContainer = document.getElementById('chapter_menu');
    var chapterbtns = chapterContainer.getElementsByClassName('chapterFilter');
    for (let i = 0; i < chapterbtns.length; i++){
        chapterbtns[i].addEventListener('click',function () {
            var current = document.getElementsByClassName('active');
            if (current.length > 0){
                current[0].className = current[0].className.replace(' active', '');
            }
            this.className += ' active';
        });
    }

});