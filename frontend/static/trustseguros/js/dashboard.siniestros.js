$(document).ready(function () {


    const show_data = function () {
        const data = $(this).data();
        let html = `<div class="container-fluid"> 
                        <div class="table-responsive">
                            <table class="table" id="report-table" style="width: 100%">
                                <thead>
                                    <tr>
                                        <td>Reclamo aseguradora</td>
                                        <td>Cliente</td>
                                        <td>Póliza</td>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${Object.keys(data).map(row => `<tr>
                                        <td><a href="/trustseguros/siniestro/#${data[row].id}">${data[row].reclamo_aseguradora}</a></td>
                                        <td>${data[row].cliente.name}</td>
                                        <td>${data[row].poliza.number}</td>
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
                export_to_excel(data, "Siniestros.xlsx");
            })
    };

    $.ajax('.', {
        method: 'POST',
        data: {siniestros: 'siniestros'},
        success: function (response) {
            console.log(response)
            const $totalcasos = reduce_count(response.siniestros, undefined, undefined, 'id', show_data);
            const $montoreclamado = reduce_sum(response.siniestros, undefined, undefined, 'monto_reclamo', show_data);
            const $montopagado = reduce_sum(response.siniestros, undefined, undefined, 'monto_pagado', show_data);
            let siniestros = $('#dashboard-siniestros tbody').empty();
            let html = $(`<tr>
                    <td class="numberinput"><a data-swap="$totalcasos"></a></td>
                    <td class="numberinput"><a data-swap="$montopagado"></a></td>
                </tr>`).swapIn({$montopagado, $montoreclamado, $totalcasos});
            siniestros.append(html)
        }
    })
});