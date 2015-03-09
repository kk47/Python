from django.conf.urls import patterns, url, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('view.views',
        (r'^$','index'),
	(r'^(?P<url>(jigui)|(switch)|(rserver)|(yserver)|(repair)|(ipaddr)|(cacti)|(swcacti))/$','mainview'),
        (r'^(?P<url>(jigui)|(yserver)|(rserver)|(switch)|(repair))/add/$','add'),
        (r'^(?P<url>(jigui)|(yserver)|(rserver)|(switch)|(repair))/edit/(?P<id>\d+)/$','edit'),
        (r'^(?P<url>(jigui)|(yserver)|(rserver)|(switch)|(repair))/del/(?P<id>\d+)/$','delete'),
	(r'^cactilist/(?P<id>\d+)/$','cactilist'),
	(r'^swcactilist/(?P<id>\d+)/$','swcactilist'),
	(r'^rebuildcacti/(?P<url>(cacti)|(switch))/(?P<id>\d+)/$','rebuild'),
        (r'^images/cpuimage/(?P<id>\d+)','cpuimage'),
        (r'^images/memimage/(?P<id>\d+)','memimage'),
        (r'^images/diskimage/(?P<id>\d+)','diskimage'),
        (r'^images/netimage/(?P<id>\d+)','netimage'),
	(r'^images/swimage/(?P<id>\d+)/(?P<ports>\d+)/$','swimage'),
	(r'^search/','search'),
)

urlpatterns += patterns('view.login',
        (r'^login/$','login_view'),
        (r'^logout/$','logout_view'),
        (r'^user/$','register'),
        (r'^user/del/(?P<id>\d+)/$','delete'),
        (r'^user/change_pass/$','change_pass'),
        (r'^user/setpassword/(?P<id>\d+)/$','setpassword'),
 )


urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
