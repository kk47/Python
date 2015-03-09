#from django.conf.urls import patterns, include, url
from django.conf.urls import *
from mysite.views import *
from contact.views import *
from django.contrib import admin
#from django.views.generic.simple import direct_to_template
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', search),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/$', include(admin.site.urls)),
    #url(r'^search/$', search),
    url(r'^meta/$', dislpay_meta),
    (r'^foo/$', foobar_view, {'template_name': 'template1.html'}),
    (r'^bar/$', foobar_view, {'template_name': 'template2.html'}),
    (r'^mydata/(?P<month>\w{3}/(?P<day>\d\d))/$', my_view), 
#    (r'^events/$', object_list, {'model': models.Event}),
#    (r'^blog/entries/$', object_list, {'model': models.models.BlogEntry}),
#    (R'^somepage/$', views.method_splitter, {'GET': views.some_page_get, 'POST': views_some_page_post}),
#    (r'^about/$', direct_to_template, {
#        'template': 'about.html'
#    }),
#    (r'^about/(\w+)/$', about_pages),
)

urlpatterns += patterns('',
    url(r'^contact/$', contact),
    url(r'^contact/thanks/$', thanks),
)
#if setting.DEBUG:
#    urlpatterns += patterns('',
#        (r'^debuginfo/$', debug),
#)
