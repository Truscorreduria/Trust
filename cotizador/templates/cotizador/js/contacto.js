{% load static %}


$(document).ready(function () {
    $('#button-ticket').on('click', function () {
        $('#modal-ticket').modal('show');
    });

    const mostrar_formato = function () {
        if ($('#movimiento').val() === '5') {
            if ($('#referente').val() === 'auto') {
                $('#row-poliza').css('display', 'flex');
                $('#row-auto').css('display', 'flex');
                $('#row-sepelio').css('display', 'none');
                $('#row-accidente').css('display', 'none');
            } else if ($('#referente').val() === 'sepelio') {
                $('#row-poliza').css('display', 'none');
                $('#row-auto').css('display', 'none');
                $('#row-sepelio').css('display', 'flex');
                $('#row-accidente').css('display', 'none');
            } else if ($('#referente').val() === 'accidente') {
                $('#row-poliza').css('display', 'none');
                $('#row-auto').css('display', 'none');
                $('#row-sepelio').css('display', 'none');
                $('#row-accidente').css('display', 'flex');
            }
        } else {
            if ($('#referente').val() === 'auto') {
                $('#row-poliza').css('display', 'flex');
            } else{
                $('#row-poliza').css('display', 'none');
            }

            $('#row-auto').css('display', 'none');
            $('#row-sepelio').css('display', 'none');
            $('#row-accidente').css('display', 'none');

            if ($('#movimiento').val() === '2') {
                $('#row-motivo').css('display', 'flex')
            } else{
                $('#row-motivo').css('display', 'none')
            }

        }

    };

    $('#referente').on('change', mostrar_formato);

    $('#movimiento').on('change', mostrar_formato);

    function aperturar_reclamo() {
        const hash = window.location.hash;
        if (hash == '#reclamovida') {
            $('#referente').val('vida').trigger('change');
            $('#movimiento').val('5').trigger('change');
            $('#modal-ticket').modal('show');
        }

        if (hash == '#reclamoaccidente') {
            $('#referente').val('accidente').trigger('change');
            $('#movimiento').val('5').trigger('change');
            $('#modal-ticket').modal('show');
        }

        if (hash == '#reclamosepelio') {
            $('#referente').val('sepelio').trigger('change');
            $('#movimiento').val('5').trigger('change');
            $('#modal-ticket').modal('show');
        }

        if (hash == '#reclamoauto') {
            $('#referente').val('auto').trigger('change');
            $('#movimiento').val('5').trigger('change');
            $('#modal-ticket').modal('show');
        }
    }

    aperturar_reclamo();

    $('.contacto-directo').on('click', function () {
        $('#contacto-ticket').val($(this).data('ticket'));
        $('#modal-contacto-directo').modal('show');
    });

    const enviar_contacto = function () {
        $.ajax("{% url 'cotizador:enviar_contacto' %}", {
            method: "POST",
            data: {
                ticket: $('#contacto-ticket').val(),
                comentarios: $('#comentarios-contacto-directo').val()
            },
            success: function (response) {
                location.reload()
            }
        })
    };

    $('#contacto-directo-form').on('submit', enviar_contacto);
    
    
    $('#ticket-form').on('submit', function (e) {
        e.preventDefault();
        let data = new FormData(this);
        $.ajax('.', {
            method: "POST",
            data: data,
            processData:false,
            contentType: false,
            success: function (response) {
                $('#modal-ticket').modal('hide');
                swal({
                    title: 'Ticket recibido',
                    text: 'Tu ticket se ha ingresado con éxito, recibiras atención en un máximo de 24 horas. Muchas gracias',
                    imageUrl: "{% static 'cotizador/images/trusty/gracias.png' %}"
                }).then(function () {
                    location.reload();
                })
            }
        })
    })
});