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



    
var btnLen = $("#myul").children(".like").length;
console.log("btnLen:" + btnLen)
for(var i = 0; i < btnLen; i++){
    console.log("i:"+i);
    $("#myul").children(".like").eq(i).click(function() {
        console.log("click")
        var commentIdVar;
        commentIdVar = $(this).attr('data-commentid');
        var ii = i;
        $.get('/comment_like_page/',
            {'comment_id': commentIdVar},
            function(data) {
                console.log("likedata:"+data);
                console.log("i:"+i);
                console.log("ii:"+ii);
                console.log("len1:"+$("#myul").children(".count").length)
                console.log("len2:"+$("#myul").children(".count").eq(i).length)
                console.log("len2:"+$("#myul").children(".count").eq(ii).length)
                console.log("len3:"+$("#myul").children(".count").eq(i)
                    .find(".like_count").length)
                console.log("len3:"+$("#myul").children(".count").eq(ii)
                    .find(".like_count").length)
                $("#myul").children(".count").eq(ii)
                    .find(".like_count").eq(0).html(data);
                // $('#like_btn').hide();
                window.location.reload()
            })
    });

    $("#myul").children(".dislike").eq(i).click(function() {
        var commentIdVar;
        commentIdVar = $(this).attr('data-commentid');

        $.get('/comment_dislike_page/',
            {'comment_id': commentIdVar},
            function(data) {
                console.log("dislikedata:"+data);
                $("#myul").children(".count").eq(i)
                    .children(".dislike_count").eq(0).html(data);
                // $('#dislike_btn').hide();
                window.location.reload()
            })
    });
}
    

});
