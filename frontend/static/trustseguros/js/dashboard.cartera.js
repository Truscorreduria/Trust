$(document).ready(function () {

    Date.prototype.addDays = function (days) {
        let date = new Date(this.valueOf());
        date.setDate(date.getDate() + days);
        return date;
    };

    function fix_date(obj) {
        obj['fecha_vence'] = new Date(obj.fecha_vence);
        return obj;
    }

    function reduce_data(data, start, end, field) {
        return data.reduce((acc, val) => {
            if (start !== undefined && end !== undefined) {
                if (val.fecha_vence >= start && val.fecha_vence <= end) {
                    acc = parseFloat(acc) + parseFloat(val[field])
                }
            }
            if (start === undefined && end !== undefined) {
                if (val.fecha_vence <= end) {
                    acc = parseFloat(acc) + parseFloat(val[field])
                }
            }
            if (start !== undefined && end === undefined) {
                if (val.fecha_vence >= start) {
                    acc = parseFloat(acc) + parseFloat(val[field])
                }
            }
            return parseFloat(acc).toFixed(2);
        }, 0);
    }

    function vencida_row(data) {
        let today = new Date();
        return `
                <tr>
                    <td>Prima</td>
                    <td class="numberinput">${intcommas(reduce_data(data, today.addDays(-30), today, 'prima'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(data, today.addDays(-60), today.addDays(-30), 'prima'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(data, today.addDays(-90), today.addDays(-60), 'prima'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(data, today.addDays(-120), today.addDays(-90), 'prima'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(data, undefined, today.addDays(-120), 'prima'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(data, undefined, today, 'prima'))}</td>
                </tr>
                <tr>
                    <td>Comisión</td>
                    <td class="numberinput">${intcommas(reduce_data(data, today.addDays(-30), today, 'comision'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(data, today.addDays(-60), today.addDays(-30), 'comision'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(data, today.addDays(-90), today.addDays(-60), 'comision'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(data, today.addDays(-120), today.addDays(-90), 'comision'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(data, undefined, today.addDays(-120), 'comision'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(data, undefined, today, 'comision'))}</td>
                </tr>
            `
    }

    function corriente_row(data) {
        let today = new Date();
        return `
                <tr>
                    <td>Prima</td>
                    <td class="numberinput">${intcommas(reduce_data(data, today, today.addDays(30), 'prima'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(data, today.addDays(30), today.addDays(60), 'prima'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(data, today.addDays(60), today.addDays(90), 'prima'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(data, today.addDays(90), today.addDays(120), 'prima'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(data, today.addDays(120), undefined, 'prima'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(data, today, undefined, 'prima'))}</td>
                </tr>
                <tr>
                    <td>Comisión</td>
                    <td class="numberinput">${intcommas(reduce_data(data, today, today.addDays(30), 'comision'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(data, today.addDays(30), today.addDays(60), 'comision'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(data, today.addDays(60), today.addDays(90), 'comision'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(data, today.addDays(90), today.addDays(120), 'comision'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(data, today.addDays(120), undefined, 'comision'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(data, today, undefined, 'comision'))}</td>
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