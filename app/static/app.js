$(document).ready(function () {

    function getTextColor(rgba) {
        rgba = rgba.match(/\d+/g);
        if ((rgba[0] * 0.299) + (rgba[1] * 0.587) + (rgba[2] * 0.114) > 186) {
            return '#111';
        } else {
            return '#fff';
        }
    }

    $('.menu').on('click', function (){
        const x = document.getElementById("sidenav");
        if (x.style.display === "none") {
            x.style.display = "grid";
        } else {
            x.style.display = "none";
        }
    });
    $('.authorFilter').on('click', function (){
        const author_name = $(this).attr('author_name');

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

        const book_id = $(this).attr('book_id');

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

        const verse_id = $(this).attr('verse_id');

        let getSourceByBook = $.ajax({
            url: '/filter_target',
            type: 'POST',
            data: {Id: verse_id}
        });

        getSourceByBook.done(function (data) {
            $('#graph-container').html(data);
        })

    });

    var authorContainer = document.getElementById('author_menu');
    var authorbtns = authorContainer.getElementsByClassName('authorFilter');
    for (let i = 0; i < authorbtns.length; i++){
        authorbtns[i].addEventListener('click',function () {
            const current = document.getElementsByClassName('active');
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
            const current = document.getElementsByClassName('active');
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
            const current = document.getElementsByClassName('active');
            if (current.length > 0){
                current[0].className = current[0].className.replace(' active', '');
            }
            this.className += ' active';
        });
    }

});