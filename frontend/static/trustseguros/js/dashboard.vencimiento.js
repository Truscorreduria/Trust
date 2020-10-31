$(document).ready(function () {

    Date.prototype.addDays = function (days) {
        let date = new Date(this.valueOf());
        date.setDate(date.getDate() + days);
        return date;
    };

    function fix_date(obj) {
        obj['fecha_emision'] = new Date(obj.fecha_vence);
        obj['fecha_vence'] = new Date(obj.fecha_vence);
        return obj;
    }

    function reduce_sum(data, start, end, field) {
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

    function reduce_count(data, start, end, field) {
        let filtered_data = [];
        if (start !== undefined && end !== undefined) {
            filtered_data = data.filter(obj => obj.fecha_vence >= start && obj.fecha_vence <= end)
        }
        if (start === undefined && end !== undefined) {
            filtered_data = data.filter(obj => obj.fecha_vence <= end)
        }
        if (start !== undefined && end === undefined) {
            filtered_data = data.filter(obj => obj.fecha_vence >= start)
        }
        return Object.keys(_.groupBy(filtered_data, field)).length
    }

    function corriente_row(data) {
        let today = new Date();
        return `
                <tr>
                    <td>#</td>
                    <td class="numberinput">${intcommas(reduce_count(data, today, today.addDays(30), 'id'))}</td>
                    <td class="numberinput">${intcommas(reduce_count(data, today, today.addDays(30), 'id'))}</td>
                    <td class="numberinput">${intcommas(reduce_count(data, today.addDays(30), today.addDays(60), 'id'))}</td>
                    <td class="numberinput">${intcommas(reduce_count(data, today.addDays(60), today.addDays(90), 'id'))}</td>
                    <td class="numberinput">${intcommas(reduce_count(data, today.addDays(90), today.addDays(120), 'id'))}</td>
                    <td class="numberinput">${intcommas(reduce_count(data, today.addDays(120), undefined, 'id'))}</td>
                    <td class="numberinput">${intcommas(reduce_count(data, today, undefined, 'id'))}</td>
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
        data: {vencimiento: 'vencimiento'},
        success: function (response) {
            let vencimiento_cordobas = response.vencimiento_Cordoba.map(fix_date);
            let vencimiento_dolares = response.vencimiento_Dolar.map(fix_date);
            const polizas_cordobas = $('#vencimiento-cordobas tbody').empty();
            const polizas_dolares = $('#vencimiento-dolares tbody').empty();

            polizas_cordobas.append(corriente_row(vencimiento_cordobas));
            polizas_dolares.append(corriente_row(vencimiento_dolares));
        }
    })
});