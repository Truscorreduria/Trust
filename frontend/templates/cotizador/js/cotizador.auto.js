"{% load static %}"


function option_municipio(municipio) {
    return (`
            <option value="${municipio.id}">${municipio.name}</option>
            `)
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


async function go_top() {
    await sleep(300);
    $("#modal-auto").scrollTop(0);
}


$(document).ready(function () {

    const $overlay = document.querySelector('.help-overlay');
    const $modal = document.querySelector('.help-modal');
    const $modal_content = document.querySelector('.help-modal-content');
    const tag_departamento = $('#departamento');
    const tag_municipio = $('#municipio');

    tag_departamento.on('change', function () {
        $.ajax("{% url 'ajax_getCollection' %}", {
            method: "POST",
            data: {
                app_label: 'utils',
                model: 'municipio',
                filters: "{'departamento_id': " + tag_departamento.val() + "}"
            },
            success: function (response) {
                tag_municipio.empty();
                $.each(response, function (i, o) {
                    tag_municipio.append($(option_municipio(o)));
                })
            }
        })
    });
    {% if user.profile.departamento and user.profile.municipio %}
    tag_departamento.val("{{ user.profile.departamento.id }}");

    $.ajax("{% url 'ajax_getCollection' %}", {
        method: "POST",
        data: {
            app_label: 'utils',
            model: 'municipio',
            filters: "{'departamento_id': " + tag_departamento.val() + "}"
        },
        success: function (response) {
            tag_municipio.empty();
            $.each(response, function (i, municipio) {
                tag_municipio.append($(option_municipio(municipio)));
            });
            tag_municipio.val("{{ user.profile.municipio.id }}")
        }
    });

    {% endif %}

    function showModal(content) {
        $overlay.classList.add('active');
        $modal_content.innerHTML = content;
        $modal.style.animation = 'modalIn .8s forwards';
    }

    $('.tip-help').on('click', function () {
        showModal($(this).data('title'));
    });

    document.querySelector('.help-modal-btn').addEventListener('click', function hideModal() {
        $overlay.classList.remove('active');
        $modal.style.animation = 'modalOut .8s forwards';
    });

    const cotizar_auto = function () {
        $('#modal-auto').modal('show');
    };

    const cotizar_sepelio = function () {
        $('#modal-sepelio').modal('show');
    };

    const cotizar_accidente = function () {
        $('#modal-accidente').modal('show');
    };

    $('#option-auto').on('click', cotizar_auto);
    $('#option-sepelio').on('click', cotizar_sepelio);
    $('#option-accidente').on('click', cotizar_accidente);

    const cargar_annos = function () {
        var anno = $('#anno').val();
        $.ajax("{% url 'cotizador:get_annos' %}", {
            method: "POST",
            data: {marca: $('#marca').val()},
            success: function (response) {
                var select = $('#anno').empty();
                $.each(response, function (i, o) {
                    var option = $('<option></option>')
                        .val(o)
                        .html(o);
                    if (o == anno) {
                        $(option).attr('selected', "");
                    }
                    select.append(option);
                });
                cargar_modelos();
                //calcular();
            }
        });
    };

    const cargar_modelos = function () {
        var modelo = $('#modelo').val();
        $.ajax("{% url 'cotizador:get_modelos' %}", {
            method: "POST",
            data: {marca: $('#marca').val(), anno: $('#anno').val()},
            success: function (response) {
                var select = $('#modelo').empty();
                $.each(response, function (i, o) {
                    var option = $('<option></option>')
                        .val(o)
                        .html(o);
                    if (o == modelo) {
                        $(option).attr('selected', "");
                    }
                    select.append(option);
                });
                calcular();
            }
        });
    };

    $('#marca').on('change', cargar_annos);
    $('#anno').on('change', cargar_modelos);

    function deducible(porcentaje, minimo) {
        return (`${porcentaje} Mínimo U$ ${minimo}`)
    }

    const calcular_cuota = function () {
        let tipo_cobertura = $('#tipo-cobertura').val();
        if (tipo_cobertura === '2') {
            var total = parseFloat($('#total-pagar').val());
        } else {
            var total = parseFloat($('#total-pagar-basica').val());
        }
        $('#h2-anual').html(intcommas(parseFloat(total).toFixed(2)));
        let numero_cuotas = parseFloat($('#cantidad_cuotas').val());
        $('#h2-mensual').html(intcommas(parseFloat(total / numero_cuotas).toFixed(2)));
        $('#valor-cuota').val((total / numero_cuotas).toFixed(2));

    };

    const calcular = function () {
        let m = $('#marca').val();
        let mo = $('#modelo').val();
        let year = $('#anno').val();
        let chasis = $('#chasis').val();
        let exceso = $('#select-exceso').val();
        $.ajax("{% url 'cotizador:get_data' %}", {
            method: "POST",
            data: {marca: m, modelo: mo, anno: year, exceso: exceso, chasis: chasis},
            success: function (response) {
                //console.log(response);
                let porcentaje = response.porcentaje;
                let minimo = parseFloat(response.minimo_deducible).toFixed(2);
                let porcentaje_extension = response.porcentaje_extension;
                let minimo_extension = parseFloat(response.minimo_deducible_extension).toFixed(2);
                $('#valor_nuevo').val(response.valor_nuevo.valor);
                $('#porcentaje-deducible').val(response.porcentaje_deducible);
                $('#porcentaje-deducible-extension').val(response.porcentaje_deducible_extension);
                $('#minimo-deducible').val(response.minimo_deducible);
                $('#minimo-deducible-extension').val(response.minimo_deducible_extension);
                $('#deducible-rotura-vidrios').val(response.deducible_rotura_vidrios);
                $('#monto-exceso').val(exceso);
                $('#costo-exceso').val(response.exceso);
                $.each($('td.deducible'), function (i, o) {
                    $(o).html(deducible(porcentaje, minimo))
                });
                $.each($('td.deducible-territorial'), function (i, o) {
                    $(o).html(deducible(porcentaje_extension, minimo_extension))
                });
                $('td.deducible-rotura-vidrios').html(response.deducible_rotura_vidrios.toFixed(2));
                let r4s = $('#r4-sum');
                let r4t = $('#r4-total');
                let r5s = $('#r5-sum');
                let r6s = $('#r6-sum');
                let r7s = $('#r7-sum');
                let r12t = $('#r12-total');
                let r13s = $('#r13-sum');
                let r14s = $('#r14-sum');
                $('#span-marca').html(response.valor_nuevo.marca);
                $('#span-modelo').html(response.valor_nuevo.modelo);
                $('#span-anno').html(year);
                $('#span-marca-basica').html(response.valor_nuevo.marca);
                $('#span-modelo-basica').html(response.valor_nuevo.modelo);
                $('#span-anno-basica').html(year);
                // $('#span-anno').html(year + " - " + response.valor_nuevo.valor);
                //$('#span-nuevo').html( + ' - ' + response.valor_nuevo.anno + ' - ' + response.valor_nuevo.chasis);
                $(r4s).val(response.suma_asegurada).trigger('change');
                $(r4s).parent().find('span').html(intcommas(parseFloat(response.suma_asegurada).toFixed(2)));
                $(r4t).val(response.prima).trigger('change');
                $(r4t).parent().find('span').html(intcommas(parseFloat(response.prima).toFixed(2)));
                $(r5s).val(response.vidrios).trigger('change');
                $(r5s).parent().find('span').html(intcommas(parseFloat(response.vidrios).toFixed(2)));
                $(r6s).val(response.suma_asegurada).trigger('change');
                $(r6s).parent().find('span').html(intcommas(parseFloat(response.suma_asegurada).toFixed(2)));
                $(r7s).val(response.suma_asegurada).trigger('change');
                $(r7s).parent().find('span').html(intcommas(parseFloat(response.suma_asegurada).toFixed(2)));
                $(r12t).val(response.exceso).trigger('change');
                $(r12t).parent().find('span').html(intcommas(parseFloat(response.exceso).toFixed(2)));
                $(r13s).val(exceso * 2).trigger('change');
                $(r13s).parent().find('span').html(intcommas(parseFloat(exceso * 2).toFixed(2)));
                $(r14s).val(exceso).trigger('change');
                $(r14s).parent().find('span').html(intcommas(parseFloat(exceso).toFixed(2)));
                let prima_total = $('#prima-total');
                $(prima_total).val(response.prima_total);
                $(prima_total).parent().find('span').html(intcommas(parseFloat(response.prima_total).toFixed(2)));
                let emision = $('#derecho-emision');
                $(emision).val(response.emision);
                $(emision).parent().find('span').html(intcommas(parseFloat(response.emision).toFixed(2)));
                let iva = $('#iva');
                $(iva).val(response.iva);
                $(iva).parent().find('span').html(intcommas(parseFloat(response.iva).toFixed(2)));
                let total = $('#total-pagar');
                $(total).val(response.total);
                $(total).parent().find('span').html('U$ ' + intcommas(parseFloat(response.total).toFixed(2)));

                let step = $('.nav-item.active').find('a').attr('href');
                if (step === '#step-2' && response.chasis_encontrado === true) {
                    swal({
                        title: "!Chasis encontrado¡",
                        text: "El número de chasis de tu vehículo ya se encuentra registrado. Hemos corregido la cotización en base al valor nuevo de tu vehículo. Tu nuevo total a pagar es " + intcommas((response.total).toFixed(2)),
                        imageUrl: "{% static 'cotizador/images/trusty/cool.png' %}"
                    })
                };
                /*const $cantidadCuotas = $('#cantidad_cuotas').empty();
                if ($('#tipo-cobertura').val() === '1') {
                    for (let i = 2; i <= 12; i++) {
                        $cantidadCuotas.append(optionCuota(i));
                    }
                } else {
                    for (let i = 2; i <= 24; i++) {
                        $cantidadCuotas.append(optionCuota(i));
                    }
                }*/

                calcular_cuota();


            }
        })
    };

    $('#chasis').on('change', calcular);

    $('#select-exceso').on('change', calcular);

    $('#cantidad_cuotas').on('change', calcular_cuota);

    const tipofile = function () {
        if ($(this).val() == 'si') {
            $('#file-carta')
                .removeAttr('required')
                .parent().css('display', 'none');
        } else if ($(this).val() == 'no') {
            $('#file-carta')
                .attr('required', 'required')
                .parent().css('display', 'block');
        }
    };

    const tipocesion = function () {
        if ($(this).val() == 'si') {
            $('#entidad')
                .attr('required', 'required')
                .parent().css('display', 'block');
        } else if ($(this).val() == 'no') {
            $('#entidad')
                .removeAttr('required')
                .parent().css('display', 'none');
        }
    };

    const tipodanno = function () {
        if ($(this).val() == 'si') {
            $('#danno_descripcion')
                .attr('required', 'required')
                .parent().css('display', 'block');
        } else if ($(this).val() == 'no') {
            $('#danno_descripcion')
                .removeAttr('required')
                .parent().css('display', 'none');
        }
    };

    const select_color = function () {
        if ($(this).val() === 'OTRO') {
            $('#group-color-otro').css('display', 'block');
        } else {
            $('#group-color-otro').css('display', 'none');
        }
    };

    $('#color').on('change', select_color);

    $('#status-circulacion').on('change', tipofile);
    $('#cesion-derecho').on('change', tipocesion);
    $('#danno').on('change', tipodanno);

    function optionCuota(cuotas) {
        return (`<option value="${cuotas}">${cuotas}</option>`)
    }

    $('.nav-link').on('click', function () {
        var valor = $(this).attr('href').replace('#', '');
        $('#tipo-cobertura').val(valor);
        if (valor == '1') {
            $('#card-cesion-derecho').css('display', 'none');
            $('#custom-radio-deposito-referenciado').css('display', 'none');
            $('#custom-radio-pago-mensual').css('display', 'block');
            $('#col-dannos').css('display', 'none');
            const $cantidadCuotas = $('#cantidad_cuotas').empty();
            for (let i = 2; i <= 12; i++) {
                $cantidadCuotas.append(optionCuota(i));
            }

        } else if (valor == '2') {
            $('#card-cesion-derecho').css('display', 'block');
            $('#custom-radio-deposito-referenciado').css('display', 'block');
            $('#custom-radio-pago-mensual').css('display', 'block');
            $('#col-dannos').css('display', 'block');
            const $cantidadCuotas = $('#cantidad_cuotas').empty();
            for (let i = 2; i <= 24; i++) {
                $cantidadCuotas.append(optionCuota(i));
            }

        }
        calcular_cuota();
    });

    $('.sin-registro a').on('click', function (e) {
        e.preventDefault();
        $('#modal-auto').modal('hide');
        $('#modal-manual').modal('show');
    });

    const generar_cotizacion = function () {
        activar_spinner();
        const data = new FormData();
        data.append('aseguradora', $('#aseguradora_id').val());
        data.append('fecha_emision', $('#fecha-emision').val());

        data.append('nombres', $('#nombres').val());
        data.append('apellidos', $('#apellidos').val());
        data.append('email', $('#email').val());
        data.append('cedula', $('#cedula').val());
        data.append('telefono', $('#telefono').val());
        data.append('celular', $('#celular').val());
        data.append('domicilio', $('#domicilio').html());

        data.append('anno', $('#anno').val());
        data.append('marca', $('#marca').val());
        data.append('modelo', $('#modelo').val());
        data.append('chasis', $('#chasis').val());
        data.append('motor', $('#motor').val());
        data.append('placa', $('#placa').val());
        data.append('color', $('#color').val());
        data.append('uso', $('#uso').val());
        data.append('valor_nuevo', $('#valor_nuevo').val());
        data.append('suma_asegurada', parseFloat($('#r4-sum').val()));
        data.append('prima_total', $('#prima-total').val());
        data.append('emision', $('#derecho-emision').val());
        data.append('iva', $('#iva').val());
        data.append('total_pagar', $('#total-pagar').val());
        data.append('forma_pago', $('input[name="forma-pago"]:checked').val());
        data.append('cuotas', $('#cantidad_cuotas').val());
        data.append('valor_cuota', $('#valor-cuota').val());
        data.append('porcentaje_deducible', $('#porcentaje-deducible').val());
        data.append('minimo_deducible', $('#minimo-deducible').val());
        data.append('porcentaje_deducible_extension', $('#porcentaje-deducible-extension').val());
        data.append('minimo_deducible_extension', $('#minimo-deducible-extension').val());
        data.append('deducible_rotura_vidrios', $('#deducible-rotura-vidrios').val());
        data.append('monto_exceso', $('#monto-exceso').val());
        data.append('costo_exceso', $('#costo-exceso').val());

        var file_cedula = document.getElementById('file-cedula');
        if (file_cedula.files[0]) {
            data.append('file_cedula', file_cedula.files[0])
        }
        var file_circulacion = document.getElementById('file-circulacion');
        if (file_circulacion.files[0]) {
            data.append('file_circulacion', file_circulacion.files[0])
        }
        var file_carta = document.getElementById('file-carta');
        if (file_carta.files[0]) {
            data.append('file_carta', file_carta.files[0])
        }
        var xhr = new XMLHttpRequest();
        xhr.open('POST', "{% url 'cotizador:generar_cotizacion' %}", true);
        xhr.responseType = 'blob';

        xhr.onload = function (e) {
            desactivar_spinner();
            if (this.status == 200) {
                var blob = new Blob([this.response], {type: 'application/pdf'});
                var link = document.createElement('a');
                link.href = window.URL.createObjectURL(blob);
                link.download = "Proforma.pdf";
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

        xhr.send(data);
    };

    $('#btn-cotizacion').on('click', generar_cotizacion);

    const btnCancel = $('<button></button>').text('Cancelar')
        .addClass('btn btn-danger')
        .on('click', function () {
            $('#smartwizard').smartWizard("reset");
        });

    const btnFinish = $('<button style="display: none;" id="btn-finish"></button>').text('Finalizar')
        .addClass('btn btn-info sw-btn-finish')
        .on('click', function () {
            const elmForm = $("#form-step-3");

            elmForm.validator('validate');
            const elmErr = $(elmForm).find('.has-error');
            if (elmErr && elmErr.length > 0) {
                return false;
            } else {
                activar_spinner();
                let data = new FormData();
                const card_number = $('#number');
                data.append('aseguradora', $('#aseguradora_id').val());
                data.append('fecha_emision', $('#fecha-emision').val());

                data.append('cambio_asegurado', $('input[name="cambio_asegurado"]:checked').val());
                data.append('primer_nombre', $('#id_primer_nombre').val());
                data.append('segundo_nombre', $('#id_segundo_nombre').val());
                data.append('apellido_paterno', $('#id_apellido_paterno').val());
                data.append('apellido_materno', $('#id_apellido_materno').val());
                data.append('cedula', $('#cedula').val());
                data.append('email', $('#email').val());
                data.append('telefono', $('#telefono').val());
                data.append('celular', $('#celular').val());
                data.append('domicilio', $('#domicilio').html());

                data.append('anno', $('#anno').val());
                data.append('marca', $('#marca').val());
                data.append('modelo', $('#modelo').val());
                data.append('chasis', $('#chasis').val());
                data.append('motor', $('#motor').val());
                data.append('circulacion', $('#circulacion').val());
                data.append('placa', $('#placa').val());
                data.append('color', $('#color').val());
                data.append('uso', $('#uso').val());
                data.append('valor_nuevo', $('#valor_nuevo').val());
                data.append('valor_depreciado', parseFloat($('#r4-sum').val()));
                data.append('prima_total', $('#prima-total').val());
                data.append('emision', $('#derecho-emision').val());
                data.append('iva', $('#iva').val());
                data.append('total_pagar', $('#total-pagar').val());
                data.append('forma_pago', $('input[name="forma-pago"]:checked').val());
                data.append('medio_pago', $('input[name="medio-pago"]:checked').val());
                data.append('cuotas', $('#cantidad_cuotas').val());
                data.append('valor_cuota', $('#valor-cuota').val());
                data.append('cesion_derecho', $('#cesion-derecho').val());
                data.append('entidad', $('#entidad').val());
                data.append('tipo_cobertura', $('#tipo-cobertura').val());
                data.append('moneda_cobro', $('#moneda-cobro').val());
                data.append('banco_emisor', $('#banco-emisor').val());
                data.append('card_number', card_number.val());
                data.append('card_expiry', $('#expiry').val());
                data.append('porcentaje_deducible', $('#porcentaje-deducible').val());
                data.append('minimo_deducible', $('#minimo-deducible').val());
                data.append('porcentaje_deducible_extension', $('#porcentaje-deducible-extension').val());
                data.append('minimo_deducible_extension', $('#minimo-deducible-extension').val());
                data.append('deducible_rotura_vidrios', $('#deducible-rotura-vidrios').val());
                data.append('monto_exceso', $('#monto-exceso').val());
                data.append('costo_exceso', $('#costo-exceso').val());

                if (card_number.hasClass('visa')) {
                    data.append('card_type', 'visa');
                }
                if (card_number.hasClass('amex')) {
                    data.append('card_type', 'amex');
                }
                if (card_number.hasClass('discover')) {
                    data.append('card_type', 'discover');
                }
                if (card_number.hasClass('jcb')) {
                    data.append('card_type', 'jcb');
                }
                if (card_number.hasClass('mastercard')) {
                    data.append('card_type', 'mastercard');
                }


                const file_cedula = document.getElementById('file-cedula');
                if (file_cedula.files) {
                    $.each(file_cedula.files, function (i, file) {
                        data.append('file_cedula', file)
                    });
                }
                const file_circulacion = document.getElementById('file-circulacion');
                if (file_circulacion.files) {
                    $.each(file_circulacion.files, function (i, file) {
                        data.append('file_circulacion', file)
                    });
                }
                const file_carta = document.getElementById('file-carta');
                if (file_carta.files) {
                    $.each(file_cedula.files, function (i, file) {
                        data.append('file_carta', file)
                    })
                }

                $.ajax("{% url 'cotizador:guardar_poliza' %}", {
                    type: "POST",
                    contentType: false,
                    processData: false,
                    cache: false,
                    data: data,
                    success: function (response) {
                        //activar_spinner();
                        let obj = new FormData();
                        obj.append('id', response.id);

                        const xhr_recibo = new XMLHttpRequest();
                        xhr_recibo.open('POST', "{% url 'cotizador:print_orden_trabajo' %}", true);
                        xhr_recibo.responseType = 'blob';
                        xhr_recibo.onload = function (e) {
                            if (parseInt(this.status) === 200) {
                                let blob = new Blob([this.response], {type: 'application/pdf'});
                                let link = document.createElement('a');
                                link.href = window.URL.createObjectURL(blob);
                                link.download = "Orden de Trabajo.pdf";
                                link.click();
                                $('#modal-auto').modal('hide');
                                swal({
                                        title: 'Muchas gracias por emitir su póliza con Trust Correduria.',
                                        text: 'En un máximo de 24 horas recibirá un correo electrónico notificandole que su póliza está lista. Podrá retirarlo en el área de seguros del Banco.',
                                        imageUrl: "{% static 'cotizador/images/trusty/exito.png' %}"
                                    }
                                ).then(function () {
                                    $(location).attr('href', "{% url 'cotizador:misseguros' %}")
                                });
                            } else {
                                swal({
                                    title: 'Ooops ha ocurrido un Error!',
                                    text: 'Por que ha ocurrido esto?',
                                    imageUrl: "{% static 'cotizador/images/trusty/error.png' %}"
                                })
                            }
                        };
                        xhr_recibo.send(obj);
                    }
                });


            }


        });

    $('#smartwizard').smartWizard({
        selected: 0,
        theme: 'dots',
        transitionEffect: 'slide',
        lang: {
            next: 'Siguiente',
            previous: 'Anterior'
        },
        toolbarSettings: {
            toolbarPosition: 'bottom',
            //toolbarExtraButtons: [btnFinish]
        },
        anchorSettings: {
            markDoneStep: true,
            markAllPreviousStepsAsDone: true,
            removeDoneStepOnNavigateBack: true,
            enableAnchorOnDoneStep: true
        },
        showStepURLhash: false,
        keyNavigation: false,
    })
        .on("leaveStep", function (e, anchorObject, stepNumber, stepDirection) {
            const elmForm = $("#form-step-" + stepNumber);
            if (stepDirection === 'forward' && elmForm) {
                elmForm.validator('validate');
                const elmErr = $(elmForm).find('.has-error');
                if (elmErr && elmErr.length > 0) {
                    return false;
                }
                if (parseInt(stepNumber) === 0) {
                    calcular();
                }
                if (parseInt(stepNumber) === 1) {
                    swal({
                        title: '<strong>Emitir Póliza</strong>',
                        html: '¿Desea contratar la póliza?',
                        showCloseButton: true,
                        showCancelButton: true,
                        focusConfirm: false,
                        confirmButtonText: 'SI',
                        cancelButtonText: 'NO',
                        imageUrl: "{% static 'cotizador/images/trusty/pregunta.png' %}"
                    }).then(function (result) {

                            if (result.value) {
                                $('#smartwizard').smartWizard('goToStep', 2);
                            } else {
                                $('#smartwizard').smartWizard('goToStep', 1);
                            }

                            go_top();
                        }
                    )
                }
                if (parseInt(stepNumber) === 2) {
                    $('#smartwizard .sw-btn-next').css('display', 'none');
                    btnFinish.css('display', 'block');
                }
            }

            if (stepDirection === 'backward' && elmForm) {
                $('.sw-btn-finish').css('display', 'none');
                $('.sw-btn-next').css('display', 'block');
            }

            return true;
        })
        .on("showStep", function (e, anchorObject, stepNumber, stepDirection) {
            // Enable finish button only on last step
            if (stepNumber === 1) {
                mostrar_notas();
            } else {
                ocultar_notas();
            }

            if (stepNumber === 2) {
                $("#modal-auto").scrollTop(0);
            }

            if (stepNumber === 3) {
                $('.btn-finish').removeClass('disabled');
            } else {
                $('.btn-finish').addClass('disabled');
            }
        });

    $('#smartwizard .sw-btn-group').append(btnFinish);
    const today = new Date();
    const day30 = new Date();
    day30.setDate(day30.getDate() + 30);

    $('#fecha-emision-group').datetimepicker({
        format: 'YYYY-MM-DD',
        minDate: today,
        maxDate: day30
    });

    $('#chasis').mask('DDDDDDDDDDDDDDDDD', {
        translation: {
            D: {
                pattern: '[A-Za-z0-9]'
            }
        }
    });

    $('#motor').mask('AAAAAAAAAAAAAAAAA');

    $('#form-manual').on('submit', function (e) {
        e.preventDefault();
        $.ajax({
                type: 'POST',
                url: $(this).attr('action'),
                enctype: 'multipart/form-data',
                data: new FormData(this),
                processData: false,
                contentType: false,
                success: function (response) {
                    swal({
                            title: 'Información Recibida!',
                            text: 'Muchas gracias por cotizar con nosotros. Un colaborador del equipo de Trust se pondrá en contacto contigo',
                            imageUrl: "{% static 'cotizador/images/trusty/gracias.png' %}"
                        }
                    ).then(
                        function () {
                            location.reload()
                        }
                    )
                }
            }
        );
    });


    $('#expiry').mask('00 / 00', {reverse: true});
    $('#number').mask('0000 0000 0000 0000', {reverse: true});
    const card = new Card({
        form: '#form-card', // *required*
        // a selector or DOM element for the container
        // where you want the card to appear
        container: '.card-widget', // *required*

        formSelectors: {
            numberInput: 'input#number', // optional — default input[name="number"]
            expiryInput: 'input#expiry', // optional — default input[name="expiry"]
            cvcInput: 'input#cvv', // optional — default input[name="cvc"]
            nameInput: 'input#name' // optional - defaults input[name="name"]
        },

        width: 350, // optional — default 350px
        formatting: true, // optional - default true

        // Strings for translation - optional
        messages: {
            validDate: 'fecha\nvence', // optional - default 'valid\nthru'
            monthYear: 'mm / yy' // optional - default 'month/year'
        },

        // Default placeholders for rendered fields - optional
        placeholders: {
            number: '•••• •••• •••• ••••',
            name: 'Full Name',
            expiry: '•• / ••',
            cvv: '•••'
        },

        masks: {
            cardNumber: '•' // optional - mask card number
        },

        // if true, will log helpful messages for setting up Card
        debug: false // optional - default false
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

    const mostrar_notas = function () {
        $('.p-upgrades-notes').css('display', 'block');
    };

    const ocultar_notas = function () {
        $('.p-upgrades-notes').css('display', 'none');
    };

    const upgrade_action = function () {

        if ($(this).hasClass('unactive')) {
            $.each($('.upgradable'), function (i, o) {
                $(o).removeClass('upgradable');
                $(o).addClass('upgradable-active');
            });

            $.each($('.upgrade-value'), function (i, o) {
                $(o).removeClass('upgrade-unavailable');
                $(o).addClass('upgrade-available');
            });
            $(this).removeClass('unactive');
            $('.upgrade-notes').html('Selecciona el monto de la suma asegurada');
            $('.btn-upgrade').html('eliminar');
            $('#select-exceso').focus();
        } else {
            $.each($('.upgradable-active'), function (i, o) {
                $(o).removeClass('upgradable-active');
                $(o).addClass('upgradable');
            });
            $('#select-exceso').css('color', 'black');
            $.each($('.upgrade-value'), function (i, o) {
                $(o).removeClass('upgrade-available');
                $(o).addClass('upgrade-unavailable');
            });
            $('.upgrade-notes').html('Las coberturas marcadas en verde pueden tener una suma asegurada mayor');
            $('.btn-upgrade').html('prueba aqui');
            $(this).addClass('unactive');
            $('#select-exceso').val('0.00').trigger('change');
        }

    };

    $('.btn-upgrade').on('click', upgrade_action);

    const datos_asegurado = function () {
        if ($(this).val() == 'si') {
            $('#id_primer_nombre').removeAttr('readonly').val('');
            $('#id_segundo_nombre').removeAttr('readonly').val('');
            $('#id_apellido_paterno').removeAttr('readonly').val('');
            $('#id_apellido_materno').removeAttr('readonly').val('');
            $('#telefono').removeAttr('readonly').val('');
            $('#celular').removeAttr('readonly').val('');
            $('#email').removeAttr('readonly').val('');
            $('#cedula').removeAttr('readonly').val('');
            $('#departamento').removeAttr('readonly').val('');
            $('#municipio').removeAttr('readonly').val('');
            $('#domicilio').removeAttr('readonly').html('');
            $('#parentezco_automovil').removeAttr('readonly').val('');
            $('#group-parentezco-automovil').css('display', 'block');
        }
        if ($(this).val() == 'no') {
            $('#id_primer_nombre').attr('readonly', 'readonly').val('{{ user.profile.primer_nombre }}');
            $('#id_segundo_nombre').attr('readonly', 'readonly').val('{{ user.profile.segundo_nombre }}');
            $('#id_apellido_paterno').attr('readonly', 'readonly').val('{{ user.profile.apellido_paterno }}');
            $('#id_apellido_materno').attr('readonly', 'readonly').val('{{ user.profile.apellido_materno }}');
            $('#telefono').attr('readonly', 'readonly').val('{{ user.profile.telefono }}');
            $('#celular').attr('readonly', 'readonly').val('{{ user.profile.celular }}');
            $('#email').attr('readonly', 'readonly').val('{{ user.email }}');
            $('#cedula').attr('readonly', 'readonly').val('{{ user.profile.cedula }}');
            $('#departamento').attr('readonly', 'readonly').val('{{ user.profile.departamento.id }}');
            $('#municipio').attr('readonly', 'readonly').val('{{ user.profile.municipio.id }}');
            $.ajax("{% url 'ajax_getCollection' %}", {
                method: "POST",
                data: {
                    app_label: 'cotizador',
                    model: 'municipio',
                    filters: "{'departamento_id': " + tag_departamento.val() + "}"
                },
                success: function (response) {
                    $('#municipio').attr('readonly', 'readonly').empty();
                    $.each(response, function (i, municipio) {
                        tag_municipio.append($(option_municipio(municipio)));
                    });
                    $('#municipio').attr('readonly', 'readonly').val("{{ user.profile.municipio.id }}")
                }
            });
            $('#domicilio').attr('readonly', 'readonly').html('{{ user.profile.domicilio }}');
            $('#parentezco_automovil').attr('readonly', 'readonly').val('');
            $('#group-parentezco-automovil').css('display', 'none');
        }
    };

    $('#cambio-asegurado-no').on('click', datos_asegurado);
    $('#cambio-asegurado-si').on('click', datos_asegurado);

    $('#celular').mask('00000000');
    $('#cedula').mask('0000000000000A');

    $('#responsabilidad').on('click', function () {
        if ($(this).is(':checked')) {
            $('#btn-finish').removeAttr('disabled').css('cursor', 'auto');
        } else {
            $('#btn-finish').attr('disabled', 'disabled').css('cursor', 'not-allowed');
        }
    });

});