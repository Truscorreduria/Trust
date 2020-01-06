$(document).ready(function(){
    $(document).on('change', 'select#filter_departamento', function(){
        const _this = $(this);
        $.ajax($ajax_getCollection, {
            method: "POST",
            data: {
                app_label: 'utils',
                model: 'municipio',
                filters: `{'departamento_id': '${_this.val()}'}`
            },
            success: function(response){
                const municipio = $('#filter_municipio').empty();
                municipio.append(`<option value="">---------</option>`);
                $.each(response, function(i, o){
                    municipio.append(`<option value="${o.id}">${o.name}</option>`);
                })
            }
        })
    })
})