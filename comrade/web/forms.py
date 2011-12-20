import datetime
from django import forms
from django.forms import ModelForm

from web.models import Event, Quote

class QuoteForm(ModelForm):
    class Meta:
        model = Quote
        fields = ('date', 'quote')

class EventForm(ModelForm):
    class Meta:
        model = Event
