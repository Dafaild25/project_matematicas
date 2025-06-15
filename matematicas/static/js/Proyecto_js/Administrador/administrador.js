$(document).ready(function () {
        $('#tbl-admin').DataTable({
          language: {
              search: "Buscar:",
              lengthMenu: "Mostrar _MENU_ registros",
              info: "Mostrando del _START_ al _END_ de _TOTAL_ registros",
              paginate: {
                  first: "Primero",
                  last: "Último",
                  next: "Siguiente",
                  previous: "Anterior"
              }
          }
          
      });
    
       
      });