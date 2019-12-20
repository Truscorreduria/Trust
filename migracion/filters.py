from django.contrib.admin.filters import SimpleListFilter

class NullFilterSpec(SimpleListFilter):
    title = u''

    parameter_name = u''

    def lookups(self, request, model_admin):
        return (
            ('1', _('Has value'), ),
            ('0', _('None'), ),
        )

    def queryset(self, request, queryset):
        kwargs = {
        '%s'%self.parameter_name : None,
        }
        if self.value() == '0':
            return queryset.filter(**kwargs)
        if self.value() == '1':
            return queryset.exclude(**kwargs)
        return queryset



class StartNullFilterSpec(NullFilterSpec):
    title = u'Started'
    parameter_name = u'started'