$(document).ready(function () {

    function fix_date(obj) {
        obj['fecha_vence'] = new Date(obj.fecha_vence);
        return obj;
    }

    const show_data = function () {
        const data = $(this).data();
        let html = `<div class="container-fluid"> 
                        <div class="table-responsive">
                            <table class="table" id="report-table" style="width: 100%">
                            <thead>
                                <tr>
                                    <td>Número de Póliza</td>
                                    <td>Cliente</td>
                                    <td>Contratante</td>
                                    <td>Ejecutivo</td>
                                    <td>Fecha de cuota</td>
                                    <td class="numberinput">Monto cuota</td>
                                </tr>
                            </thead>
                            <tbody>
                                ${Object.keys(data).map(row => `<tr>
                                    <td><a href="/trustseguros/polizas/#${data[row].id_poliza}">${data[row].no_poliza}</a></td>
                                    <td>${data[row].cliente}</td>
                                    <td>${data[row].contratante}</td>
                                    <td>${data[row].ejecutivo}</td>
                                    <td>${data[row].fecha_vence.toLocaleString('es-NI').slice(0, 10)}</td>
                                    <td class="numberinput">${intcommas(data[row].prima)}</td>
                                </tr>`).join("")}
                            </tbody>
                        </table>
                        </div>
                        <div class="row float-right">
                            <button type="button" class="btn btn-info btn-download">
                                <i class="fa fa-file-excel"></i>
                                Descargar
                            </button>
                        </div>
                    </div>`;
        dashModal.iziModal('destroy');
        dashModal.empty().append(html);
        dashModal.iziModal({
            title: 'Cartera',
            width: 1200, padding: 20, fullscreen: false, zindex: 1500,
            headerColor: '#326634'
        }).iziModal('open');

        $('#report-table').dataTable({
            dom: 'Bfrtip',
            language: ES_ni,
        });
        $('.btn-download')
            .off('click')
            .on('click', () => {
                export_to_excel(data, "Carterak.xlsx");
            })
    };

    function vencida_row(data) {
        let today = new Date();

        const $vencidas30 = reduce_count(data, today.addDays(-30), today, 'no_poliza', show_data);
        const $vencidas60 = reduce_count(data, today.addDays(-60), today.addDays(-30), 'no_poliza', show_data);
        const $vencidas90 = reduce_count(data, today.addDays(-90), today.addDays(-60), 'no_poliza', show_data);
        const $vencidas120 = reduce_count(data, today.addDays(-120), today.addDays(-90), 'no_poliza', show_data);
        const $vencidas_ = reduce_count(data, undefined, today.addDays(-120), 'no_poliza', show_data);
        const $vencidast = reduce_count(data, undefined, today, 'no_poliza', show_data);

        const $primas30 = reduce_sum(data, today.addDays(-30), today, 'prima', show_data);
        const $primas60 = reduce_sum(data, today.addDays(-60), today.addDays(-30), 'prima', show_data);
        const $primas90 = reduce_sum(data, today.addDays(-90), today.addDays(-60), 'prima', show_data);
        const $primas120 = reduce_sum(data, today.addDays(-120), today.addDays(-90), 'prima', show_data);
        const $primas_ = reduce_sum(data, undefined, today.addDays(-120), 'prima', show_data);
        const $primast = reduce_sum(data, undefined, today, 'prima', show_data);

        const $comision30 = reduce_sum(data, today.addDays(-30), today, 'comision', show_data);
        const $comision60 = reduce_sum(data, today.addDays(-60), today.addDays(-30), 'comision', show_data);
        const $comision90 = reduce_sum(data, today.addDays(-90), today.addDays(-60), 'comision', show_data);
        const $comision120 = reduce_sum(data, today.addDays(-120), today.addDays(-90), 'comision', show_data);
        const $comision_ = reduce_sum(data, undefined, today.addDays(-120), 'comision', show_data);
        const $comisiont = reduce_sum(data, undefined, today, 'comision', show_data);


        return $(`
                <tr>
                    <td>#</td>
                    <td class="numberinput"><a data-swap="$vencidas30"></a></td>
                    <td class="numberinput"><a data-swap="$vencidas60"></a></td>
                    <td class="numberinput"><a data-swap="$vencidas90"></a></td>
                    <td class="numberinput"><a data-swap="$vencidas120"></a></td>
                    <td class="numberinput"><a data-swap="$vencidas_"></a></td>
                    <td class="numberinput"><a data-swap="$vencidast"></a></td>
                </tr>
                <tr>
                    <td>Prima</td>
                    <td class="numberinput"><a data-swap="$primas30"></a></td>
                    <td class="numberinput"><a data-swap="$primas60"></a></td>
                    <td class="numberinput"><a data-swap="$primas90"></a></td>
                    <td class="numberinput"><a data-swap="$primas120"></a></td>
                    <td class="numberinput"><a data-swap="$primas_"></a></td>
                    <td class="numberinput"><a data-swap="$primast"></a></td>
                </tr>
                <tr>
                    <td>Comisión</td>
                    <td class="numberinput"><a data-swap="$comision30"></a></td>
                    <td class="numberinput"><a data-swap="$comision60"></a></td>
                    <td class="numberinput"><a data-swap="$comision90"></a></td>
                    <td class="numberinput"><a data-swap="$comision120"></a></td>
                    <td class="numberinput"><a data-swap="$comision_"></a></td>
                    <td class="numberinput"><a data-swap="$comisiont"></a></td>
                </tr>
            `).swapIn({
            $vencidas30, $vencidas60, $vencidas90, $vencidas120, $vencidas_, $vencidast,
            $primas30, $primas60, $primas90, $primas120, $primas_, $primast,
            $comision30, $comision60, $comision90, $comision120, $comision_, $comisiont,
        })
    }

    function corriente_row(data) {
        let today = new Date();
        const $vencidas30 = reduce_count(data, today, today.addDays(30), 'no_poliza', show_data);
        const $vencidas60 = reduce_count(data, today.addDays(30), today.addDays(60), 'no_poliza', show_data);
        const $vencidas90 = reduce_count(data, today.addDays(60), today.addDays(90), 'no_poliza', show_data);
        const $vencidas120 = reduce_count(data, today.addDays(90), today.addDays(120), 'no_poliza', show_data);
        const $vencidas_ = reduce_count(data, today.addDays(120), undefined, 'no_poliza', show_data);
        const $vencidast = reduce_count(data, today, undefined, 'no_poliza', show_data);

        const $primas30 = reduce_sum(data, today, today.addDays(30), 'prima', show_data);
        const $primas60 = reduce_sum(data, today.addDays(30), today.addDays(60), 'prima', show_data);
        const $primas90 = reduce_sum(data, today.addDays(60), today.addDays(90), 'prima', show_data);
        const $primas120 = reduce_sum(data, today.addDays(90), today.addDays(120), 'prima', show_data);
        const $primas_ = reduce_sum(data, today.addDays(120), undefined, 'prima', show_data);
        const $primast = reduce_sum(data, today, undefined, 'prima', show_data);

        const $comision30 = reduce_sum(data, today, today.addDays(30), 'comision', show_data);
        const $comision60 = reduce_sum(data, today.addDays(30), today.addDays(60), 'comision', show_data);
        const $comision90 = reduce_sum(data, today.addDays(60), today.addDays(90), 'comision', show_data);
        const $comision120 = reduce_sum(data, today.addDays(90), today.addDays(120), 'comision', show_data);
        const $comision_ = reduce_sum(data, today.addDays(120), undefined, 'comision', show_data);
        const $comisiont = reduce_sum(data, today, undefined, 'comision', show_data);
        return $(`
                <tr>
                    <td>#</td>
                    <td class="numberinput"><a data-swap="$vencidas30"></a></td>
                    <td class="numberinput"><a data-swap="$vencidas60"></a></td>
                    <td class="numberinput"><a data-swap="$vencidas90"></a></td>
                    <td class="numberinput"><a data-swap="$vencidas120"></a></td>
                    <td class="numberinput"><a data-swap="$vencidas_"></a></td>
                    <td class="numberinput"><a data-swap="$vencidast"></a></td>
                </tr>
                <tr>
                    <td>Prima</td>
                    <td class="numberinput"><a data-swap="$primas30"></a></td>
                    <td class="numberinput"><a data-swap="$primas60"></a></td>
                    <td class="numberinput"><a data-swap="$primas90"></a></td>
                    <td class="numberinput"><a data-swap="$primas120"></a></td>
                    <td class="numberinput"><a data-swap="$primas_"></a></td>
                    <td class="numberinput"><a data-swap="$primast"></a></td>
                </tr>
                <tr>
                    <td>Comisión</td>
                    <td class="numberinput"><a data-swap="$comision30"></a></td>
                    <td class="numberinput"><a data-swap="$comision60"></a></td>
                    <td class="numberinput"><a data-swap="$comision90"></a></td>
                    <td class="numberinput"><a data-swap="$comision120"></a></td>
                    <td class="numberinput"><a data-swap="$comision_"></a></td>
                    <td class="numberinput"><a data-swap="$comisiont"></a></td>
                </tr>
            `).swapIn({
            $vencidas30, $vencidas60, $vencidas90, $vencidas120, $vencidas_, $vencidast,
            $primas30, $primas60, $primas90, $primas120, $primas_, $primast,
            $comision30, $comision60, $comision90, $comision120, $comision_, $comisiont,
        })
    };

    const load_data = function () {
        $.ajax('.', {
            method: 'POST',
            data: {cartera: 'cartera', 'grupo': $('select[name="grupo"]').val()},
            success: function (response) {
                let cartera_cordobas = response.cartera_Cordoba.map(fix_date);
                let cartera_dolares = response.cartera_Dolar.map(fix_date);


                let corriente_cordobas = $('#corriente-cordobas tbody').empty();
                let corriente_dolares = $('#corriente-dolares tbody').empty();
                corriente_cordobas.append(corriente_row(cartera_cordobas));
                corriente_dolares.append(corriente_row(cartera_dolares));


                let vencida_cordobas = $('#vencida-cordobas tbody').empty();
                let vencida_dolares = $('#vencida-dolares tbody').empty();
                vencida_cordobas.append(vencida_row(cartera_cordobas));
                vencida_dolares.append(vencida_row(cartera_dolares));
            }
        })
    };

    load_data();

    $('select[name="grupo"]').on('change', load_data)
});