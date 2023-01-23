$(document).ready(function(){

    $.ajax({
        type: 'GET',
        url: 'user/reset-limit',
        success: function(data){
            console.log(data.result)
        }
    });
})