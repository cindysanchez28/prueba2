$(document).ready(function(){
    $('#formregistro').on('submit',function(event){
        $.ajax({
                data:{
                    nombre: $('#nombrer').val(),
                    apellido: $('#apellidor').val(),
                    nombreUsuario: $('#usuarior').val(),
                    correo: $('#correor').val(),
                    fecha: $('#fechar').val(),
                    contraseña: $('#contraseñar').val() 
            },
            type: 'POST',
            url: '/crearusuario'
        })
        .done(function(data){
            if(data.error == "1"){
                $('#errorRegistro').html(`<div class="alert alert-danger" id="borrar" role="alert">
                El correo ya se encuentra registrado
                </div>`);
                $('#correor').val("");
            }
            else if(data.error == "2"){
                $('#errorRegistro').html(`<div class="alert alert-danger" id="borrar" role="alert">
                El nombre de usario ya se encuentra en uso
                </div>`);
                $('#usuarior').val("");
                
            }
            else if(data.error == "3"){
                $('#errorRegistro').html(`<div class="alert alert-danger" id="borrar" role="alert">
                El nombre de usario no tiene formato valido
                </div>`);
                $('#nombrer').val("");  
            }
            else if(data.error == "4"){
                $('#errorRegistro').html(`<div class="alert alert-danger" id="borrar" role="alert">
                El apellido no tiene formato valido
                </div>`);
                $('#apellidor').val("");  
            }
            else if(data.error == "5"){
                $('#errorRegistro').html(`<div class="alert alert-danger" id="borrar" role="alert">
                El nickname no tiene formato valido
                </div>`);
                $('#usuarior').val("");  
            }
            else if(data.error == "7"){
                $('#errorRegistro').html(`<div class="alert alert-danger" id="borrar" role="alert">
                La contraseña no tiene un formato valido
                </div>`);
                $('#contraseñar').val("");  
            }
            else if(data.error == "8"){
                $('#errorRegistro').html(`<div class="alert alert-danger" id="borrar" role="alert">
                la fecha no tiene un formato valido
                </div>`);
                $('#fechar').val("");  
            }
            
            else{
              
                $('#nombrer').val("");
                $('#apellidor').val("");
                $('#correor').val("");
                $('#usuarior').val("");
                $('#fechar').val("");
                $('#contraseñar').val("");
                swal("Exito", "Registrado Correctamente, revisa tu correo electronico", "success",{
                    button : false
                  });
            }
        });
        event.preventDefault();
    });
});
$(document).ready(function() {
    
    $('#BtnRegistro').click(function(event){
        console.log("elimino")
        $('#nombrer').val("");
                $('#apellidor').val("");
                $('#correor').val("");
                $('#usuarior').val("");
                $('#fechar').val("");
                $('#contraseñar').val("");
                $('#errorRegistro').html(``);
                $('#error').html(``);
                
    });

    
});