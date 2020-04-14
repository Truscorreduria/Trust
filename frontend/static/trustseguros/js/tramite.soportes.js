$(document).ready(function () {

    const uploadFile = function (file) {
        const data = new FormData();
        data.append('file', file);
        data.append('new', 'new');
        data.append('app_label', 'backend');
        data.append('model', 'tramite');
        data.append('id', $('input[name="id"]').val());
        $.ajax($ajax_soporte, {
            type: "POST",
            data: data,
            processData: false,
            contentType: false,
            success: function (response) {
                $('#drive-list').append(`
                            <tr>
                                <td> <a href="${response.archivo.archivo}" target="_blank"><i class="fa fa-eye"></i></a> ${response.archivo.nombre}</td>
                                <td>${response.archivo.created_user.username}</td>
                                <td>${response.archivo.updated}</td>
                                <td style="text-align: center;">
                                    <button type="button" class="btn btn-danger btn-table-delete" data-id="${ response.archivo.id }">
                                        <span class="fa fa-trash"></span>
                                    </button>
                                </td>
                            </tr>
                        `);
            }
        })
    };

    $(document).on('change', '#drive-files', function () {
        uploadFile(this.files[0]);
    });
});