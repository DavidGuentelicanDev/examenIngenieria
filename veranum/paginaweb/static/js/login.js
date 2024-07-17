$(document).ready(function() {
    $('#btn_login').click(function(event) {
        event.preventDefault();

        let usuario = $('#txt_usuario').val().trim();
        let clave = $('#txt_clave').val().trim();
        let url = '/login_admin/';

        if (usuario === '' || clave === '') {
            Swal.fire({
                title: 'Campos obligatorios',
                text: 'Debes indicar un usuario y una clave válidos para iniciar sesión.',
                icon: 'warning',
                confirmButtonText: 'OK'
            });
            return;
        }

        $.ajax({
            type: 'POST',
            url: url,
            data: {
                usuario: usuario,
                clave: clave,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            dataType: 'json',
            success: function(response) {
                console.log(response);
                if (response.success) {
                    let redirectUrl = '/';
                    if (response.rol === 'M') {
                        redirectUrl = '/portal_admin/';
                    } else if (response.rol === 'G') {
                        redirectUrl = '/portal_admin/';
                    }
                    Swal.fire({
                        title: 'Éxito',
                        text: response.message + ' Redirigiendo a la página inicial...',
                        icon: 'success',
                        timer: 1000,
                        showConfirmButton: false,
                        didOpen: () => {
                            Swal.showLoading();
                        },
                        willClose: () => {
                            window.location.href = redirectUrl;
                        }
                    });
                } else {
                    Swal.fire({
                        title: 'Error',
                        text: response.message,
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
    });
});