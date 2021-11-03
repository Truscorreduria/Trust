$(document).ready(function () {

    const uploadFile = function (file) {
        const data = new FormData();
        data.append('file', file);
        data.append('new', 'new');
        data.append('app_label', 'backend');
        data.append('model', 'cliente');
        data.append('pk', $('input[name="pk"]').val());
        $.ajax($ajax_soporte, {
            type: "POST",
            data: data,
            processData: false,
            contentType: false,
            success: function (response) {
                $('#documentos-list').append(response.html);
                $('.dateinput').datepicker({
                    dateFormat: 'dd/mm/yy',
                });
            }
        })
    };

    $(document).on('change', '#documentos-files', function () {
        $.each(this.files, function (i, file) {
            uploadFile(file);
        })
    });

    $(document).on('change', 'input[name="fecha_caducidad"]', function () {
        const _this = $(this);
        $.ajax($ajax_soporte, {
            method: 'POST',
            data: {
                'id': _this.data('id'),
                'fecha': _this.val(),
                'update': 'update',
            },
            success: function (response) {
                console.log(response)
            }
        })
    });

    $(document).on('change', 'select[name="tipo_doc"]', function () {
        const _this = $(this);
        $.ajax($ajax_soporte, {
            method: 'POST',
            data: {
                'id': _this.data('id'),
                'tipo_doc': _this.val(),
                'update': 'update',
            },
            success: function (response) {
                console.log(response)
            }
        })
    });
});