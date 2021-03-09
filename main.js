function removeBanner(){
    var banner = document.getElementById('new-user-banner');
    console.log('hello!');
    console.log(banner);
    banner.remove();
}

function selectTab(tabName){
    $('.tab-content').hide();
    var id = "#" + tabName;
    console.log(id);
    $(id).show();
    $('.tab.' + tabName).siblings().removeClass('is-active');
    $('.tab.' + tabName).addClass('is-active');
}

$('#square-root-input').on('input',
    function(){
        var $input = $('#square-root-input');
        var $answer = $('#square-root-answer');
        var x = $input.val();
        var number = parseFloat(x);
        $input.removeClass('is-success');
        $input.removeClass('is-danger');
        if(isNaN(number)){
            $answer.text("You must input a number!");
            $input.addClass('is-danger');
        }
        else if(number < 0){
            $answer.text("Number must be positive");
            $input.addClass('is-danger');
        }
        else{
            var result = Math.sqrt(number);
            $answer.text(result);
            $input.addClass('is-success');
        }
    }
)

// $('#square-root-button').click(
//     function(){
//         var x = $('#square-root-input').val();
//         var result = Math.sqrt(parseFloat(x));
//         $('#square-root-answer').text(result);
//     }
// )