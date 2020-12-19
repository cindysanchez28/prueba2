
function eliminar(){
    swal({
        title: "¿Estas Seguro?",
        text: "Una vez eliminada la imagen no podras recuperarla",
        icon: "warning",
        buttons: true,
        dangerMode: true,
      })
      .then((willDelete) => {
        if (willDelete) {
          $.ajax({
            data:{
                //correo: $('#correo').val(),
                id: idImg
            },
            type: 'POST',
            url: '/deleteImage'
          })
          .done(function(data){
            swal("Tu imagen fue eliminada", {
              icon: "success",
            });
          });
          
          
        } else {
          swal("Tu imagen no se elimino", {
            button : {
                className : "btn-ini"
            }
          });
        }
      });
}

function Storage() {
  console.log("ejecutando la funcion");
  //usuario = document.getElementById("");
}
