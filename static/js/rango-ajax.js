$(document).ready(function() {
    $('#catelike_btn').click(function() {
        var categoryIdVar;
        categoryIdVar = $(this).attr('data-categoryid');

        $.get('/rango/like_category/',
            {'category_id': categoryIdVar},
            function(data) {
                $('#catelike_count').html(data);
                $('#catelike_btn').hide();
            })
    });

    
    $('#like_btn').click(function() {
        var pageIdVar;
        pageIdVar = $(this).attr('data-pageid');

        $.get('/rango/like_page/',
            {'page_id': pageIdVar},
            function(data) {
                $('#like_count').html(data);
                $('#like_btn').hide();
            })
    });

    // $('#dislike_btn').click(function() {
    //     var pageIdVar;
    //     pageIdVar = $(this).attr('data-pageid');

    //     $.get('/rango/dislike_page/',
    //         {'page_id': pageIdVar},
    //         function(data) {
    //             $('#dislike_count').html(data);
    //             $('#dislike_btn').hide();
    //         })
    // });

    

});