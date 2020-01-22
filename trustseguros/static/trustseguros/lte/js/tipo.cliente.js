$(document).ready(function () {

    const tipo_cliente = function () {
        const personaNatural = $('#persona-natural');
        const personaJuridica = $('#persona-juridica');
        const _this = $(this);
        if (_this.val() === '1') {
            personaJuridica.css('display', 'none');
            personaNatural.css('display', 'flex');
        }
        if (_this.val() === '2') {
            personaNatural.css('display', 'none');
            personaJuridica.css('display', 'flex');
        }
    };

    $(document).on('change', '#id_tipo_cliente', tipo_cliente);
    $(document).on('focusin', '#id_tipo_cliente', tipo_cliente);
});

