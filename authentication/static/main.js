$(document).ready(function(){
    $(".post-like").click(function(event){
        event.preventDefault();
        let span = $(this);
        let href = span.parent().attr('href');
        let like_id = href.split('=');
        like_id = like_id[like_id.length - 1];
        let split_id = like_id.split('_');
        const text = split_id[0];
        if (text === 'like'){
            let type = 1;
        } else {
            let type = -1;
        }
        const blogpost_id = split_id[2];
        $.ajax({
           url: span.parent().attr('href'),
            success: function(){
                let cur_likes = $('#'+toString(blogpost_id)).text();
                cur_likes = parseInt(cur_likes) + type;
                $("#" +toString(blogpost_id)).html(cur_likes);
            },
            error: function(response, error){
            }

        })
    });

});