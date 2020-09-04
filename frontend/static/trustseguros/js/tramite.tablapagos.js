$(document).ready(function () {

    const calcular_prima_neta = function () {
        let prima = parseFloat($('input[name="subtotal"]').val());
        let descuento = parseFloat($('input[name="descuento"]').val());
        $('input[name="prima_neta"]').val((prima - descuento).toFixed(2))
            .trigger('change')
    };

    const calcular_total = function () {
        let prima_neta = parseFloat($('input[name="prima_neta"]').val());
        let emision = parseFloat($('input[name="emision"]').val());
        let iva = parseFloat($('input[name="iva"]').val());
        let otros = parseFloat($('input[name="otros"]').val());
        $('input[name="total"]').val((prima_neta + emision + iva + otros).toFixed(2)).trigger('change')
    };

    const calcular_comision = function () {
        let prima_neta = parseFloat($('input[name="prima_neta"]').val());
        let per_comision = parseFloat($('input[name="per_comision"]').val());
        $('input[name="amount_comision"]').val(((prima_neta * per_comision) / 100).toFixed(2))
    };

    const calcular_tabla_pagos = function () {
        const form = $('#tramite-form')[0];
        const data = new FormData(form);
        data.append('calcular_tabla_pagos', 'calcular_tabla_pagos');
        $.ajax(".", {
            method: "POST",
            data: data,
            processData: false,
            contentType: false,
            success: function (response) {
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
                                            <input type="text" name="tabla_pagos_monto_comision" class="form-control" value="${o.monto_comision}">
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

    $(document).on('change', 'input[name="subtotal"]', calcular_prima_neta);
    $(document).on('change', 'input[name="descuento"]', calcular_prima_neta);

    $(document).on('change', 'input[name="prima_neta"]', calcular_total);
    $(document).on('change', 'input[name="emision"]', calcular_total);
    $(document).on('change', 'input[name="iva"]', calcular_total);
    $(document).on('change', 'input[name="otros"]', calcular_total);

    $(document).on('change', 'input[name="prima_neta"]', calcular_comision);
    $(document).on('change', 'input[name="per_comision"]', calcular_comision);
    $(document).on('change', 'input[name="per_comision"]', calcular_tabla_pagos);

    $(document).on('change', 'input[name="cuotas"]', calcular_tabla_pagos);
    $(document).on('change', 'input[name="fecha_pago"]', calcular_tabla_pagos);
    $(document).on('change', 'input[name="total"]', calcular_tabla_pagos);

    $(document).on('change', '#id_f_pago', function () {
        if ($(this).val() === "1") {
            $('#id_cuotas').attr('readonly', 'readonly').val('1').trigger('change')
        } else {
            $('#id_cuotas').removeAttr('readonly')
        }
    });


});