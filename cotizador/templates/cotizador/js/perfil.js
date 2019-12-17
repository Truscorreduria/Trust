function option_municipio(municipio) {
    return (`
    <option value="${municipio.id}">${municipio.name}</option>
    `)
}

function alertPassword(message, clase) {
    return (`<div class="alert alert-${clase}">
                <strong>${message}</strong>
            </div>`)
}

$(document).ready(function () {

    const tag_departamento = $('#departamento');
    const tag_municipio = $('#municipio');

    tag_departamento.on('change', function () {
        $.ajax("{% url 'ajax_getCollection' %}", {
            method: "POST",
            data: {
                app_label: 'cotizador',
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
        tag_departamento.val({{ user.profile.departamento.id }});

        $.ajax("{% url 'ajax_getCollection' %}", {
            method: "POST",
            data: {
                app_label: 'cotizador',
                model: 'municipio',
                filters: "{'departamento_id': " + tag_departamento.val() + "}"
            },
            success: function (response) {
                tag_municipio.empty();
                $.each(response, function (i, municipio) {
                    tag_municipio.append($(option_municipio(municipio)));
                });
                tag_municipio.val({{ user.profile.municipio.id }})
            }
        });

    {% endif %}

    const modal_password = function () {
        $('#modal-password').modal('show');
    };

    $('#btn-password').on('click', modal_password);

    const submit_form = function (e) {
        e.preventDefault();
        const form = $(this);
        errors = $(form).find('.errors').empty();
        if ($('#pass_new').val() === $('#pass_conf').val()) {
            $.ajax("{% url 'cotizador:change_password' %}", {
                method: "post",
                data: form.serialize(),
                success: function (response) {
                    if (response.class === 'success') {
                        $('#modal-password').modal('hide');
                        swal('Excelente!',
                            'Tu cotraseña ha sido actualizada con éxito. Por seguridad inicia sesión nuevamente.',
                            'success').then(function () {
                            location.reload();
                        });
                    } else {
                        $.each(response.messages, function (i, message) {
                            errors.append(alertPassword(message, response.class));
                        })
                    }

                }
            })

        } else {
            errors.append(alertPassword("No coiciden los campos!", "danger"));
        }
    };

    $('#change-password-form').on('submit', submit_form);

    {% if user.profile.cambiar_pass %}
        $('#pass_actual').val('Trust2019');
        modal_password();
    {% endif %}


});