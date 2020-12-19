
function eliminar(id){
  idImagen = document.getElementById('eliminarImagenId')
  console.log(idImagen.value);
  console.log(id);
    swal({
        title: "¿Estas Seguro?",
        text: "Una vez eliminada la imagen no podras recuperarla",
        icon: "warning",
        buttons: true,
        dangerMode: true,
      })
      .then((willDelete) => {
        if (willDelete) {
          swal("Tu imagen fue eliminada", {
            icon: "success",
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
