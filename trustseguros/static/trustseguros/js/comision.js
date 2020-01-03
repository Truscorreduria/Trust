(function ($) {
    $(document).ready(function () {
        $('#id_comision').on('change', function () {
            value = $(this).val();
            if (value > 30.0){
                $(this).val(30.0)
            }
            if (value < 0){
                $(this).val(0.0)
            }
        })
    })
})(grp.jQuery);