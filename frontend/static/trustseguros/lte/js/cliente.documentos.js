$(document).ready(function () {

    const uploadFile = function (file) {
        const data = new FormData();
        data.append('file', file);
        data.append('new', 'new');
        data.append('app_label', 'backend');
        data.append('model', 'cliente');
        data.append('id', $('input[name="id"]').val());
        $.ajax($ajax_soporte, {
            type: "POST",
            data: data,
            processData: false,
            contentType: false,
            success: function (response) {
                $('#documentos-list').append(`
                            <tr>
                                <td> <a href="${response.archivo.archivo}" target="_blank"><i class="fa fa-eye"></i></a> ${response.archivo.nombre}</td>
                                <td>${response.archivo.created_user.username}</td>
                                <td>${response.archivo.updated}</td>
                                <td>
                                    <input type="text" name="fecha_caducidad" class="form-control dateinput" 
                                    data-id="${response.archivo.id}">
                                </td>
                                <td style="text-align: center;">
                                    <button type="button" class="btn btn-danger btn-table-delete" data-id="${response.archivo.id}">
                                        <span class="fa fa-trash"></span>
                                    </button>
                                </td>
                            </tr>
                        `);


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
    })
});