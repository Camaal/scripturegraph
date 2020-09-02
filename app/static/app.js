$(document).ready(function () {

    $('.filterBook').on('click', function (){
        const author_name = $(this).attr('author_name');

        let req = $.ajax({
            url: '/filter_book_menu',
            type: 'POST',
            data: {author: author_name}
        });
        
        req.done(function (data) {
            $('#book_menu').html(data);
        })

    });

});