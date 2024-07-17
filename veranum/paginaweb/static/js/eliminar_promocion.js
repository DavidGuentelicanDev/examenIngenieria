$(document).ready(function() {
    $('.btn_eliminarPromocion').click(function(event) {
        event.preventDefault();

        let button = $(this);
        let form = button.closest('.form_eliminarPromocion');
        let url = form.attr('action');
        let csrfToken = form.find('input[name="csrfmiddlewaretoken"]').val();

        Swal.fire({
            title: 'Eliminar promoción',
            text: "¿Estás seguro/a de eliminar esta promoción? No podrás revertirlo.",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Eliminar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    type: 'POST',
                    url: url,
                    headers: {'X-CSRFToken': csrfToken},  // Envía el token CSRF en los headers
                    data: {'csrfmiddlewaretoken': csrfToken},
                    success: function(response) {
                        console.log(response);
                        if (response.success) {
                            Swal.fire({
                                title: 'Promoción eliminada',
                                text: 'La promoción ha sido eliminada exitosamente.',
                                icon: 'success',
                                confirmButtonText: 'OK'
                            }).then((result) => {
                                if (result.isConfirmed) {
                                    window.location.href = '/portal_admin/';
                                }
                            });
                        } else {
                            Swal.fire({
                                title: 'Error',
                                text: response.message || 'Hubo un problema al eliminar la promoción.',
                                icon: 'error',
                                confirmButtonText: 'OK'
                            });
                        }
                    },
                    error: function(xhr, status, error) {
                        Swal.fire({
                            title: 'Error',
                            text: 'Ocurrió un error al procesar la solicitud.',
                            icon: 'error',
                            confirmButtonText: 'OK'
                        });
                    }
                });
            }
        });
    });
});