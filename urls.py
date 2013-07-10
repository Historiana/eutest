from django.conf.urls.defaults import *
from django.conf import settings


urlpatterns = patterns('',
    
    #(r'^chaining/',                                          include('smart_selects.urls')),
    #(r'^eu/',                                          include('eutest.urls')),
    (r'^$',                                                  'eutest.views.start'),
)
