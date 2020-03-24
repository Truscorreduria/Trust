$(document).ready(function () {

    function addDays(date, days) {
        date.setDate(date.getDate() + days);
        return date;
    }

    $(document).on('change', '#id_fecha_emision', function () {
        let emision = $(this).val().split('/');
        let inicio = new Date(`${emision[1]}/${emision[0]}/${emision[2]}`);
        let fin = addDays(inicio, 365);
        $('#id_fecha_vence').val(moment(fin).format('DD/MM/YYYY'));
    })
});