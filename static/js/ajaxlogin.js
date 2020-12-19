$(document).ready(function(){
    $('#formlogin').on('submit',function(event){
        $('#error').text("").show();
        $('#error').css("transition", "all 500ms ease");
        $.ajax({
                data:{
                    correo: $('#correo').val(),
                    contraseña: $('#contraseña').val()
            },
            type: 'POST',
            url: '/login'
        })
        .done(function(data){
            if(data.error ==  "1"){

                $('#error').html(`<div class="alert alert-danger" id="borrar" role="alert">
                Correo no registrado
                </div>`);
                $('#contraseña').val("")
                $('#correo').val("")
                
               
            }
            else if(data.error == "2"){

                $('#error').html(`<div class="alert alert-danger" id="borrar" role="alert">
                Contraseña incorrecta
                </div>`);
                $('#contraseña').val("")
                
                
            }
            else if(data.error == "3"){

                $('#error').html(`<div class="alert alert-danger" id="borrar" role="alert">
                Usuario no activo
                </div>`);
                $('#contraseña').val("")
                $('#correo').val("")
                
                
            }
            else if(data.error == "4"){

                $('#error').html(`<div class="alert alert-danger" id="borrar" role="alert">
                Correo invalido
                </div>`);
                $('#contraseña').val("")
                $('#correo').val("")
                
                
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

$(document).ready(function() {
    
    $('#BtnIniciar').click(function(event){
        $('#correo').val(""),
        $('#contraseña').val("")
        $('#error').html(``);
        $('#errorRegistro').html(``);
    });
});