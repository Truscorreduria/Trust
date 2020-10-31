$(document).ready(function () {

    function fix_date(obj) {
        obj['fecha_vence'] = new Date(obj.fecha_vence);
        return obj;
    }

    function vencida_row(data) {
        let today = new Date();
        return `
                <tr>
                    <td>#</td>
                    <td class="numberinput">${intcommas(reduce_count(data, today.addDays(-30), today, 'poliza'))}</td>
                    <td class="numberinput">${intcommas(reduce_count(data, today.addDays(-60), today.addDays(-30), 'poliza'))}</td>
                    <td class="numberinput">${intcommas(reduce_count(data, today.addDays(-90), today.addDays(-60), 'poliza'))}</td>
                    <td class="numberinput">${intcommas(reduce_count(data, today.addDays(-120), today.addDays(-90), 'poliza'))}</td>
                    <td class="numberinput">${intcommas(reduce_count(data, undefined, today.addDays(-120), 'poliza'))}</td>
                    <td class="numberinput">${intcommas(reduce_count(data, undefined, today, 'poliza'))}</td>
                </tr>
                <tr>
                    <td>Prima</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, today.addDays(-30), today, 'prima'))}</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, today.addDays(-60), today.addDays(-30), 'prima'))}</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, today.addDays(-90), today.addDays(-60), 'prima'))}</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, today.addDays(-120), today.addDays(-90), 'prima'))}</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, undefined, today.addDays(-120), 'prima'))}</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, undefined, today, 'prima'))}</td>
                </tr>
                <tr>
                    <td>Comisión</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, today.addDays(-30), today, 'comision'))}</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, today.addDays(-60), today.addDays(-30), 'comision'))}</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, today.addDays(-90), today.addDays(-60), 'comision'))}</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, today.addDays(-120), today.addDays(-90), 'comision'))}</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, undefined, today.addDays(-120), 'comision'))}</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, undefined, today, 'comision'))}</td>
                </tr>
            `
    }

    function corriente_row(data) {
        let today = new Date();
        return `
                <tr>
                    <td>#</td>
                    <td class="numberinput">${intcommas(reduce_count(data, today, today.addDays(30), 'poliza'))}</td>
                    <td class="numberinput">${intcommas(reduce_count(data, today.addDays(30), today.addDays(60), 'poliza'))}</td>
                    <td class="numberinput">${intcommas(reduce_count(data, today.addDays(60), today.addDays(90), 'poliza'))}</td>
                    <td class="numberinput">${intcommas(reduce_count(data, today.addDays(90), today.addDays(120), 'poliza'))}</td>
                    <td class="numberinput">${intcommas(reduce_count(data, today.addDays(120), undefined, 'poliza'))}</td>
                    <td class="numberinput">${intcommas(reduce_count(data, today, undefined, 'poliza'))}</td>
                </tr>
                <tr>
                    <td>Prima</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, today, today.addDays(30), 'prima'))}</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, today.addDays(30), today.addDays(60), 'prima'))}</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, today.addDays(60), today.addDays(90), 'prima'))}</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, today.addDays(90), today.addDays(120), 'prima'))}</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, today.addDays(120), undefined, 'prima'))}</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, today, undefined, 'prima'))}</td>
                </tr>
                <tr>
                    <td>Comisión</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, today, today.addDays(30), 'comision'))}</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, today.addDays(30), today.addDays(60), 'comision'))}</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, today.addDays(60), today.addDays(90), 'comision'))}</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, today.addDays(90), today.addDays(120), 'comision'))}</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, today.addDays(120), undefined, 'comision'))}</td>
                    <td class="numberinput">${intcommas(reduce_sum(data, today, undefined, 'comision'))}</td>
                </tr>
            `
    }

    $.ajax('.', {
        method: 'POST',
        data: {cartera: 'cartera'},
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
});