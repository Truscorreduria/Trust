$(document).ready(function () {
    $(document).on('click', '#btn-null', function () {
        $.ajax(".", {
            method: "POST",
            data: {
                id: $('input[name="id"]').val(), cancelar: 'cancelar'
            }, success: function (response) {
                redraw_object(response);
            }
        })
    });
});