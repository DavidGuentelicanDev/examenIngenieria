$(document).ready(function() {
    $('#btn_editarPromocion').click(function(event) {
        event.preventDefault();

        let form = $('#form_editarPromocion');
        let formData = new FormData(form[0]);

        let hotel = formData.get('hotel');
        let tipoHabitacion = formData.get('tipo_habitacion');
        let codigo = formData.get('codigo_promocion');
        let nombre = formData.get('nombre_promocion');
        let fechaInicio = formData.get('fecha_inicio');
        let fechaFin = formData.get('fecha_fin');
        let porcDscto = formData.get('porc_descuento');

        if (!hotel || !tipoHabitacion || !codigo || !nombre || !fechaInicio || !fechaFin || !porcDscto) {
            Swal.fire({
                title: 'Campos vacíos',
                text: 'Por favor, completa todos los campos obligatorios.',
                icon: 'warning',
                confirmButtonText: 'OK'
            });
            return;
        }

        $.ajax({
            type: 'POST',
            url: form.attr('action'),
            data: formData,
            processData: false,
            contentType: false,
            headers: {'X-CSRFToken': form.find('input[name="csrfmiddlewaretoken"]').val()},
            success: function(response) {
                console.log(response);
                if (response.success) {
                    Swal.fire({
                        title: 'Promoción actualizada',
                        text: response.message,
                        icon: 'success',
                        confirmButtonText: 'OK'
                    }).then((result) => {
                        if (result.isConfirmed) {
                            window.location.href = '/portal_admin/';
                        }
                    });
                } else {
                    let errors = JSON.parse(response.errors);
                    let errorMessage = '';
                    for (let field in errors) {
                        if (errors.hasOwnProperty(field)) {
                            errorMessage += errors[field][0].message + '\n';
                        }
                    }
                    Swal.fire({
                        title: 'Error',
                        text: errorMessage,
                        icon: 'error',
                        confirmButtonText: 'OK'
                    });
                }
            },
            error: function(response) {
                console.log(response);
                Swal.fire({
                    title: 'Error',
                    text: 'Hubo un problema al procesar la solicitud. Por favor, intenta nuevamente.',
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
            }
        });
    });
});