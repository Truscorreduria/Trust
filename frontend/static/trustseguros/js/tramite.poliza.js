$(document).ready(function () {
    $(document).on('change', '#id_cliente', function () {
        const _this = $(this);
        $.ajax('.', {
            method: "POST",
            data: {cliente: _this.val(), polizas: 'polizas'},
            success: function (response) {
                const $poliza = $('#id_poliza').empty();
                $poliza.append(`<option value="" selected="">---------</option>`);
                $.each(response.collection, function (i, o) {
                    $poliza.append(`<option value="${o.id}">${o.no_poliza}</option>`)
                })
            }
        })
    });
    $(document).on('change', '#id_poliza', function () {
        const _this = $(this);
        $.ajax('.', {
            method: "POST",
            data: {pk: _this.val(), contactos: 'contactos'},
            success: function (response) {
                const $contacto = $('#id_contacto_aseguradora').empty();
                $contacto.append(`<option value="" selected="">---------</option>`);
                $.each(response.collection, function (i, o) {
                    $contacto.append(`<option value="${o.id}">${o.name}</option>`)
                });
                $('#id_ramo').val(response.instance.ramo.name);
                $('#id_sub_ramo').val(response.instance.sub_ramo.name);
                $('#id_grupo').val(response.instance.grupo.name);
                $('#id_aseguradora').val(response.instance.aseguradora.name);
            }
        })
    });
});