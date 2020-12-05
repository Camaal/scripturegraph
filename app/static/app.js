$(document).ready(function () {

    // Modal about
    const modal = document.getElementById("about");
    const btn = document.getElementById("about_modal");
    const span = document.getElementsByClassName("close")[0];

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
        const author_name = $(this).attr('author_name');

        const getBookByAuthor = $.ajax({
            url: '/filter_book_menu',
            type: 'POST',
            data: {author: author_name}
        });

        getBookByAuthor.done(function (data) {
            $('#book_menu').html(data);
        })
    });
    $('.bookFilter').on('click', function (){

        const book_id = parseInt($(this).attr('book_id'));
        const chapter_id = 1

        const getSourceByBook = $.ajax({
            url: '/filter_source',
            type: 'POST',
            data: {book: book_id, chapter: chapter_id}
        });

        getSourceByBook.done(function (data) {
            $('#source_text').html(data);
        });

        const getSourceBookName = $.ajax({
            url: '/filter_book_name',
            type: 'POST',
            data: {book: book_id}
        });

        getSourceBookName.done(function (data) {
            $('#sourceBookName').html(data);
        });

        const getAuthors = $.ajax({
            url: '/filter_author_menu',
            type: 'POST',
            data: {book: book_id}
        });

        getAuthors.done(function (data) {
            $('#author_menu').html(data);
        });

        const getChapters = $.ajax({
            url: '/filter_chapter_menu',
            type: 'POST',
            data: {book: book_id}
        });

        getChapters.done(function (data) {
            $('#chapter_menu').html(data);
        });
    });

    $('.verseFilter').on('click', function (){

        const verse_id = parseInt($(this).attr('verse_id'));

        const getSourceByBook = $.ajax({
            url: '/filter_target',
            type: 'POST',
            data: {id: verse_id}
        });

        getSourceByBook.done(function (data) {
            $('#graph-container').html(data);
        })

    });

    $('.chapterFilter').on('click', function (){

        const book_id = parseInt($(this).attr('book_id'));
        const chapter_id = parseInt($(this).attr('chapter_id'));

        const getSourceByBook = $.ajax({
            url: '/filter_source',
            type: 'POST',
            data: {book: book_id, chapter: chapter_id}
        });

        getSourceByBook.done(function (data) {
            $('#source_text').html(data);
        });
    });

    const authorContainer = document.getElementById('author_menu');
    const authorbtns = authorContainer.getElementsByClassName('authorFilter');
    for (let i = 0; i < authorbtns.length; i++){
        authorbtns[i].addEventListener('click',function () {
            var current = document.getElementsByClassName('active');
            if (current.length > 0){
                current[0].className = current[0].className.replace(' active', '');
            }
            this.className += ' active';
        });
    }

    const bookContainer = document.getElementById('book_menu');
    const bookbtns = bookContainer.getElementsByClassName('bookFilter');
    for (let i = 0; i < bookbtns.length; i++){
        bookbtns[i].addEventListener('click',function () {
            var current = document.getElementsByClassName('active');
            if (current.length > 0){
                current[0].className = current[0].className.replace(' active', '');
            }
            this.className += ' active';
        });
    }

    const chapterContainer = document.getElementById('chapter_menu');
    const chapterbtns = chapterContainer.getElementsByClassName('chapterFilter');
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