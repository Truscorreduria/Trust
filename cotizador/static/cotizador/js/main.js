function activar_spinner() {
    $('#spinner').css('display', 'block');
}


function desactivar_spinner() {
    $('#spinner').css('display', 'none');
}


function intcommas(x) {
    x = x.toString();
    let pattern = /(-?\d+)(\d{3})/;
    while (pattern.test(x))
        x = x.replace(pattern, "$1,$2");
    return x;
}


function getParameter(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    let regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

const DataTableLang = function () {
    return {
        "sProcessing": "Procesando...",
        "sLengthMenu": "Mostrar _MENU_ registros",
        "sZeroRecords": "No se encontraron resultados",
        "sEmptyTable": "Ningún dato disponible en esta tabla",
        "sInfo": "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
        "sInfoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
        "sInfoFiltered": "(filtrado de un total de _MAX_ registros)",
        "sInfoPostFix": "",
        "sSearch": "Buscar:",
        "sUrl": "",
        "sInfoThousands": ",",
        "sLoadingRecords": "Cargando...",
        "oPaginate": {
            "sFirst": "Primero",
            "sLast": "Último",
            "sNext": "Siguiente",
            "sPrevious": "Anterior"
        },
        "oAria": {
            "sSortAscending": ": Activar para ordenar la columna de manera ascendente",
            "sSortDescending": ": Activar para ordenar la columna de manera descendente"
        }
    };
};

(function ($) {
    $(document).ready(function () {

        $(document)
            .ajaxStart(function () {
                activar_spinner();
            })
            .ajaxStop(function () {
                desactivar_spinner();
            });

        const menu_button = function () {
            $('.menu-ul').toggleClass('collapse')
        };

        $('.menu-button').on('click', menu_button);

        // $('.flexslider').flexslider({
        //     animation: "slide"
        // });

        $('.menu-ul li a[class!="active"]').mouseenter(function () {
            $(this).find('div.menu-bar')[0].style.animation = "activar .5s forwards"
        }).mouseleave(function () {
            $(this).find('div.menu-bar')[0].style.animation = "desactivar .5s forwards"
        });

        $('body').on('keyup', 'input:not([type="password"])', function () {
            _val = this.value;
            if (_val) {
                $(this).val(_val.toUpperCase());
            }
        });

        // $(window).on('resize', function () {
        //     alert("resize");
        //     $('.flexslider').flexslider({
        //         animation: "slide"
        //     });
        // })
    });
})(jQuery);

