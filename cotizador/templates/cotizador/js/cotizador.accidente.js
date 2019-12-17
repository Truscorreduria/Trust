{% load static humanize %}

$(document).ready(function () {

    function activarFechaAccidente() {


        $('.mask-only-text').mask('Z', {
            translation: {
                'Z': {pattern: /[a-zA-ZáéíóúñÑ ]/, recursive: true}
            }
        });

        const today = new Date();
        let yearmin = new Date();
        yearmin.setDate(yearmin.getDate() - 21900);
        $.each($('.fecha-nacimiento-accidente-group'), function (i, o) {
            $(o).datetimepicker({
                format: 'YYYY-MM-DD',
                maxDate: today,
                minDate: yearmin
            })
        });
    }

    function rowDepentienteAccidente() {
        return (`<tr>
                    <td>
                        <div class="form-group">
                            <input type="text" class="form-control form-control-sm mask-only-text"
                                   id="primer_nombre_accidente" required>
                            <div class="help-block with-errors"></div>
                        </div>
                    </td>
                    <td>
                        <div class="form-group">
                            <input type="text" class="form-control form-control-sm mask-only-text"
                                   id="segundo_nombre_accidente">
                            <div class="help-block with-errors"></div>
                        </div>
                    </td>
                    <td>
                        <div class="form-group">
                            <input type="text" class="form-control form-control-sm mask-only-text"
                                   id="apellido_paterno_accidente" required>
                            <div class="help-block with-errors"></div>
                        </div>
                    </td>
                    <td>
                        <div class="form-group">
                            <input type="text" class="form-control form-control-sm mask-only-text"
                                   id="apellido_materno_accidente">
                            <div class="help-block with-errors"></div>
                        </div>
                    </td>
                    <td>
                        <div class="form-group">
                            <select name="parentesco-accidente" id="parentesco-accidente"
                                    class="form-control form-control-sm" required>
                                <option disabled selected></option>
                                <option value="Padre">Padre</option>
                                <option value="Madre">Madre</option>
                                <option value="Hermano">Hermano</option>
                                <option value="Hermana">Hermana</option>
                                <option value="Cónyuge">Cónyuge</option>
                                <option value="Hijo">Hijo</option>
                                <option value="Hija">Hija</option>
                            </select>
                            <div class="help-block with-errors"></div>
                        </div>
                    </td>
                    <td>
                        <div class="form-group">
                            <div class='input-group date fecha-nacimiento-accidente-group'>
                                <input type='text' class="form-control form-control-sm"
                                       id="fecha_nacimiento_accidente" required/>
                                <span class="input-group-append input-group-addon">
                                <span class="input-group-text glyphicon glyphicon-calendar"></span>
                            </span>
                            </div>
                            <div class="help-block with-errors"></div>
                        </div>
                    </td>
                </tr>`)
    }

    function rowCotizacionAccidente(obj, costo) {
        return (`<tr>
                    <td>${obj.primer_nombre} ${obj.segundo_nombre} ${obj.apellido_paterno} ${obj.apellido_paterno}</td>
                    <td>Reembolso de Gastos por Accidente.</td>
                    <td>U$ {{ config.SUMA_ACCIDENTE_DEPENDIENTE|intcomma }}</td>
                    <td>U$ ${costo}</td>
                </tr>`)
    }

    function rowDocumentosAccidente(obj) {
        return (`<tr>
                    <td>${obj.primer_nombre} ${obj.segundo_nombre} ${obj.apellido_paterno} ${obj.apellido_paterno}</td>
                    <td>
                        <div class="form-group">
                            <select class="form-control form-control-sm tipo-identidad" required>
                                <option></option>
                                <option value="cedula">Cédula de Identidad</option>
                                <option value="acta">Acta de Nacimiento</option>
                            </select>
                            <div class="help-block with-errors"></div>
                        </div>
                    </td>
                    <td style="text-align: right">
                        <div class="form-group">
                            <input type="file" class="documento-adjunto" required>
                            <div class="help-block with-errors"></div>
                        </div>
                    </td>
                </tr>`)
    }

    const calcular_cuota = function () {
        let total = parseFloat($('#total-accidente').val());
        $('#h2-anual-accidente').html(intcommas(parseFloat(total).toFixed(2)));
        let numero_cuotas = parseFloat($('#cantidad_cuotas_accidente').val());
        $('#h2-mensual-accidente').html(intcommas(parseFloat(total / numero_cuotas).toFixed(2)));
        $('#valor-cuota-accidente').val((total / numero_cuotas).toFixed(2));
    };

    $('#cantidad_cuotas_accidente').on('change', calcular_cuota);

    function cotizar() {

        $.ajax("{% url 'cotizador:costo_accidente' %}", {
            method: 'POST',
            success: function (response) {
                let dependientesAccidente = [];
                localStorage.removeItem("dependientes_accidente");
                $.each($('#table-dependientes-accidente tbody tr'), function (i, tr) {
                    dependientesAccidente.push({
                        parentesco: $(tr).find('#parentesco-accidente').val(),
                        primer_nombre: $(tr).find('#primer_nombre_accidente').val(),
                        segundo_nombre: $(tr).find('#segundo_nombre_accidente').val(),
                        apellido_paterno: $(tr).find('#apellido_paterno_accidente').val(),
                        apellido_materno: $(tr).find('#apellido_materno_accidente').val(),
                        fecha_nacimiento: $(tr).find('#fecha_nacimiento_accidente').val(),
                        costo: response.costo, prima: response.prima, carnet: response.carnet,
                        suma: response.suma, emision: response.emision
                    })
                });
                localStorage.setItem("dependientes_accidente", JSON.stringify(dependientesAccidente));

                let cotizacion = $('#table-cotizacion-accidente').find('tbody').empty();
                $.each(dependientesAccidente, function (i, o) {
                    cotizacion.append(rowCotizacionAccidente(o, intcommas(o['costo'])));
                });

                let total = dependientesAccidente.map(function (o) {
                    return o['costo'];
                }).reduce(function (a, b) {
                    return a + b
                });

                let suma_asegurada = dependientesAccidente.map(function (o) {
                    return o['suma'];
                }).reduce(function (a, b) {
                    return a + b
                });

                $('#span-suma-asegurada-cotizacion-accidente').empty().html(intcommas(suma_asegurada.toFixed(1)));
                $('#span-total-cotizacion-accidente').empty().html(intcommas(total.toFixed(2)));
                $('#total-accidente').val(total);
                calcular_cuota();
            }
        });


    }

    function solicitarDocumentos() {
        const dependientes = JSON.parse(localStorage.getItem("dependientes_accidente"));
        let documentos = $('#table-documentos-accidente').find('tbody').empty();
        $.each(dependientes, function (i, o) {
            documentos.append(rowDocumentosAccidente(o));
        });
    }

    function getFormData() {
        const dependientes = JSON.parse(localStorage.getItem("dependientes_accidente"));
        data = new FormData();
        $.each($('#table-documentos-accidente tbody tr'), function (i, tr) {
            dependientes[i]['tipo_identificacion'] = $(tr).find('.tipo-identidad').val();
            dependientes[i]['documento_adjunto'] = $(tr).find('.documento-adjunto')[0].files[0];
        });
        console.log(dependientes);
        $.each(dependientes, function (i, o) {
            data.append('parentesco', o.parentesco);
            data.append('primer_nombre', o.primer_nombre);
            data.append('segundo_nombre', o.segundo_nombre);
            data.append('apellido_paterno', o.apellido_paterno);
            data.append('apellido_materno', o.apellido_materno);
            data.append('fecha_nacimiento', o.fecha_nacimiento);
            data.append('tipo_identificacion', o.tipo_identificacion);
            data.append('prima', o.prima);
            data.append('carnet', o.carnet);
            data.append('emision', o.emision);
            data.append('costo', o.costo);
            data.append('suma_asegurada', o.suma);
            data.append('documento_adjunto_' + i, o.documento_adjunto);
        });

        return data;

    }

    const btnFinish = $('<button style="display: none;" id="btn-finish"></button>').text('Finalizar')
        .addClass('btn btn-info sw-btn-finish')
        .on('click', function () {
            const elmForm = $("#form-accidente-step-3");

            elmForm.validator('validate');
            let elmErr = $(elmForm).find('.has-error');
            if (elmErr && elmErr.length > 0) {
                return false;
            } else {
                //activar_spinner();
                data = getFormData();
                $.ajax("{% url 'cotizador:guardar_accidente' %}", {
                    type: "POST",
                    contentType: false,
                    processData: false,
                    cache: false,
                    data: data,
                    success: function (response) {
                        let fdata = new FormData();
                        fdata.append('orden', response.orden.id);
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

                        swal({
                            title: 'Muchas gracias',
                            text: 'Tu póliza se ha emitido con exito. Ahora serás dirigido a la seccion de tus seguros activos.',
                            imageUrl: "{% static 'cotizador/images/trusty/exito.png' %}"
                        }).then(function () {
                            window.location = "{% url 'cotizador:misseguros' %}";
                        });
                    }
                });
            }
        });

    $('#smartwizard-accidente').smartWizard({
        selected: 0,
        theme: 'dots',
        transitionEffect: 'slide',
        lang: {
            next: 'Siguiente',
            previous: 'Anterior'
        },
        toolbarSettings: {
            toolbarPosition: 'bottom'
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
            const elmForm = $("#form-accidente-step-" + stepNumber);
            if (stepDirection === 'forward' && elmForm) {
                elmForm.validator('validate');
                const elmErr = $(elmForm).find('.has-error');
                if (elmErr && elmErr.length > 0) {
                    return false;
                }
                if (parseInt(stepNumber) === 0) {
                    cotizar();
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
                                $('#smartwizard-accidente').smartWizard('goToStep', 2);
                                solicitarDocumentos();
                            } else {
                                $('#smartwizard-accidente').smartWizard('goToStep', 1);
                            }
                        }
                    )
                }
                if (parseInt(stepNumber) === 2) {
                    $('#smartwizard-accidente .sw-btn-next').css('display', 'none');
                    btnFinish.css('display', 'block');
                }
            }

            if (stepDirection === 'backward' && elmForm) {
                $('.sw-btn-finish').css('display', 'none');
                $('.sw-btn-next').css('display', 'block');
            }

            return true;
        });

    $('#smartwizard-accidente .sw-btn-group').append(btnFinish);

    $('#btn-add-dependiente-accidente').on('click', function () {
        $('#table-dependientes-accidente tbody').append(rowDepentienteAccidente());
        activarFechaAccidente();
    }).trigger('click');

});