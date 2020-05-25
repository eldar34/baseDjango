function activateUser(msg){

    $.ajax({
        type: 'POST',
        url: url,
        data: msg,

        success: function (data) {            
            
            $('#regSuccess').text(
                "User activated"
            );
            $('#regSuccess').css("display", "block");
            setTimeout(function () {
                $('#regSuccess').fadeOut('slow');
            }, 3000);
        },
        error: function (xhr, str) {
            $('#regSuccess').removeClass('alert-success');
            $('#regSuccess').addClass('alert-danger');

            $('#regSuccess').text(
                "Activation error"
            );
            $('#regSuccess').css("display", "block");
            setTimeout(function () {
                $('#regSuccess').fadeOut('slow');
            }, 3000);
            // alert('Возникла ошибка: ' + xhr.responseCode);
        }
    });
}
        

