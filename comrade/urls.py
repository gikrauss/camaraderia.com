from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'comrade.views.home', name='home'),
    # url(r'^comrade/', include('comrade.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/images/favicon.ico'}),
    (r'^favicon\.gif$', 'django.views.generic.simple.redirect_to', {'url': '/static/images/favicon.ico'}),
    url(r'^$', 'web.views.home', name='home'),
    url(r'^best/$', 'web.views.best', name='best'),
    url(r'^worst/$', 'web.views.worst', name='worst'),
    url(r'^event/(?P<event_id>\d+)/$', 'web.views.event', name='event'),
    url(r'^quote/(?P<quote_id>\d+)/like/$', 'web.views.like', name='like'),
    url(r'^quote/(?P<quote_id>\d+)/dislike/$', 'web.views.dislike', name='dislike'),
    url(r'^quote/create/$', 'web.views.create_quote', name='create_quote'),
    url(r'^event/create/$', 'web.views.create_event', name='create_event'),
    url(r'^admin/', include(admin.site.urls)),
)
