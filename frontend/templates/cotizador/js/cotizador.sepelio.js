{% load static humanize %}
$(document).ready(function () {

    function activarFechaSepelio() {

        $('.mask-only-text').mask('Z', {
            translation: {
                'Z': {pattern: /[a-zA-ZáéíóúñÑ ]/, recursive: true}
            }
        });

        const today = new Date();
        let yearmin = new Date();
        yearmin.setDate(yearmin.getDate() - 21900);
        $.each($('.fecha-nacimiento-sepelio-group'), function (i, o) {
            $(o).datetimepicker({
                format: 'YYYY-MM-DD',
                maxDate: today,
                minDate: yearmin
            })
        });
    }

    function rowDepentienteSepelio() {
        return (`<tr>
                    <td>
                        <div class="form-group">
                            <input type="text" class="form-control form-control-sm mask-only-text"
                                   id="primer_nombre_sepelio" required>
                            <div class="help-block with-errors"></div>
                        </div>
                    </td>
                    <td>
                        <div class="form-group">
                            <input type="text" class="form-control form-control-sm mask-only-text"
                                   id="segundo_nombre_sepelio">
                            <div class="help-block with-errors"></div>
                        </div>
                    </td>
                    <td>
                        <div class="form-group">
                            <input type="text" class="form-control form-control-sm mask-only-text"
                                   id="apellido_paterno_sepelio" required>
                            <div class="help-block with-errors"></div>
                        </div>
                    </td>
                    <td>
                        <div class="form-group">
                            <input type="text" class="form-control form-control-sm mask-only-text"
                                   id="apellido_materno_sepelio">
                            <div class="help-block with-errors"></div>
                        </div>
                    </td>
                    <td>
                        <div class="form-group">
                            <select name="parentesco-sepelio" id="parentesco-sepelio"
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
                            <div class='input-group date fecha-nacimiento-sepelio-group'>
                                <input type='text' class="form-control form-control-sm"
                                       id="fecha_nacimiento_sepelio" required/>
                                <span class="input-group-append input-group-addon">
                                <span class="input-group-text glyphicon glyphicon-calendar"></span>
                            </span>
                            </div>
                            <div class="help-block with-errors"></div>
                        </div>
                    </td>
                </tr>`)
    }

    function rowCotizacionSepelio(obj) {
        return (`<tr>
                    <td>${obj.primer_nombre} ${obj.segundo_nombre} ${obj.apellido_paterno} ${obj.apellido_materno}</td>
                    <td>Muerte por cualquier causa</td>
                    <td>U$ {{ user.config.suma_sepelio|intcomma }}</td>
                    <td>U$ {{ user.config.costo_sepelio|intcomma }}</td>
                </tr>`)
    }

    function rowDocumentosSepelio(obj) {
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

    function rowSelectCuota(number) {
        return (`<option value="${number}">${number}</option>`)
    }

    function salvarDependientes() {
        let dependientesSepelio = [];
        localStorage.removeItem("dependientes_sepelio");
        $.each($('#table-dependientes-sepelio tbody tr'), function (i, tr) {
            dependientesSepelio.push({
                parentesco: $(tr).find('#parentesco-sepelio').val(),
                primer_nombre: $(tr).find('#primer_nombre_sepelio').val(),
                segundo_nombre: $(tr).find('#segundo_nombre_sepelio').val(),
                apellido_paterno: $(tr).find('#apellido_paterno_sepelio').val(),
                apellido_materno: $(tr).find('#apellido_materno_sepelio').val(),
                fecha_nacimiento: $(tr).find('#fecha_nacimiento_sepelio').val()
            })
        });
        localStorage.setItem("dependientes_sepelio", JSON.stringify(dependientesSepelio));
    }

    function renderDependientes() {
        const dependientes = JSON.parse(localStorage.getItem("dependientes_sepelio"));
        let cotizacion = $('#table-cotizacion-sepelio').find('tbody').empty();
        $.each(dependientes, function (i, o) {
            cotizacion.append(rowCotizacionSepelio(o));
        });
        let suma = {{ user.config.suma_sepelio }} * dependientes.length;
        let prima = {{ user.config.costo_sepelio }} * dependientes.length;
        $('#span-suma-asegurada-cotizacion-sepelio').empty().html(intcommas(suma.toFixed(1)));
        $('#span-total-cotizacion-sepelio').empty().html(intcommas(prima.toFixed(2)));
        $('#h2-anual-sepelio').empty().html(intcommas(prima.toFixed(2)));
        $('#total-sepelio').val(prima.toFixed(2));
        let total_dependientes = dependientes.length;
        let select_cuotas = $('#cantidad_cuotas_sepelio').empty();
        if (total_dependientes === 1) {
            select_cuotas.append(rowSelectCuota(1));
        }

        if (total_dependientes === 2) {
            select_cuotas.append(rowSelectCuota(1));
            select_cuotas.append(rowSelectCuota(2));
        }

        if (total_dependientes > 2 && total_dependientes < 6) {
            // mario.rojas@valuarte.com.ni
            // ricoh mpc306
            for (let i = 1; i < 5; i++) {
                select_cuotas.append(rowSelectCuota(i));
            }
        }

        if (total_dependientes >= 6) {
            for (let i = 1; i < 7; i++) {
                select_cuotas.append(rowSelectCuota(i));
            }
        }

    }

    function solicitarDocumentos() {
        const dependientes = JSON.parse(localStorage.getItem("dependientes_sepelio"));
        let documentos = $('#table-documentos-sepelio').find('tbody').empty();
        $.each(dependientes, function (i, o) {
            documentos.append(rowDocumentosSepelio(o));
        });
    }

    function getFormData() {
        const dependientes = JSON.parse(localStorage.getItem("dependientes_sepelio"));
        data = new FormData();
        $.each($('#table-documentos-sepelio tbody tr'), function (i, tr) {
            dependientes[i]['tipo_identificacion'] = $(tr).find('.tipo-identidad').val();
            dependientes[i]['documento_adjunto'] = $(tr).find('.documento-adjunto')[0].files[0];
        });

        $.each(dependientes, function (i, o) {
            data.append('parentesco', o.parentesco);
            data.append('primer_nombre', o.primer_nombre);
            data.append('segundo_nombre', o.segundo_nombre);
            data.append('apellido_paterno', o.apellido_paterno);
            data.append('apellido_materno', o.apellido_materno);
            data.append('fecha_nacimiento', o.fecha_nacimiento);
            data.append('tipo_identificacion', o.tipo_identificacion);
            data.append('documento_adjunto_' + i, o.documento_adjunto);
        });

        return data;

    }

    const calcular_cuota = function () {
        let total = parseFloat($('#total-sepelio').val());
        $('#h2-anual-sepelio').html(intcommas(parseFloat(total).toFixed(2)));
        let numero_cuotas = parseFloat($('#cantidad_cuotas_sepelio').val());
        $('#h2-mensual-sepelio').html(intcommas(parseFloat(total / numero_cuotas).toFixed(2)));
        $('#valor-cuota-sepelio').val((total / numero_cuotas).toFixed(2));
    };

    $('#cantidad_cuotas_sepelio').on('change', calcular_cuota);

    const btnFinish = $('<button style="display: none;" id="btn-finish-sepelio"></button>').text('Finalizar')
        .addClass('btn btn-info sw-btn-finish')
        .on('click', function () {
            const elmForm = $("#form-sepelio-step-3");
            elmForm.validator('validate');
            let elmErr = $(elmForm).find('.has-error');
            if (elmErr && elmErr.length > 0) {
                return false;
            } else {
                data = getFormData();
                $.ajax("{% url 'cotizador:guardar_sepelio' %}", {
                    type: "POST",
                    contentType: false,
                    processData: false,
                    cache: false,
                    data: data,
                    success: function (response) {
                        let fdata = new FormData();
                        fdata.append('orden', response.orden.id);
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
                        swal({
                            title: 'Tu póliza se ha emitido con exito!',
                            text: 'Ahora serás dirigido a la seccion de tus seguros activos.',
                            imageUrl: "{% static 'cotizador/images/trusty/gracias.png' %}"
                        }).then(function () {
                            window.location = "{% url 'cotizador:misseguros' %}";
                        });
                    }
                });
            }
        });

    $('#smartwizard-sepelio').smartWizard({
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
            const elmForm = $("#form-sepelio-step-" + stepNumber);
            if (stepDirection === 'forward' && elmForm) {
                elmForm.validator('validate');
                const elmErr = $(elmForm).find('.has-error');
                if (elmErr && elmErr.length > 0) {
                    return false;
                }
                if (parseInt(stepNumber) === 0) {
                    salvarDependientes();
                    renderDependientes();
                    calcular_cuota();
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
                                $('#smartwizard-sepelio').smartWizard('goToStep', 2);
                                solicitarDocumentos();
                            } else {
                                $('#smartwizard-sepelio').smartWizard('goToStep', 1);
                            }
                        }
                    )
                }
                if (parseInt(stepNumber) === 2) {
                    $('#smartwizard-sepelio .sw-btn-next').css('display', 'none');
                    $('#btn-finish-sepelio').css('display', 'block');
                }
            }

            if (stepDirection === 'backward' && elmForm) {
                $('#btn-finish-sepelio').css('display', 'none');
                $('#smartwizard-sepelio .sw-btn-next').css('display', 'block');
            }

            return true;
        });

    $('#smartwizard-sepelio .sw-btn-group').append(btnFinish);

    $('#btn-add-dependiente-sepelio').on('click', function () {
        $('#table-dependientes-sepelio tbody').append(rowDepentienteSepelio());
        activarFechaSepelio();
    }).trigger('click');

});