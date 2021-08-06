$(document).ready(function() {
    $('#catelike_btn').click(function() {
        var categoryIdVar;
        categoryIdVar = $(this).attr('data-categoryid');

        $.get('/rango/like_category/',
            {'category_id': categoryIdVar},
            function(data) {
                $('#catelike_count').html(data);
                // $('#catelike_btn').hide();
            })
    });

    
    $('#like_btn').click(function() {
        var pageIdVar;
        pageIdVar = $(this).attr('data-pageid');

        $.get('/like_page/',
            {'page_id': pageIdVar},
            function(data) {
                $('#like_count').html(data);
                // $('#like_btn').hide();
            })
    });

    $('#dislike_btn').click(function() {
        var pageIdVar;
        pageIdVar = $(this).attr('data-pageid');

        $.get('/dislike_page/',
            {'page_id': pageIdVar},
            function(data) {
                $('#dislike_count').html(data);
                // $('#dislike_btn').hide();
            })
    });

    $('#comment_like_btn').click(function() {
        var commentIdVar;
        commentIdVar = $(this).attr('data-commentid');

        $.get('/comment_like_page/',
            {'comment_id': commentIdVar},
            function(data) {
                $('#comment_like_count').html(data);
                // $('#like_btn').hide();
            })
    });

    $('#comment_dislike_btn').click(function() {
        var commentIdVar;
        commentIdVar = $(this).attr('data-commentid');

        $.get('/comment_dislike_page/',
            {'comment_id': commentIdVar},
            function(data) {
                $('#comment_dislike_count').html(data);
                // $('#dislike_btn').hide();
            })
    });

    

});