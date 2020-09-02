$(document).ready(function () {

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

        let getChapterByAuthor = $.ajax({
            url: '/filter_chapter_menu',
            type: 'POST',
            data: {author: author_name}
        });

        getChapterByAuthor.done(function (data) {
            $('#chapter_menu').html(data);
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
        })

        let getAuthors = $.ajax({
            url: '/filter_author_menu',
            type: 'POST',
            data: {book: book_id}
        });

        getAuthors.done(function (data) {
            $('#author_menu').html(data);
        })
    });

    $('.verseFilter').on('click', function (){
        const verse_id = $(this).attr('verse_id');

        let getSourceByBook = $.ajax({
            url: '/filter_target',
            type: 'POST',
            data: {Id: verse_id}
        });

        getSourceByBook.done(function (data) {
            $('#target_text').html(data);
        })
    });

});