(function ($) {
    $(document).ready(function () {
        $('#id_departamento').on('change', function () {
            departamento = $(this).val();
            $.ajax($ajax_getColletion, {
                method: "post",
                data: {
                    app_label: 'cotizador', model: 'municipio',
                    filters: `{'departamento_id': ${departamento}}`
                },
                success: function (response) {
                    element = $('#id_municipio').empty();
                    element.append(`<option>---------</option>`);
                    $.each(response, function (i, o) {
                        element.append(`<option value="${o.id}">${o.name}</option>`)
                    })
                }
            })
        });
    });
})(grp.jQuery);