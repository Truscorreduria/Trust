(function ($) {
    $(document).ready(function () {
        $('a.sugerencia').on('click', function () {
            const _this = $(this);
            $.ajax('/admin/ajax/object_execute/', {
                method: "POST",
                data: {
                    app_label: 'migracion', model: _this.data('model'), id: _this.data('id'),
                    view: 'asignar', em: _this.data('em')
                },
                success: function (response) {
                    location.reload()
                }
            })
        })
    })
})(grp.jQuery)