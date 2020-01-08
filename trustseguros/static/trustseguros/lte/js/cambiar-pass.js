$(document).ready(function(){
    $(document).on('click', 'btn-cambiar-pass', function(){
        const _this = $(this);
        $.ajax($ajax_getCollection, {
            method: "POST",
            data: {
                app_label: 'utils',
                model: 'municipio',
                filters: `{'departamento_id': '${_this.val()}'}`
            },
            success: function(response){
                const municipio = $('#id_municipio').empty();
                municipio.append(`<option value="">---------</option>`);
                $.each(response, function(i, o){
                    municipio.append(`<option value="${o.id}">${o.name}</option>`);
                })
            }
        })
        
    })
})