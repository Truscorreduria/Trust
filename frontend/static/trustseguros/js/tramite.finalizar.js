$(document).ready(function () {
    $(document).on('click', '#btn-finish', function () {
        $.ajax('.', {
            method: "POST",
            data: {
                finalizar: 'finalizar',
                id: $('input[name="id"]').val()
            },
            success: function (response) {
                redraw_object(response);
            }
        })
    })
});