$(document).ready(function () {

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

    $.ajax('.', {
        method: 'POST',
        data: {cartera: 'cartera'},
        success: function (response) {
            let cartera_cordobas = response.cartera_Cordoba.map(fix_date);
            let cartera_dolares = response.cartera_Dolar.map(fix_date);

            let today = new Date();


            let cordobas = $('#cobranza-cordobas tbody').empty();
            let dolares = $('#cobranza-dolares tbody').empty();

            cordobas.append(`
                <tr>
                    <td>Prima</td>
                    <td class="numberinput">${intcommas(reduce_data(cartera_cordobas, today, undefined, 'prima'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(cartera_cordobas, today - 30, today, 'prima'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(cartera_cordobas, today - 60, today - 30, 'prima'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(cartera_cordobas, today - 90, today - 60, 'prima'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(cartera_cordobas, today - 120, today - 90, 'prima'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(cartera_cordobas, undefined, today - 120, 'prima'))}</td>
                    <td class="numberinput">${intcommas(cartera_cordobas.reduce((acc, val) => {
                acc += val.prima;
                return parseFloat(acc.toFixed(2));
            }, 0))}</td>
                </tr>
                <tr>
                    <td>Comisión</td>
                    <td class="numberinput">${intcommas(reduce_data(cartera_cordobas, today, undefined, 'comision'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(cartera_cordobas, today - 30, today, 'comision'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(cartera_cordobas, today - 60, today - 30, 'comision'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(cartera_cordobas, today - 90, today - 60, 'comision'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(cartera_cordobas, today - 120, today - 90, 'comision'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(cartera_cordobas, undefined, today - 120, 'comision'))}</td>
                    <td class="numberinput">${intcommas(cartera_cordobas.reduce((acc, val) => {
                acc += val.comision;
                return parseFloat(acc.toFixed(2));
            }, 0))}</td>
                </tr>
            `);

            dolares.append(`
                <tr>
                    <td>Prima</td>
                    <td class="numberinput">${intcommas(reduce_data(cartera_dolares, today, undefined, 'prima'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(cartera_dolares, today - 30, today, 'prima'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(cartera_dolares, today - 60, today - 30, 'prima'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(cartera_dolares, today - 90, today - 60, 'prima'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(cartera_dolares, today - 120, today - 90, 'prima'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(cartera_dolares, undefined, today - 120, 'prima'))}</td>
                    <td class="numberinput">${intcommas(cartera_dolares.reduce((acc, val) => {
                acc += val.prima;
                return parseFloat(acc.toFixed(2));
            }, 0))}</td>
                </tr>
                <tr>
                    <td>Comisión</td>
                    <td class="numberinput">${intcommas(reduce_data(cartera_dolares, today, undefined, 'comision'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(cartera_dolares, today - 30, today, 'comision'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(cartera_dolares, today - 60, today - 30, 'comision'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(cartera_dolares, today - 90, today - 60, 'comision'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(cartera_dolares, today - 120, today - 90, 'comision'))}</td>
                    <td class="numberinput">${intcommas(reduce_data(cartera_dolares, undefined, today - 120, 'comision'))}</td>
                    <td class="numberinput">${intcommas(cartera_dolares.reduce((acc, val) => {
                acc += val.comision;
                return parseFloat(acc.toFixed(2));
            }, 0))}</td>
                </tr>
            `);
        }
    })
});