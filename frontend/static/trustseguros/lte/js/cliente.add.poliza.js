function add_poliza() {
    Swal.fire({
        imageUrl: "{% static 'cotizador/images/trusty/pregunta.png' %}",
        title: 'Estas seguro?',
        text: "Esta acción generará una póliza en estado pendiente para este cliente.",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Si',
        cancelButtonText: 'No'
    }).then((result) => {
        if (result.value) {
            $.ajax("/trustseguros/polizas/", {
                method: "POST",
                data: {
                    customer: $('input[name="id"]').val(), add_from_customer: 'add_from_customer'
                }, success: function (response) {
                    window.location.assign("/trustseguros/polizas/#" + response.id);
                }
            });
        } else {
            $('.btn-perform').removeAttr('disabled')
        }
    });
}