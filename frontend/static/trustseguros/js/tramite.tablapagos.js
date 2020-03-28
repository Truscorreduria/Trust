$(document).ready(function () {

    const calcular_prima_neta = function () {
        let prima = parseFloat($('#id_subtotal').val());
        let descuento = parseFloat($('#id_descuento').val());
        $('#id_prima_neta').val((prima - descuento).toFixed(2))
            .trigger('change')
    };

    const calcular_total = function () {
        let prima_neta = parseFloat($('#id_prima_neta').val());
        let emision = parseFloat($('#id_emision').val());
        let iva = parseFloat($('#id_iva').val());
        let otros = parseFloat($('#id_otros').val());
        $('#id_total').val((prima_neta + emision + iva + otros).toFixed(2)).trigger('change')
    };

    const calcular_comision = function () {
        let prima_neta = parseFloat($('#id_prima_neta').val());
        let per_comision = parseFloat($('#id_per_comision').val());
        $('#id_amount_comision').val(((prima_neta * per_comision) / 100).toFixed(2))
    };

    const calcular_tabla_pagos = function () {
        $.ajax($ajax_tabla_pagos_tramites, {
            method: "POST",
            data: {
                total: $('#id_total').val(), fecha: $('#id_fecha_pago').val(),
                cuotas: $('#id_cuotas').val(), poliza: $('input[name="id"]').val()
            },
            success: function (response) {
                console.log(response)
                const pagos = $('#id_tabla_pagos tbody').empty();
                $.each(response, function (i, o) {
                    pagos.append(`
                                    <tr>
                                        <td>
                                            <input type="hidden" name="tabla_pagos_id">
                                            <input type="text" name="tabla_pagos_numero" class="form-control" readonly value="${o.numero}">
                                        </td>
                                        <td>
                                            <input type="text" name="tabla_pagos_fecha_vence" class="form-control" readonly value="${o.fecha}">
                                        </td>
                                        <td>
                                            <input type="text" name="tabla_pagos_monto" class="form-control" value="${o.monto}">
                                        </td>
                                        <td>
                                            <input type="text" name="tabla_pagos_estado" class="form-control" readonly value="${o.estado}">
                                        </td>
                                    </tr>
                            `)
                });
                let total_pagos = 0.0;
                $.each($('input[name="tabla_pagos_monto"]'), function (i, o) {
                    total_pagos += parseFloat($(o).val())
                });
                $('#id_total_pagos').val(total_pagos);
            }
        })
    };

    $(document).on('change', 'input[name="tabla_pagos_monto"]', function () {
        let total_pagos = 0.0;
        $.each($('input[name="tabla_pagos_monto"]'), function (i, o) {
            total_pagos += parseFloat($(o).val())
        });
        $('#id_total_pagos').val(total_pagos);
    });

    $(document).on('change', '#id_subtotal', calcular_prima_neta);
    $(document).on('change', '#id_descuento', calcular_prima_neta);

    $(document).on('change', '#id_prima_neta', calcular_total);
    $(document).on('change', '#id_emision', calcular_total);
    $(document).on('change', '#id_iva', calcular_total);
    $(document).on('change', '#id_otros', calcular_total);

    $(document).on('change', '#id_prima_neta', calcular_comision);
    $(document).on('change', '#id_per_comision', calcular_comision);

    $(document).on('change', '#id_cuotas', calcular_tabla_pagos);
    $(document).on('change', '#id_fecha_pago', calcular_tabla_pagos);
    $(document).on('change', '#id_total', calcular_tabla_pagos);

    $(document).on('change', '#id_f_pago', function () {
        if ($(this).val() === "1") {
            $('#id_cuotas').attr('readonly', 'readonly').val('1').trigger('change')
        } else {
            $('#id_cuotas').removeAttr('readonly')
        }
    });


});