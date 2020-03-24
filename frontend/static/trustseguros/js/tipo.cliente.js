(function ($) {
    $(document).ready(function () {
        const personaNatural = $('.fields-persona-natural');
        const personaJuridica = $('.fields-persona-juridica');

        personaNatural.css('display', 'none');
        personaJuridica.css('display', 'none');

        const tipo_cliente = function () {
            _this = $('#id_tipo');
            if ($(_this).val() === '1') {
                personaJuridica.css('display', 'none');
                personaNatural.css('display', 'block');
            }
            if ($(_this).val() === '2') {
                personaNatural.css('display', 'none');
                personaJuridica.css('display', 'block');
            }
        };

        $('#id_tipo').on('change', tipo_cliente);
        tipo_cliente();
    })
})(grp.jQuery);