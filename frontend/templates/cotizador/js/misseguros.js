{% load static %}

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
                    app_label: 'cotizador', model: 'poliza',
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
            swal({
                title: 'Póliza en renovación',
                text: 'Su póliza se encuentra en periodo de renovación',
                imageUrl: "{% static 'cotizador/images/trusty/cool.png' %}"
            })
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
                    app_label: 'cotizador', model: model,
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

    }
);