import sys

from django.shortcuts import render_to_response, get_object_or_404
from django.forms.models import inlineformset_factory
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

from web.models import Quote, Event
from web.forms import QuoteForm, EventForm

def home(request):
    latest_quotes = Quote.objects.all().order_by('-date')
    return __quotes(request, latest_quotes)

def best(request):
    quotes = Quote.objects.all().order_by('-votes_up')
    return __quotes(request, quotes)

def worst(request):
    quotes = Quote.objects.all().order_by('-votes_down')
    return __quotes(request, quotes)

def event(request, event_id):
    quotes = Quote.objects.filter(event=event_id).order_by('-votes_up')
    return __quotes(request, quotes)

def like(request, quote_id):
    return __vote(request, quote_id, True)

def dislike(request, quote_id):
    return __vote(request, quote_id, False)

def create_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = QuoteForm()

    return render_to_response('create_quote.html', {'form':form}, context_instance=RequestContext(request))

def create_event(request):
    QuoteInlineFormSet = inlineformset_factory(Event, Quote, can_delete=False, exclude=('date'))
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            formset = QuoteInlineFormSet(request.POST, instance=event)
            if formset.is_valid():
                event.save()
                formset.save()
            return HttpResponseRedirect('/')
        else:
            formset = QuoteInlineFormSet(request.POST)
    else:
        form = EventForm()
        formset = QuoteInlineFormSet()

    return render_to_response('create_event.html', {'form':form,'formset':formset}, context_instance=RequestContext(request))


def __quotes(request, quotes):
    return render_to_response('quotes.html', {'quotes':quotes}, context_instance=RequestContext(request))

def __vote(request, quote_id, like):
    key = 'vote_quote_' + str(quote_id)
    if key in request.COOKIES:
        result = simplejson.dumps([{'success':False, 'error':'Ya votaste!'}])
        return HttpResponse(result, mimetype='application/json')

    try:
        quote = get_object_or_404(Quote, pk=quote_id)
        if like:
            quote.votes_up = quote.votes_up + 1
            votes = quote.votes_up
        else:
            quote.votes_down = quote.votes_down + 1
            votes = quote.votes_down

        quote.save()
        result = simplejson.dumps([{'success':True, 'votes':votes}])
        response = HttpResponse(result, mimetype='application/json')
        response.set_cookie(key)
        return response
    except Exception as e:
        result = simplejson.dumps([{'success':False, 'error':e}])
        return HttpResponse(result, mimetype='application/json')

