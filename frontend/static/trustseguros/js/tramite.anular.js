$(document).ready(function () {
    $(document).on('click', '#btn-null', function () {
        $.ajax(".", {
            method: "POST",
            data: {
                pk: $('input[name="pk"]').val(), cancelar: 'cancelar'
            }, success: function (response) {
                redraw_object(response);
            }
        })
    });
});