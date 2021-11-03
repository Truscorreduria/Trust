$(document).ready(function () {
    $(document).on('click', '#bitacorabtn-add-comment', function () {
        let comment = $('#bitacora-comentario-input').val();
        if (comment.length > 0) {
            $.ajax($ajax_bitacora, {
                method: "post",
                data: {
                    new: 'new', comentario: comment,
                    app_label: 'backend', model: 'siniestrotramite',
                    id: $('input[name="pk"]').val()
                },
                success: function (response) {
                    $('#bitacora-table').prepend(`
                                <tr>
                                    <td colspan="2">${response.instance.comentario}</td>
                                    <td>${response.instance.created_user.username}</td>
                                    <td>${response.instance.created}</td>
                                </tr>
                            `);
                    $('#bitacora-comentario-input').val('')
                }
            })
        }
    });
})