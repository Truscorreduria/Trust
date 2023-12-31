from django.shortcuts import render
from django.http import JsonResponse
from .utils import Codec
from django.views.generic import View
from django.forms import modelform_factory
from django.contrib.admin.utils import flatten
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.db.models import Q
from functools import reduce
import operator
from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor
from django.db.models.query_utils import DeferredAttribute
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db import IntegrityError


class Filter:
    def __init__(self, field_name, model, option="=",
                 template_name="adminlte/filters/select-filter.html"):
        self.model = model
        self.field_name = field_name
        self.option = option
        self.template_name = template_name
        self.field = self.get_field()

    def get_form(self):
        return modelform_factory(self.model, fields=(self.field_name,))

    def get_field(self):
        field = getattr(self.model, self.field_name, None)
        if not field:
            raise ValueError('field not exist')
        return field

    def get_model_choices(self):
        return [{'value': x.id, 'name': str(x)} for x in self.field.get_queryset()]

    def get_value(self, instance):
        return getattr(instance, self.field_name)

    def get_value_display(self, instance):
        try:
            return getattr(instance, 'get_%s_display' % self.field_name)
        except:
            return getattr(instance, self.field_name)

    def get_distinct_choices(self):
        return [{'value': self.get_value(x), 'name': self.get_value_display(x)}
                for x in self.model.objects.all().distinct(self.field_name).order_by(self.field_name)]

    def get_bool_choices(self):
        return [{'value': '1', 'name': 'Si'}, {'value': '0', 'name': 'No'}, ]

    def render(self):
        if isinstance(self.field, ForwardManyToOneDescriptor):
            return render_to_string(self.template_name, context={
                'field_name': self.field_name,
                'option': self.option,
                'choices': self.get_model_choices(),
                'table_field': '%s_id' % self.field_name,
                'form': self.get_form(),
            })
        if isinstance(self.field, DeferredAttribute):
            return render_to_string(self.template_name, context={
                'field_name': self.field_name,
                'option': '__icontains=',
                'table_field': self.field_name,
                'choices': self.get_distinct_choices(),
                'form': self.get_form(),
            })
        if isinstance(self.field, bool):
            return render_to_string(self.template_name, context={
                'field_name': self.field_name,
                'option': self.option,
                'table_field': self.field_name,
                'choices': self.get_bool_choices(),
                'form': self.get_form(),
            })


