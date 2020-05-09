"{% load static %}"


$(document).ready(function () {
        const imprimir_sepelio = function () {
            let fdata = new FormData();
            fdata.append('orden', $(this).data('orden'));
            const xhr = new XMLHttpRequest();
            xhr.open('POST', "{% url 'cotizador:print_orden_trabajo_sepelio' %}", true);
            xhr.responseType = 'blob';
            xhr.onload = function (e) {
                desactivar_spinner();
                if (parseInt(this.status) === 200) {
                    let blob = new Blob([this.response], {type: 'application/pdf'});
                    let link = document.createElement('a');
                    link.href = window.URL.createObjectURL(blob);
                    link.download = "Orden de Trabajo.pdf";
                    link.click();
                } else {
                    swal({
                            title: 'Ooops Ha ocurrido un Error!',
                            text: 'Por que ha ocurrido esto?',
                            imageUrl: "{% static 'cotizador/images/trusty/error.png' %}"
                        }
                    )
                }
            };
            xhr.send(fdata);
        };

        const calcular_cuota = function () {
            let total = parseFloat($('#poliza-total').val());
            $('#h2-anual').html(intcommas(parseFloat(total).toFixed(2)));
            let numero_cuotas = parseFloat($('#cantidad_cuotas').val());
            $('#h2-mensual').html(intcommas(parseFloat(total / numero_cuotas).toFixed(2)));
            $('#valor-cuota').val((total / numero_cuotas).toFixed(2));

        };

        function optionCuota(cuotas) {
            return (`<option value="${cuotas}">${cuotas}</option>`)
        };

        $('body').on('click', '.imprimir-sepelio', imprimir_sepelio);

        const cambio_beneficiario_sepelio = function () {
            swal({
                title: '<strong>Pasos para cambio de beneficiario</strong>',
                html: 'Por favor imprima el documento que se acaba de descargar, completelo con toda la informacion requerida, firme igual que su cedula y entregue el formato con copia de su cedula al area de seguros del banco.',
                showCloseButton: true,
                showCancelButton: false,
                focusConfirm: false,
                confirmButtonText: 'Aceptar',
                imageUrl: "{% static 'cotizador/images/trusty/exito.png' %}"
            }).then(function () {
                window.location = "{% url 'cotizador:download' %}?file_name=sepelio_SOLICITUD_PARA_CAMBIO_DE_BENEFICIARIOS.pdf";
            });
        };

        $('body').on('click', '.cambiar-beneficiario-sepelio', cambio_beneficiario_sepelio);

        const imprimir_cambio_vida = function () {
            swal({
                title: '<strong>Pasos para actualizar beneficiario</strong>',
                html: 'Por favor imprima el documento que se acaba de descargar, completelo con toda la informacion requerida, firme igual que su cedula y entregue el formato con copia de su cedula al area de seguros del banco.',
                showCloseButton: true,
                showCancelButton: false,
                focusConfirm: false,
                confirmButtonText: 'Aceptar',
                imageUrl: "{% static 'cotizador/images/trusty/exito.png' %}"
            }).then(function () {
                window.location = "{% url 'cotizador:download' %}?file_name=vida_INI_085-CAMBIO_DE_BENEFICIARIO.pdf";
            });
        };

        $('body').on('click', '.cambiar-beneficiario', imprimir_cambio_vida);

        const imprimir_vida = function () {
            window.location = "{% url 'cotizador:download' %}?file_name=vida_COBERTURAS_EMPLEADO_BANPRO.pdf";
        };

        $('body').on('click', '.imprimir-vida', imprimir_vida);

        const imprimir_accidente = function () {
            let fdata = new FormData();
            fdata.append('orden', $(this).data('orden'));
            const xhr = new XMLHttpRequest();
            xhr.open('POST', "{% url 'cotizador:print_orden_trabajo_accidente' %}", true);
            xhr.responseType = 'blob';
            xhr.onload = function (e) {
                desactivar_spinner();
                if (parseInt(this.status) === 200) {
                    let blob = new Blob([this.response], {type: 'application/pdf'});
                    let link = document.createElement('a');
                    link.href = window.URL.createObjectURL(blob);
                    link.download = "Orden de Trabajo.pdf";
                    link.click();
                } else {
                    swal({
                            title: 'Ooops Ha ocurrido un Error!',
                            text: 'Por que ha ocurrido esto?',
                            imageUrl: "{% static 'cotizador/images/trusty/error.png' %}"
                        }
                    )
                }
            };
            xhr.send(fdata);
        };

        $('body').on('click', '.imprimir-accidente', imprimir_accidente);

        const imprimir_auto = function () {
            let fdata = new FormData();
            fdata.append('id', $(this).data('poliza'));
            const xhr = new XMLHttpRequest();
            xhr.open('POST', $(this).data('url'), true);
            let filename = $(this).data('filename');
            xhr.responseType = 'blob';
            xhr.onload = function (e) {
                desactivar_spinner();
                if (parseInt(this.status) === 200) {
                    let blob = new Blob([this.response], {type: 'application/pdf'});
                    let link = document.createElement('a');
                    link.href = window.URL.createObjectURL(blob);
                    link.download = filename;
                    link.click();
                } else {
                    swal({
                            title: 'Ooops Ha ocurrido un Error!',
                            text: 'Por que ha ocurrido esto?',
                            imageUrl: "{% static 'cotizador/images/trusty/error.png' %}"
                        }
                    )
                }
            };
            xhr.send(fdata);
        };

        $('body').on('click', '.imprimir-auto', imprimir_auto);

        const baja_auto = function () {

            const _this = $(this);
            $.ajax("{% url 'ajax_getObject' %}", {
                method: "POST",
                data: {
                    app_label: 'backend', model: 'poliza',
                    id: $(_this).data('poliza')
                },
                success: function (response) {
                    $('#poliza').val(response.id);
                    $('#marca').val(response.marca);
                    $('#modelo').val(response.modelo);
                    $('#anno').val(response.anno);
                    $('#chasis').val(response.chasis);
                    $('#motor').val(response.motor);
                    $('#placa').val(response.placa);
                    $('#modal-baja-auto').modal('show');
                }
            });
        };

        const renovar_auto = function () {
            const _this = $(this);
            $.ajax("{% url 'ajax_getObject' %}", {
                method: "POST",
                data: {
                    app_label: 'backend', model: 'poliza',
                    id: _this.data('poliza')
                },
                success: function (response) {
                    console.log(response);
                    $('#modal-renovacion').modal('show');
                    $('#poliza-renovacion').val(response.id);
                    $('#poliza-total').val(response.total);
                    calcular_cuota()
                }
            });

        };

        const baja = function () {

            const _this = $(this);
            let model = undefined;
            if ($(_this).data('type') === 'CF') {
                model = 'bensepelio';
            }
            if ($(_this).data('type') === 'AP') {
                model = 'benaccidente';
            }
            $.ajax("{% url 'ajax_getObject' %}", {
                method: "POST",
                data: {
                    app_label: 'backend', model: model,
                    id: $(_this).data('beneficiario')
                },
                success: function (response) {
                    $('#beneficiario-baja').val(response.id);
                    $('#beneficiario-tipo').val(response.model);
                    $('#primer_nombre').val(response.primer_nombre);
                    $('#segundo_nombre').val(response.segundo_nombre);
                    $('#apellido_paterno').val(response.apellido_paterno);
                    $('#apellido_materno').val(response.apellido_materno);
                    $('#parentesco').val(response.parentesco);
                    $('#fecha_nacimiento').val(response.fecha_nacimiento);
                    $('#modal-baja').modal('show');
                }
            });
        };

        $('body').on('click', '.baja', baja);
        $('body').on('click', '.baja-auto', baja_auto);
        $('body').on('click', '.btn-renovacion', renovar_auto);

        $('#form-baja').on('submit', function (e) {

            e.preventDefault();
            $('#modal-baja').modal('hide');
            swal({
                title: '<strong>¿Estas seguro?</strong>',
                html: 'Esta acción no se puede revertir. Tendrías que hacer una inclusión nueva.',
                showCloseButton: true,
                showCancelButton: true,
                focusConfirm: false,
                confirmButtonText: 'SI',
                cancelButtonText: 'NO',
                imageUrl: "{% static 'cotizador/images/trusty/pregunta.png' %}"
            }).then(function () {
                $.ajax("{% url 'cotizador:solicitar_baja' %}", {
                    method: "POST",
                    data: {
                        beneficiario: $('#beneficiario-baja').val(),
                        tipo: $('#beneficiario-tipo').val()
                    },
                    success: function (response) {
                        $('#modal-baja').modal('hide');
                        console.log(response);
                        swal({
                            title: 'Tu solicitud ha sido ingresada.',
                            html: 'Seras dirigido al area de contacto, en donde podras ver el estado de la gestión. Tu número de Ticket es ' + response.ticket.code,
                            imageUrl: "{% static 'cotizador/images/trusty/exito.png' %}"
                        }).then(function () {
                            location.href = "{% url 'cotizador:contactanos' %}"
                        });


                    }
                })
            });
        });

        $('#form-baja-auto').on('submit', function (e) {

            e.preventDefault();
            $('#modal-baja').modal('hide');
            swal({
                title: '<strong>¿Estas seguro?</strong>',
                html: 'Esta acción no se puede revertir.',
                showCloseButton: true,
                showCancelButton: true,
                focusConfirm: false,
                confirmButtonText: 'SI',
                cancelButtonText: 'NO',
                imageUrl: "{% static 'cotizador/images/trusty/pregunta.png' %}"
            }).then(function () {
                $.ajax("{% url 'cotizador:solicitar_baja_auto' %}", {
                    method: "POST",
                    data: {
                        poliza: $('#poliza').val(),
                    },
                    success: function (response) {
                        $('#modal-baja').modal('hide');
                        console.log(response);
                        swal({
                            title: 'Tu solicitud ha sido ingresada.',
                            html: 'Seras dirigido al area de contacto, en donde podras ver el estado de la gestión. Tu número de Ticket es ' + response.ticket.code,
                            imageUrl: "{% static 'cotizador/images/trusty/exito.png' %}"
                        }).then(function () {
                            location.href = "{% url 'cotizador:contactanos' %}"
                        });


                    }
                })
            });
        });


        $('input[name="medio-pago"]').on('change', function () {
            $('.zona-debito').css('display', 'none');
            $('.zona-deduccion').css('display', 'none');
            $('.zona-deposito').css('display', 'none');
            $('#group-autoriza-banpro').css('display', 'none');
            $('#custom-radio-pago-mensual').css('display', 'none');
            const $cantidadCuotas = $('#cantidad_cuotas').empty();
            var valor = $(this).val();
            if (valor == 'debito_automatico') {
                $('.zona-debito').css('display', 'flex');
                $('#custom-radio-pago-mensual').css('display', 'block');
                $('#autoriza-banpro').removeAttr('required');
                $('#name').attr('required', 'required');
                $('#number').attr('required', 'required');
                $('#expiry').attr('required', 'required');
                $('#cuotas-text').html("En cuotas mensuales");
                for (let i = 2; i <= 12; i++) {
                    $cantidadCuotas.append(optionCuota(i));
                }
            } else if (valor == 'deduccion_nomina') {
                $('.zona-deduccion').css('display', 'flex');
                $('#custom-radio-pago-mensual').css('display', 'block');
                $('#group-autoriza-banpro').css('display', 'block');
                $('#autoriza-banpro').attr('required', 'required');
                $('#name').removeAttr('required');
                $('#number').removeAttr('required');
                $('#expiry').removeAttr('required');
                $('#cuotas-text').html("En cuotas quincenales")
                for (let i = 2; i <= 24; i++) {
                    $cantidadCuotas.append(optionCuota(i));
                }
            } else if (valor == 'deposito_referenciado') {
                $('.zona-deposito').css('display', 'flex');
                $('#autoriza-banpro').removeAttr('required');
                $('#name').removeAttr('required');
                $('#number').removeAttr('required');
                $('#expiry').removeAttr('required');
            }
            calcular_cuota()
        });

        $('input[name="forma-pago"]').on('change', function () {
            if ($(this).val() === "mensual") {
                $('#cantidad_cuotas').removeAttr('disabled');
            } else {
                $('#cantidad_cuotas').attr('disabled', 'disabled');
            }
        });

        $('#cantidad_cuotas').on('change', calcular_cuota);

        $('#form-renovacion').on('submit', function (e) {
            e.preventDefault();
            let data = new FormData(this);
            $.ajax("{% url 'cotizador:solicitud_renovacion_auto' %}", {
                method: "POST",
                data: data,
                processData: false,
                contentType: false,
                success: function (response) {
                    $('#modal-renovacion').modal('hide');
                }
            })

        })

    }
);