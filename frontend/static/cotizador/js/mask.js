(function ($) {
    $(document).ready(function () {
        $('.mask-only-text').mask('Z', {
            translation: {
                'Z': {pattern: /[a-zA-ZáéíóúñÑ ]/, recursive: true}
            }
        });

        $('.mask-card-expire').mask('00 / 00', {reverse: true});

        $('.mask-card-number').mask('0000 0000 0000 0000', {reverse: true});

        $('.mask-chasis').mask('AAAAAAAAAAAAAAAAA');

        $('.mask-motor').mask('AAAAAAAAAAAAAAAAA');

        const options = {
            onKeyPress: function (cep, e, field, options) {
                const masks = ['00000000', '00000000'];
                const mask = (cep.length > 7) ? masks[1] : masks[0];
                $('.crazy_cep').mask(mask, options);
            }
        };

        $('.mask-celular').inputmask('9{8,8}', { clearIncomplete: true, greedy: false });

        $('.mask-cedula').inputmask('9{13,13}A', { clearIncomplete: true, greedy: false });
    });
})(jQuery);