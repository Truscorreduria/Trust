$(document).ready(function () {
    const modal = $('#dashboard-modal').iziModal({
        width: 1200, padding: 20, fullscreen: false, zindex: 1500,
        headerColor: '#326634'
    });


    const show_data = function () {
        const data = $(this).data();
        const content = modal.find('.modal-body').empty();
        let html = ` <table class="table">
                        <thead>
                            <tr>
                                <td>Número</td>
                                <td>Prospecto</td>
                                <td>Campaña</td>
                                <td class="numberinput">Días</td>
                                <td class="numberinput">Valor nuevo</td>
                            </tr>
                        </thead>
                        <tbody>
                            ${Object.keys(data).map(row => `<tr>
                                <td><a href="/trustseguros/oportunidades/${data[row].linea}/#${data[row].id}">${data[row].code}</a></td>
                                <td>${data[row].prospect.name}</td>
                                <td>${data[row].campain.name}</td>
                                <td class="numberinput">${data[row].dias}</td>
                                <td class="numberinput">${data[row].valor_nuevo}</td>
                            </tr>`).join("")}
                        </tbody>
                    </table>`;

        content.html(html);
        modal.iziModal('open')
    };


    function make_link(data) {
        return $('<a href="javascript:void(0)"></a>')
            .text(data.length)
            .data(data)
            .on('click', show_data)
    }

    const load_data = function () {
        $.ajax('.', {
            method: 'POST',
            data: {crm: 'crm', desde: $('#id_desde').val(), hasta: $('#id_hasta').val()},
            success: function (response) {
                let sellers = _.groupBy(response.oportunidades, 'vendedor.full_name');
                let crm = $('#dashboard-crm tbody').empty();
                Object.keys(sellers).map(function (o, i) {
                    const status1 = make_link(sellers[o].filter(el => el.status.id === 1));
                    const status2 = make_link(sellers[o].filter(el => el.status.id === 2));
                    const status3 = make_link(sellers[o].filter(el => el.status.id === 3));
                    const status4 = make_link(sellers[o].filter(el => el.status.id === 4));
                    const status5 = make_link(sellers[o].filter(el => el.status.id === 5));
                    const status6 = make_link(sellers[o].filter(el => el.status.id === 6));
                    const total = make_link(sellers[o]);
                    crm.append($(`<tr>
                        <td>${o}</td>
                        <td class="numberinput"><a data-swap="status1"></a></td>
                        <td class="numberinput"><a data-swap="status2"></a></td>
                        <td class="numberinput"><a data-swap="status3"></a></td>
                        <td class="numberinput"><a data-swap="status4"></a></td>
                        <td class="numberinput"><a data-swap="status5"></a></td>
                        <td class="numberinput"><a data-swap="status6"></a></td>
                        <td class="numberinput"><a data-swap="total"></a></td>
                    </tr>`).swapIn({status1, status2, status3, status4, status5, status6, total}))
                });
            }
        })
    };


    $('#id_desde').on('change', load_data);
    $('#id_hasta').on('change', load_data);


    load_data();

});