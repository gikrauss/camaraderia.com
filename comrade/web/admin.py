from django.contrib import admin
from web.models import Event
from web.models import Quote

import csv
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

def export_as_csv(modeladmin, request, queryset):
    """
    Generic csv export admin action.
    """
    if not request.user.is_staff:
        raise PermissionDenied
    opts = modeladmin.model._meta
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')
    writer = csv.writer(response)
    field_names = [field.name for field in opts.fields]
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])
    return response

export_as_csv.short_description = "Export selected objects as csv file"

class QuoteInline(admin.TabularInline):
    model = Quote
    fields = ['quote']

class EventAdmin(admin.ModelAdmin):
    inlines = [
        QuoteInline,
    ]
    actions = [export_as_csv]
    list_per_page = 10
    list_filter = ('date',)

class QuoteAdmin(admin.ModelAdmin):
    list_filter = ('event',)

admin.site.register(Event, EventAdmin)
admin.site.register(Quote, QuoteAdmin)
