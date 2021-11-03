$(document).ready(function () {
    $(document).on('click', '#btn-finish', function () {
        $.ajax('.', {
            method: "POST",
            data: {
                finalizar: 'finalizar',
                pk: $('input[name="pk"]').val()
            },
            success: function (response) {
                redraw_object(response);
            }
        })
    })
});