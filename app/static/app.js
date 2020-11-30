$(document).ready(function () {

    // Modal about
    let modal = document.getElementById("about");
    let btn = document.getElementById("about_modal");
    let span = document.getElementsByClassName("close")[0];

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
        let x = document.getElementById("sidenav");
        if (x.style.display === "none") {
            x.style.display = "grid";
        } else {
            x.style.display = "none";
        }
    });

    // Main navigation functions
    $('.authorFilter').on('click', function (){
        let author_name = $(this).attr('author_name');

        let getBookByAuthor = $.ajax({
            url: '/filter_book_menu',
            type: 'POST',
            data: {author: author_name}
        });

        getBookByAuthor.done(function (data) {
            $('#book_menu').html(data);
        })
    });
    $('.bookFilter').on('click', function (){

        let book_id = $(this).attr('book_id');

        let getSourceByBook = $.ajax({
            url: '/filter_source',
            type: 'POST',
            data: {book: book_id}
        });

        getSourceByBook.done(function (data) {
            $('#source_text').html(data);
        });

        let getSourceBookName = $.ajax({
            url: '/filter_book_name',
            type: 'POST',
            data: {book: book_id}
        });

        getSourceBookName.done(function (data) {
            $('#sourceBookName').html(data);
        });

        let getAuthors = $.ajax({
            url: '/filter_author_menu',
            type: 'POST',
            data: {book: book_id}
        });

        getAuthors.done(function (data) {
            $('#author_menu').html(data);
        });

        let getChapters = $.ajax({
            url: '/filter_chapter_menu',
            type: 'POST',
            data: {book: book_id}
        });

        getChapters.done(function (data) {
            $('#chapter_menu').html(data);
        });
    });
    $('.verseFilter').on('click', function (){

        let verse_id = $(this).attr('verse_id');

        let getSourceByBook = $.ajax({
            url: '/filter_target',
            type: 'POST',
            data: {id: verse_id}
        });

        getSourceByBook.done(function (data) {
            $('#graph-container').html(data);
        })

    });

    let authorContainer = document.getElementById('author_menu');
    let authorbtns = authorContainer.getElementsByClassName('authorFilter');
    for (let i = 0; i < authorbtns.length; i++){
        authorbtns[i].addEventListener('click',function () {
            let current = document.getElementsByClassName('active');
            if (current.length > 0){
                current[0].className = current[0].className.replace(' active', '');
            }
            this.className += ' active';
        });
    }

    let bookContainer = document.getElementById('book_menu');
    let bookbtns = bookContainer.getElementsByClassName('bookFilter');
    for (let i = 0; i < bookbtns.length; i++){
        bookbtns[i].addEventListener('click',function () {
            let current = document.getElementsByClassName('active');
            if (current.length > 0){
                current[0].className = current[0].className.replace(' active', '');
            }
            this.className += ' active';
        });
    }

    let chapterContainer = document.getElementById('chapter_menu');
    let chapterbtns = chapterContainer.getElementsByClassName('chapterFilter');
    for (let i = 0; i < chapterbtns.length; i++){
        chapterbtns[i].addEventListener('click',function () {
            let current = document.getElementsByClassName('active');
            if (current.length > 0){
                current[0].className = current[0].className.replace(' active', '');
            }
            this.className += ' active';
        });
    }

});