$(document).on('keyup', '#id_cliente_representante-cedula', function () {
    $(this).autocomplete({
        minLength: 2,
        source: $ajax_autocomplete + "?app_label=cotizador&model=clientenatural&column_name=cedula&column_value=cedula",
        select: function (i, o) {
            $('#id_representante').val(o.item.obj.id);
            $('#id_cliente_representante-primer_nombre').val(o.item.obj.primer_nombre);
            $('#id_cliente_representante-segundo_nombre').val(o.item.obj.segundo_nombre);
            $('#id_cliente_representante-apellido_paterno').val(o.item.obj.apellido_paterno);
            $('#id_cliente_representante-apellido_materno').val(o.item.obj.apellido_materno);
            $('#id_cliente_representante-departamento').val(o.item.obj.departamento);
            $('#id_cliente_representante-municipio').val(o.item.obj.municipio);
            $('#id_cliente_representante-telefono').val(o.item.obj.telefono);
            $('#id_cliente_representante-celular').val(o.item.obj.celular);
            $('#id_cliente_representante-domicilio').val(o.item.obj.domicilio);
        }
    })
});