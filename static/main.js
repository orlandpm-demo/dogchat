function enableLikeButtons($target){
    $target.find('.like-button').click(function() {
        var post_id = parseInt($(this).closest('.post-box').attr('data-postid'));
        // alert('like button clicked! post id was ' + post_id);
        var $link = $(this);
        $.ajax({
          url: '/like/' + post_id
        }).done(function(data) {
            var like_info = JSON.parse(data);
            var like_count = like_info['like_count'];
            var action = like_info['action'];
            console.log(like_info);
            console.log(action);
            // console.log($link.find('.like-count'));
            if(action === 'like'){
              $link.find('.fa-heart').removeClass('far');
              $link.find('.fa-heart').addClass('fas');
            }
            else {
              $link.find('.fa-heart').removeClass('fas');
              $link.find('.fa-heart').addClass('far');
            }
            $link.find('.like-count').text(like_count);
        })
        .fail(function() {
          alert( "error" );
        })
      });
}

function enableCommentButtons($target){ 
    $target.find('.comment-button').click(function(){
        var post_id = parseInt($(this).closest('.post-box').attr('data-postid'));
        var $comments = $(this).closest('.post-box').find('.comments');
        $.ajax({
            url: '/api/comments/' + post_id
        }).done(function(data) {
            var comments = JSON.parse(data);
            $comments.html('');
            if(comments.length == 0){
            $comments.append(`<li>No comments yet!</li>`);
            }
            else {
            for (var i = 0; i < comments.length; i++){
                var handle = comments[i]['Handle'];
                var text = comments[i]['Text'];
                $comments.append(`<li><b>${handle}:</b> ${text} </li>`);
            }
            }
            
        })
        .fail(function() {
            alert( "failed to get comments" );
        });
    });
    console.log('comment buttons enabled!')
}

function likeButtonHtml(post){
    var icon_type = post['CurrentDogLike'] ? 'fas' : 'far';

    var html = `<a class="level-item like-button" aria-label="like">
    <span class="icon is-small"><i class="${icon_type} fa-heart" aria-hidden="true"></i>
      <span class="like-count">${ post['LikeCount'] }</span>
    </span>
    </a> `
    return html;
}

function renderPost($target, post){
    var html =  `<div class="box post-box" data-postid="${post['Id']}">
<article class="media">
  <div class="media-left">
    <figure class="image is-64x64">
      <img src="${ post['avatar_url'] }" alt="Image">
    </figure>
  </div>
  <div class="media-content">
    <div class="content">
      <p>
        <a onclick="dogPage('${post['Handle']}')"><strong>${ post['Name'] }</strong></a> <small>@${post['Handle']}</small>
        <br>
        ${ post['Text'] }
        <br>
      </p>
    </div>
    <nav class="level is-mobile">
      <div class="level-left">
        <a class="level-item" aria-label="reply">
          <span class="icon is-small">
            <i class="fas fa-reply" aria-hidden="true"></i>
          </span>
        </a>
        <a class="level-item" aria-label="retweet">
          <span class="icon is-small">
            <i class="fas fa-retweet" aria-hidden="true"></i>
          </span>
        </a>
        <a class="level-item comment-button" aria-label="comment">
          <span class="icon is-small">
            <i class="fas fa-comment" aria-hidden="true"></i>
          </span>
        </a>
        ${likeButtonHtml(post)}
      </div>
    </nav>
  </div>
</article>

<ul class="comments">
</ul>
</div>`

    $target.append(html);
    console.log('post appended')
}


// $.ajax({
//     url: '/api/comments/' + post_id
//   }).done(function(data) {
    
//   })
//   .fail(function() {
//     alert( "failed to get comments" );
//   });


var $main = $('#main');

function clearMain(){
    $main.html('');
}

function feedPage() {
    window.location.hash = 'feed'
    clearMain();
    $main.append(`<h1>Dogchat Feed</h1>`);
    $.ajax({
        url: '/api/feed'
      }).done(function(data) {
        var posts = JSON.parse(data);
        
        // like "for post in posts" in Python
        posts.forEach(function (post){
            renderPost($main, post)
        });
        enableCommentButtons($main);
        enableLikeButtons($main);
      })
      .fail(function() {
        alert( "failed to get feed" );
      });
}

function dogPage(handle) {
    window.location.hash = `dogs/${handle}`
    clearMain();
    $main.append(`<h1>User: @${handle}</h1>`);
    $.ajax({
        url: `/api/dog/${handle}`
      }).done(function(data) {
        $main.append(`<pre>${data}</pre>`)
      })
      .fail(function() {
        alert( "failed to get feed" );
      });
}


/// Instructions when the page loads

$('.my-profile-button').click(function(){
    dogPage('rover');
});

$('.feed-button').click(function(){
    feedPage();
});

console.log(window.location.hash);
if(window.location.hash == '#feed'){
    feedPage();
}
