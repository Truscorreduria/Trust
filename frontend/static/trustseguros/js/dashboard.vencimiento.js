$(document).ready(function () {


    const modal = $('#dashboard-modal').iziModal({
        width: 1200, padding: 20, fullscreen: false, zindex: 1500,
        headerColor: '#326634'
    });

    function fix_date(obj) {
        obj['fecha_emision'] = new Date(obj.fecha_vence);
        obj['fecha_vence'] = new Date(obj.fecha_vence);
        return obj;
    }

    const show_data = function () {
        const data = $(this).data();
        console.log(data)
        const content = modal.find('.modal-body');

        let html = ` <table class="table">
                        <thead>
                            <tr>
                                <td>Número de Póliza</td>
                                <td>Fecha de emisión</td>
                                <td>Fecha de vencimiento</td>
                                <td class="numberinput">Prima</td>
                                <td class="numberinput">Comisión</td>
                            </tr>
                        </thead>
                        <tbody>
                            ${Object.keys(data).map(row => `<tr>
                                <td>${data[row].no_poliza}</td>
                                <td>${data[row].fecha_emision.toLocaleString('es-NI').slice(0, 10)}</td>
                                <td>${data[row].fecha_vence.toLocaleString('es-NI').slice(0, 10)}</td>
                                <td class="numberinput">${intcommas(data[row].prima)}</td>
                                <td class="numberinput">${intcommas(data[row].comision)}</td>
                            </tr>`).join("")}
                        </tbody>
                    </table>`;

        content.html(html);
        modal.iziModal('open')
    };

    function corriente_row(data) {
        let today = new Date();
        const $vencidas = reduce_count(data, undefined, today, 'id', show_data);
        const $vencidas30 = reduce_count(data, today, today.addDays(30), 'id', show_data);
        const $vencidas60 = reduce_count(data, today.addDays(30), today.addDays(60), 'id', show_data);
        const $vencidas90 = reduce_count(data, today.addDays(60), today.addDays(90), 'id', show_data);
        const $vencidas120 = reduce_count(data, today.addDays(90), today.addDays(120), 'id', show_data);
        const $vencidas_ = reduce_count(data, today.addDays(120), undefined, 'id', show_data);
        const $vencidast = reduce_count(data, today, undefined, 'id', show_data);
        return $(`
                <tr>
                    <td>#</td>
                    <td class="numberinput"><a data-swap="$vencidas"></a></td>
                    <td class="numberinput"><a data-swap="$vencidas30"></a></td>
                    <td class="numberinput"><a data-swap="$vencidas60"></a></td>
                    <td class="numberinput"><a data-swap="$vencidas90"></a></td>
                    <td class="numberinput"><a data-swap="$vencidas120"></a></td>
                    <td class="numberinput"><a data-swap="$vencidas_"></a></td>
                    <td class="numberinput"><a data-swap="$vencidast"></a></td>
                </tr>
                <tr>
                    <td>Prima</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, undefined, today, 'prima'))}</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, today, today.addDays(30), 'prima'))}</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, today.addDays(30), today.addDays(60), 'prima'))}</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, today.addDays(60), today.addDays(90), 'prima'))}</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, today.addDays(90), today.addDays(120), 'prima'))}</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, today.addDays(120), undefined, 'prima'))}</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, today, undefined, 'prima'))}</td>
                </tr>
                <tr>
                    <td>Comisión</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, undefined, today, 'comision'))}</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, today, today.addDays(30), 'comision'))}</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, today.addDays(30), today.addDays(60), 'comision'))}</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, today.addDays(60), today.addDays(90), 'comision'))}</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, today.addDays(90), today.addDays(120), 'comision'))}</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, today.addDays(120), undefined, 'comision'))}</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, today, undefined, 'comision'))}</td>
                </tr>
            `).swapIn({$vencidas, $vencidas30, $vencidas60, $vencidas90, $vencidas120, $vencidas_, $vencidast})
    }

    $.ajax('.', {
        method: 'POST',
        data: {vencimiento: 'vencimiento'},
        success: function (response) {
            let vencimiento_cordobas = response.vencimiento_Cordoba.map(fix_date);
            let vencimiento_dolares = response.vencimiento_Dolar.map(fix_date);
            const polizas_cordobas = $('#vencimiento-cordobas tbody').empty();
            const polizas_dolares = $('#vencimiento-dolares tbody').empty();

            polizas_cordobas.append(corriente_row(vencimiento_cordobas));
            polizas_dolares.append(corriente_row(vencimiento_dolares));
        }
    });


});