$(document).ready(function () {
    $(document).on('click', '.btn-clear', function () {
        console.log(this)
        $('#id_siniestro_tramite-tramite_siniestro').val('');
        $('#id_siniestro_tramite-monto_reclamo').val('');
        $('#id_siniestro_tramite-deducible').val('');
        $('#id_siniestro_tramite-coaseguro').val('');
        $('#id_siniestro_tramite-gastos_presentados').val('');
        $('#id_siniestro_tramite-no_cubierto').val('');
        $('#id_siniestro_tramite-monto_pago').val('');
        $('#id_siniestro_tramite-diagnostico').val('');
        $('#id_siniestro_tramite-forma_pago').val('');
    });

    $(document).on('change', '#id_tramites_siniestro', function () {
        const _this = $(this);
        $.ajax('/trustseguros/siniestros/', {
            method: "POST",
            data: {
                load_tramite: 'load_tramite',
                id: $('input[name="id"]').val(),
                tramite: _this.val(),
            },
            success: function (response, txtStatus, xhr) {
                process_response(response, txtStatus, xhr);
            }
        })
    })
});