class Datatables(View):
    modal_width = 600
    list_template = "adminlte/datatables.html"
    form_template = "adminlte/datatables-modal.html"
    model = None
    form = None
    buttons = [
        {
            'class': 'btn btn-success btn-perform',
            'perform': 'save',
            'callback': 'process_response',
            'icon': 'fa fa-save',
            'text': 'Guardar',
        },
    ]
    fieldsets = None
    fields = None
    media = None
    list_display = ()
    search_fields = ()
    list_filter = ()
    ordering = None

    @classmethod
    def as_view(cls, **initkwars):
        return staff_member_required(super().as_view(**initkwars), login_url="/cotizador/login/")

    def get_fields(self):
        field_names = []
        if self.fieldsets:
            for fieldset in self.fieldsets:
                field_names.extend(flatten(fieldset['fields']))
        elif self.fields:
            return self.fields
        return field_names

    def get_form(self):
        if not self.form:
            return modelform_factory(self.model, fields=self.get_fields())
        else:
            return self.form

    def get_buttons(self, request, instance=None):
        return self.buttons

    def html_form(self, instance, request, form, method):
        return render_to_string(self.form_template,
                                context={'opts': self.model._meta, 'fieldsets': self.fieldsets,
                                         'form': form, 'instance': instance, 'method': method,
                                         'buttons': self.get_buttons(request, instance=instance)},
                                request=request)

    def get_list_filters(self):
        return [Filter(x, self.model) for x in self.list_filter]

    def get_opts(self):
        return self.model._meta

    def get(self, request, **kwargs):
        return render(request, self.list_template, {
            'opts': self.get_opts(), 'list_display': self.list_display,
            'form': self.get_form(), 'form_template': self.form_template,
            'modal_width': self.modal_width, 'media': self.media,
            'list_filter': self.get_list_filters(),
            **kwargs
        })

    def save_related(self, instance, data):
        pass

    @staticmethod
    def get_filters(filters):
        return [Q((field.split('=')[0], field.split('=')[1])) for field in filters.split('&')]

    def search_value(self, search_value):
        return [
            Q(('{}__icontains'.format(field), word))
            for word in search_value.split(' ')
            for field in self.search_fields
        ]

    def get_queryset(self, filters, search_value):
        queryset = self.model.objects.all()
        if not filters == "":
            queryset = queryset.filter(reduce(operator.and_, self.get_filters(filters)))
        if search_value:
            queryset = queryset.filter(reduce(operator.or_, self.search_value(search_value)))
        return queryset

    def get_ordered_queryset(self, filters, search_value, order):
        queryset = self.get_queryset(filters, search_value)
        return queryset.order_by(order)

    def get_data(self, start, per_page, filters, search_value, draw, order=None):
        queryset = self.get_queryset(filters, search_value)
        if order:
            queryset = self.get_ordered_queryset(filters, search_value, order)
        page = int(start / per_page) + 1
        paginator = Paginator(queryset, per_page)
        data = [x.to_json() for x in paginator.page(page).object_list]
        return {
            'draw': draw,
            'data': data,
            'recordsTotal': len(data),
            'recordsFiltered': queryset.count(),
        }

    def get_instance(self, request):
        try:
            return self.model.objects.get(pk=request.POST.get('pk', '').replace(',', ''))
        except TypeError:
            return None
        except ValueError:
            return None

    @staticmethod
    def get_form_errors(form):
        return [{'key': f, 'errors': e.get_json_data()} for f, e in form.errors.items()]

    def pre_save(self, instance, request):
        return instance

    def pos_save(self, instance, request):
        return instance

    def process_request(self, request, method, instance=None):
        status = 200
        errors = []
        if instance:
            form = self.get_form()(request.POST, instance=instance)
        else:
            form = self.get_form()(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance = self.pre_save(instance, request)
            instance.save()
            instance = self.pos_save(instance, request)
            self.save_related(instance=instance, data=request.POST)
            form = self.get_form()(instance=instance)
            method = "POST"
        else:
            errors = self.get_form_errors(form)
            status = 203
        html_form = self.html_form(instance, request, form, method)
        return instance, html_form, errors, status

    @staticmethod
    def make_response(instance, html_form, errors, status):
        instance_json = {}
        if instance:
            instance_json = instance.to_json()
        return JsonResponse({'instance': instance_json,
                             'form': html_form, 'errors': errors}, encoder=Codec,
                            status=status)

    def post(self, request):
        status = 200
        errors = []
        instance = None
        html_form = ""
        if 'list' in request.POST:
            order = None
            start = int(request.POST.get('start', 0))
            draw = int(request.POST.get('draw', 0))
            per_page = int(request.POST.get('length', 10))
            search_value = request.POST.get('search[value]', None)
            filters = request.POST.get('filters', None)
            order_column = request.POST.get('order[0][column]', None)
            order_dir = request.POST.get('order[0][dir]', None)

            if order_column and order_dir:
                order = ''
                if order_dir == 'desc':
                    order += '-'
                list_display_column = self.list_display[int(order_column)]
                if type(list_display_column) == tuple:
                    order += list_display_column[1].replace('.', '__')
                else:
                    order += list_display_column.split('.')[0]

            return JsonResponse(self.get_data(start, per_page, filters, search_value, draw, order), encoder=Codec)
        if 'open' in request.POST:
            instance = self.get_instance(request)
            form = self.get_form()(instance=instance)
            html_form = self.html_form(instance, request, form, 'POST')  # fixme change to POST
        if 'save' in request.POST:
            instance = self.get_instance(request)
            instance, html_form, errors, status = self.process_request(request, 'POST', instance)
        return self.make_response(instance, html_form, errors, status)

    def put(self, request):
        status = 203
        instance = self.model()
        try:
            form = self.get_form()(request=request)
        except TypeError:
            form = self.get_form()
        html_form = self.html_form(instance, request, form, 'PUT')
        errors = []

        if 'save' in request.PUT:
            instance, html_form, errors, status = self.process_request(request, 'PUT')
        return self.make_response(instance, html_form, errors, status)
