$(document).ready(function() {
    //aprobar
    $('.btn_aprobar').click(function(event) {
        event.preventDefault();

        let $form = $(this).closest('form');
        let actionUrl = $form.attr('action');
        let formData = $form.serialize() + '&aprobar=aprobar';

        Swal.fire({
            title: "Aprobar promoción",
            text: "¿Deseas aprobar esta promoción? Esta acción no se puede cambiar.",
            icon: "warning",
            showCancelButton: true,
            confirmButtonText: 'Aprobar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    type: 'POST',
                    url: actionUrl,
                    data: formData,
                    success: function(response) {
                        console.log(response);
                        if (response.success) {
                            Swal.fire({
                                title: 'Promoción aprobada',
                                text: 'La promoción ha sido aprobada exitosamente.',
                                icon: 'success',
                                confirmButtonText: 'OK'
                            }).then((result) => {
                                if (result.isConfirmed) {
                                    window.location.href = '/portal_admin/';
                                }
                            })
                        } else {
                            Swal.fire({
                                title: 'Error',
                                text: response.message || 'Hubo un problema al aprobar la promoción.',
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

    //rechazar
    $('.btn_rechazar').click(function(event) {
        event.preventDefault();

        let $form = $(this).closest('form');
        let actionUrl = $form.attr('action');
        let formData = $form.serialize() + '&rechazar=rechazar';

        Swal.fire({
            title: "Rechazar promoción",
            text: "¿Deseas rechazar esta promoción? Esta acción no se puede cambiar.",
            icon: "warning",
            showCancelButton: true,
            confirmButtonText: 'Rechazar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    type: 'POST',
                    url: actionUrl,
                    data: formData,
                    success: function(response) {
                        console.log(response);
                        if (response.success) {
                            Swal.fire({
                                title: 'Promoción rechazada',
                                text: 'La promoción ha sido rechazada.',
                                icon: 'success',
                                confirmButtonText: 'OK'
                            }).then((result) => {
                                if (result.isConfirmed) {
                                    window.location.href = '/portal_admin/';
                                }
                            })
                        } else {
                            Swal.fire({
                                title: 'Error',
                                text: response.message || 'Hubo un problema al rechazar la promoción.',
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