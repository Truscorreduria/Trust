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

    const load_data = function () {
        $.ajax('.', {
            method: 'POST',
            data: {
                canceladas: 'canceladas',
                desde: $('.card-canceladas input[name="desde"]').val(),
                hasta: $('.card-canceladas input[name="hasta"]').val(),
            },
            success: function (response) {
                let data = response.canceladas.map(fix_date);
                const span_canceladas = $('#dashboard-canceladas').empty();
                let today = new Date();
                const $canceladas = reduce_count(data, undefined, today, 'id', show_data);
                span_canceladas.append($canceladas)
            }
        });
    };

    $('.card-canceladas input[name="desde"]').on('change', load_data);
    $('.card-canceladas input[name="hasta"]').on('change', load_data);

    load_data();

});