$(document).ready(function () {

    function fix_date(obj) {
        obj['fecha_emision'] = new Date(obj.fecha_emision);
        obj['fecha_vence'] = new Date(obj.fecha_vence);
        return obj;
    }

    const show_data = function () {
        const data = $(this).data();
        let html = ` <table class="table">
                        <thead>
                            <tr>
                                <td>Número de Póliza</td>
                                <td>Fecha de emisión</td>
                                <td>Fecha de vencimiento</td>
                                <td>Cliente</td>
                                <td>Contratante</td>
                                <td>Ejecutivo</td>
                                <td class="numberinput">Prima</td>
                            </tr>
                        </thead>
                        <tbody>
                            ${Object.keys(data).map(row => `<tr>
                                <td><a href="/trustseguros/polizas/#${data[row].id}">${data[row].no_poliza}</a></td>
                                <td>${data[row].fecha_emision.toLocaleString('es-NI').slice(0, 10)}</td>
                                <td>${data[row].fecha_vence.toLocaleString('es-NI').slice(0, 10)}</td>
                                <td>${data[row].cliente}</td>
                                <td>${data[row].contratante}</td>
                                <td>${data[row].ejecutivo}</td>
                                <td class="numberinput">${intcommas(data[row].prima)}</td>
                            </tr>`).join("")}
                        </tbody>
                    </table>`;

        dashModal.iziModal('destroy');
        dashModal.empty().append(html);
        dashModal.iziModal({
            title: 'Pólizas por vencer',
            width: 1600, padding: 20, fullscreen: false, zindex: 1500,
            headerColor: '#326634'
        }).iziModal('open')
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

        const $primas = reduce_sum(data, undefined, today, 'prima', show_data);
        const $primas30 = reduce_sum(data, today, today.addDays(30), 'prima', show_data);
        const $primas60 = reduce_sum(data, today.addDays(30), today.addDays(60), 'prima', show_data);
        const $primas90 = reduce_sum(data, today.addDays(60), today.addDays(90), 'prima', show_data);
        const $primas120 = reduce_sum(data, today.addDays(90), today.addDays(120), 'prima', show_data);
        const $primas_ = reduce_sum(data, today.addDays(120), undefined, 'prima', show_data);
        const $primast = reduce_sum(data, today, undefined, 'prima', show_data);

        const $comision = reduce_sum(data, undefined, today, 'comision', show_data);
        const $comision30 = reduce_sum(data, today, today.addDays(30), 'comision', show_data);
        const $comision60 = reduce_sum(data, today.addDays(30), today.addDays(60), 'comision', show_data);
        const $comision90 = reduce_sum(data, today.addDays(60), today.addDays(90), 'comision', show_data);
        const $comision120 = reduce_sum(data, today.addDays(90), today.addDays(120), 'comision', show_data);
        const $comision_ = reduce_sum(data, today.addDays(120), undefined, 'comision', show_data);
        const $comisiont = reduce_sum(data, today, undefined, 'comision', show_data);
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
                    <td class="numberinput"><a data-swap="$primas"></a></td>
                    <td class="numberinput"><a data-swap="$primas30"></a></td>
                    <td class="numberinput"><a data-swap="$primas60"></a></td>
                    <td class="numberinput"><a data-swap="$primas90"></a></td>
                    <td class="numberinput"><a data-swap="$primas120"></a></td>
                    <td class="numberinput"><a data-swap="$primas_"></a></td>
                    <td class="numberinput"><a data-swap="$primast"></a></td>
                </tr>
                <tr>
                    <td>Comisión</td>
                    <td class="numberinput"><a data-swap="$comision"></a></td>
                    <td class="numberinput"><a data-swap="$comision30"></a></td>
                    <td class="numberinput"><a data-swap="$comision60"></a></td>
                    <td class="numberinput"><a data-swap="$comision90"></a></td>
                    <td class="numberinput"><a data-swap="$comision120"></a></td>
                    <td class="numberinput"><a data-swap="$comision_"></a></td>
                    <td class="numberinput"><a data-swap="$comisiont"></a></td>
                </tr>
            `).swapIn({
            $vencidas, $vencidas30, $vencidas60, $vencidas90, $vencidas120, $vencidas_, $vencidast,
            $primas, $primas30, $primas60, $primas90, $primas120, $primas_, $primast,
            $comision, $comision30, $comision60, $comision90, $comision120, $comision_, $comisiont,
        })
    };

    const load_data = function () {
        $.ajax('.', {
            method: 'POST',
            data: {vencimiento: 'vencimiento', 'grupo': $('select[name="grupo"]').val()},
            success: function (response) {
                let vencimiento_cordobas = response.vencimiento_Cordoba.map(fix_date);
                let vencimiento_dolares = response.vencimiento_Dolar.map(fix_date);
                const polizas_cordobas = $('#vencimiento-cordobas tbody').empty();
                const polizas_dolares = $('#vencimiento-dolares tbody').empty();

                polizas_cordobas.append(corriente_row(vencimiento_cordobas));
                polizas_dolares.append(corriente_row(vencimiento_dolares));
            }
        });
    };

    load_data();

    $('select[name="grupo"]').on('change', load_data)


});