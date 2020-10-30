$(document).ready(function () {

    function monto_pagado(acc, val) {
        let o = acc.filter(function (obj) {
            return obj.id == val.id;
        }).pop() || {name: val.id, monto_pagado: 0};

        o.monto_pagado += val.monto_pagado;
        acc.push(o);
        return acc;
    }

    $.ajax('.', {
        method: 'POST',
        data: {},
        success: function (response) {
            let monto = response.siniestros.reduce(monto_pagado, [])[0].monto_pagado;
            if (monto.length > 0) {
                monto = monto[0].monto_pagado
            } else {
                monto = 0;
            }
            let siniestros = $('#dashboard-siniestros tbody').empty();
            siniestros.append(
                `<tr>
                    <td>${response.siniestros.length}</td>
                    <td>${monto}</td>
                    <td>${monto}</td>
                    <td>${monto}</td>
                </tr>`
            )
        }
    })
});