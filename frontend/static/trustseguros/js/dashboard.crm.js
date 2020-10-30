$(document).ready(function () {
    $.ajax('.', {
        method: 'POST',
        data: {crm: 'crm'},
        success: function (response) {
            let sellers = _.groupBy(response.oportunidades, 'vendedor.full_name');
            let crm = $('#dashboard-crm tbody').empty();
            Object.keys(sellers).map(function (o, i) {
                let status1 = sellers[o].filter(el => el.status.id === 1);
                let status2 = sellers[o].filter(el => el.status.id === 2);
                let status3 = sellers[o].filter(el => el.status.id === 3);
                let status4 = sellers[o].filter(el => el.status.id === 4);
                let status5 = sellers[o].filter(el => el.status.id === 5);
                let status6 = sellers[o].filter(el => el.status.id === 6);
                crm.append(
                    `<tr>
                        <td>${o}</td>
                        <td class="numberinput">${status1.length}</td>
                        <td class="numberinput">${status2.length}</td>
                        <td class="numberinput">${status3.length}</td>
                        <td class="numberinput">${status4.length}</td>
                        <td class="numberinput">${status5.length}</td>
                        <td class="numberinput">${status6.length}</td>
                        <td class="numberinput">${sellers[o].length}</td>
                    </tr>`
                )
            });
        }
    })
});