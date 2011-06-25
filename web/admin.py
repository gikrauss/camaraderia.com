from django.contrib import admin
from web.models import Event
from web.models import Quote

class QuoteInline(admin.TabularInline):
    model = Quote
    fields = ['quote']

class EventAdmin(admin.ModelAdmin):
    inlines = [
        QuoteInline,
    ]

admin.site.register(Event, EventAdmin)
admin.site.register(Quote)

