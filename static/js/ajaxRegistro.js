$(document).ready(function(){
    $('#formregistro').on('submit',function(event){
        $.ajax({
                data:{
                    nombre: $('#nombrer').val(),
                    apellido: $('#apellidor').val(),
                    correo: $('#correor').val(),
                    nombreUsuario: $('#nombreUsuario').val(),
                    fecha: $('#fechar').val(),
                    contraseña: $('#contraseñar').val()
            },
            type: 'POST',
            url: '/crearusuario'
        })
        .done(function(data){
            if(data.error){
                $('#errorRegistro').html(`<div class="alert alert-danger" id="borrar" role="alert">
                Usuario ya existe
              </div>`);
                
            }
            else{
                $('#errorRegistro').html(`<div class="alert alert-danger" id="borrar" role="alert">
                Usuario registrado
              </div>`);
            }
        });
        event.preventDefault();
    });
});