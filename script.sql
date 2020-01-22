drop table trustseguros_archivo cascade;
drop table trustseguros_asegurado cascade;
drop table trustseguros_contacto cascade;
drop table trustseguros_endoso cascade;
drop table trustseguros_certificado cascade;
drop table trustseguros_calendariopago cascade;
drop table trustseguros_cesionario cascade;
drop table trustseguros_tramite cascade;
drop table trustseguros_beneficiario cascade;
drop table trustseguros_poliza cascade;
drop table trustseguros_grupo cascade;
drop table trustseguros_aseguradorasubramo cascade;
drop table trustseguros_subramo cascade;
drop table trustseguros_ramo cascade;
drop table trustseguros_aseguradora cascade;
drop table trustseguros_campana cascade;
drop table trustseguros_catalogoarchivo cascade;
drop table trustseguros_cliente cascade;
drop table trustseguros_historicaltramite cascade;
drop table trustseguros_vendedor cascade;


drop table seguros_anno cascade;
drop table seguros_aseguradora cascade;
drop table seguros_beneficio cascade;
drop table seguros_cobertura cascade;
drop table seguros_costo cascade;
drop table seguros_cotizacion cascade;
drop table seguros_cotizacion_aseguradora cascade;
drop table seguros_depreciacion cascade;
drop table seguros_detallecobertura cascade;
drop table seguros_oferta cascade;
drop table seguros_poliza cascade;
drop table seguros_precio cascade;
drop table seguros_producto cascade;
drop table seguros_referencia cascade;
drop table seguros_valordepreciado cascade;


drop table atm_insurance cascade;
drop table atm_insurance_id_seq cascade;
drop table atm_key cascade;
drop table atm_key_id_seq cascade;


drop table RRHH_empleado cascade;
drop table RRHH_empleado_id_seq cascade;
drop table RRHH_pagoempleado cascade;
drop table RRHH_pagoempleado_id_seq cascade;
drop table RRHH_planilla cascade;
drop table RRHH_planilla_id_seq cascade;


delete from auth_user_user_permissions
where permission_id in
(select id from auth_permission
where content_type_id in (select id from django_content_type where app_label = 'trustseguros'));

delete from auth_permission
where content_type_id in (select id from django_content_type where app_label = 'trustseguros');

delete from django_admin_log
where content_type_id in (select id from django_content_type where app_label = 'trustseguros');

delete from django_content_type where app_label = 'trustseguros';


delete from auth_user_user_permissions
where permission_id in
(select id from auth_permission
where content_type_id in (select id from django_content_type where app_label = 'seguros'));

delete from auth_permission
where content_type_id in (select id from django_content_type where app_label = 'seguros');

delete from django_admin_log
where content_type_id in (select id from django_content_type where app_label = 'seguros');

delete from django_content_type where app_label = 'seguros';


delete from auth_user_user_permissions
where permission_id in
(select id from auth_permission
where content_type_id in (select id from django_content_type where app_label = 'RRHH'));

delete from auth_permission
where content_type_id in (select id from django_content_type where app_label = 'RRHH');

delete from django_admin_log
where content_type_id in (select id from django_content_type where app_label = 'RRHH');

delete from django_content_type where app_label = 'RRHH';


delete from auth_user_user_permissions
where permission_id in
(select id from auth_permission
where content_type_id in (select id from django_content_type where app_label = 'atm'));

delete from auth_permission
where content_type_id in (select id from django_content_type where app_label = 'atm');

delete from django_admin_log
where content_type_id in (select id from django_content_type where app_label = 'atm');

delete from django_content_type where app_label = 'atm';


drop table social_auth_usersocialauth cascade;