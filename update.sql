drop table alquirer_commerce cascade;
drop table alquirer_contact cascade;
drop table alquirer_contract cascade;
drop table alquirer_contractbuilding cascade;
drop table alquirer_contractrow cascade;
drop table alquirer_discount cascade;

alter table importaciones_bulk rename to backend_bulk;
alter table importaciones_category rename to backend_category;
alter table importaciones_container rename to backend_container;
alter table importaciones_customer rename to backend_customer;
alter table importaciones_item rename to backend_item;
alter table importaciones_material rename to backend_material;
alter table importaciones_origin rename to backend_origin;
alter table importaciones_outcoming rename to backend_outcoming;
alter table importaciones_outcomingrow rename to backend_outcomingrow;
alter table importaciones_package rename to backend_package;
alter table importaciones_port rename to backend_port;
alter table importaciones_product rename to backend_product;
alter table importaciones_storeplace rename to backend_storeplace;
alter table importaciones_unittype rename to backend_unittype;

delete from django_migrations where app = 'alquirer';
delete from django_migrations where app = 'produccion';
delete from django_migrations where app = 'importaciones';
delete from django_migrations where app = 'portal';


delete from auth_user_user_permissions
where permission_id in
(select id from auth_permission
where content_type_id in (select id from django_content_type where app_label = 'alquirer'));
delete from auth_permission
where content_type_id in (select id from django_content_type where app_label = 'alquirer');
delete from django_admin_log
where content_type_id in (select id from django_content_type where app_label = 'alquirer');
delete from django_content_type where app_label = 'alquirer';


delete from auth_user_user_permissions
where permission_id in
(select id from auth_permission
where content_type_id in (select id from django_content_type where app_label = 'produccion'));
delete from auth_permission
where content_type_id in (select id from django_content_type where app_label = 'produccion');
delete from django_admin_log
where content_type_id in (select id from django_content_type where app_label = 'produccion');
delete from django_content_type where app_label = 'produccion';


delete from auth_user_user_permissions
where permission_id in
(select id from auth_permission
where content_type_id in (select id from django_content_type where app_label = 'importaciones'));
delete from auth_permission
where content_type_id in (select id from django_content_type where app_label = 'importaciones');
delete from django_admin_log
where content_type_id in (select id from django_content_type where app_label = 'importaciones');
delete from django_content_type where app_label = 'importaciones';


delete from auth_user_user_permissions
where permission_id in
(select id from auth_permission
where content_type_id in (select id from django_content_type where app_label = 'portal'));
delete from auth_permission
where content_type_id in (select id from django_content_type where app_label = 'portal');
delete from django_admin_log
where content_type_id in (select id from django_content_type where app_label = 'portal');
delete from django_content_type where app_label = 'portal';