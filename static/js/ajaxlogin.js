$(document).ready(function(){
    $('#formlogin').on('submit',function(event){
        $.ajax({
                data:{
                    correo: $('#correo').val(),
                    contraseña: $('#contraseña').val()
            },
            type: 'POST',
            url: '/login'
        })
        .done(function(data){
            if(data.error){
                $('#error').html(`<div class="alert alert-danger" id="borrar" role="alert">
                Contraseña o usuario incorrecto
              </div>`);
               // $('#error').text("Contraseña o usuario incorrecto").show();
                //$('#error').css("background-color", "rgba(255, 18, 18, 0.5)");
               // $('#error').css("padding", "10px");
                //$('#error').css("margin", "15px");
              //  $('#error').css("border-radius", "5px");
                //$('#error').css("transition", "all 500ms ease");
                $('.alert').css("transition", "all 500ms ease");
               
            }
            else{
                $(location).attr('href', '/dashboard')
            }
        });
        event.preventDefault();
    });
});

$(document).ready(function() {
    $("#borrar").click(function(event) {
        $("#error").remove();
    });
});