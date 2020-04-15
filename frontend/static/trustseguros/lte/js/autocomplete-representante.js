$(document).on('keyup', '#id_cliente_representante-cedula', function () {
    $(this).autocomplete({
        minLength: 2,
        source: $ajax_autocomplete + "?app_label=backend&model=clientenatural&column_name=cedula&column_value=cedula",
        select: function (i, o) {
            $('#id_cliente_representante-primer_nombre').val(o.item.obj.primer_nombre).removeAttr('readonly');
            $('#id_cliente_representante-segundo_nombre').val(o.item.obj.segundo_nombre).removeAttr('readonly');
            $('#id_cliente_representante-apellido_paterno').val(o.item.obj.apellido_paterno).removeAttr('readonly');
            $('#id_cliente_representante-apellido_materno').val(o.item.obj.apellido_materno).removeAttr('readonly');
            $('#id_cliente_representante-departamento').val(o.item.obj.departamento).removeAttr('disabled');
            $('#id_cliente_representante-municipio').val(o.item.obj.municipio).removeAttr('disabled');
            $('#id_cliente_representante-telefono').val(o.item.obj.telefono).removeAttr('readonly');
            $('#id_cliente_representante-celular').val(o.item.obj.celular).removeAttr('readonly');
            $('#id_cliente_representante-domicilio').val(o.item.obj.domicilio).removeAttr('readonly');
            $('#id_cliente_representante-tipo_identificacion').attr('disabled', 'disabled');
            $('#id_cliente_representante-cedula').attr('readonly', 'readonly');

            $('.representante-button-clear').css('display', 'initial');
        }
    });

    if ($(this).val().length === 14) {
        $('#id_cliente_representante-primer_nombre').removeAttr('readonly');
        $('#id_cliente_representante-segundo_nombre').removeAttr('readonly');
        $('#id_cliente_representante-apellido_paterno').removeAttr('readonly');
        $('#id_cliente_representante-apellido_materno').removeAttr('readonly');
        $('#id_cliente_representante-departamento').removeAttr('disabled');
        $('#id_cliente_representante-municipio').removeAttr('disabled');
        $('#id_cliente_representante-telefono').removeAttr('readonly');
        $('#id_cliente_representante-celular').removeAttr('readonly');
        $('#id_cliente_representante-domicilio').removeAttr('readonly');
        $('#id_cliente_representante-cedula').attr('readonly', 'readonly');
        $('.representante-button-clear').css('display', 'initial');
    }
});


$(document).on('click', '.representante-button-clear', function () {
    $('#id_cliente_representante-primer_nombre').val('').attr('readonly', 'readonly');
    $('#id_cliente_representante-segundo_nombre').val('').attr('readonly', 'readonly');
    $('#id_cliente_representante-apellido_paterno').val('').attr('readonly', 'readonly');
    $('#id_cliente_representante-apellido_materno').val('').attr('readonly', 'readonly');
    $('#id_cliente_representante-departamento').val('').attr('disabled', 'disabled');
    $('#id_cliente_representante-municipio').val('').attr('disabled', 'disabled');
    $('#id_cliente_representante-telefono').val('').attr('readonly', 'readonly');
    $('#id_cliente_representante-celular').val('').attr('readonly', 'readonly');
    $('#id_cliente_representante-domicilio').val('').attr('readonly', 'readonly');
    $('#id_cliente_representante-cedula').val('').removeAttr('readonly', 'readonly');
    $('#id_cliente_representante-tipo_identificacion').removeAttr('disabled', 'disabled');
    $(this).css('display', 'none');
});