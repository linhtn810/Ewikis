from django.conf.urls.defaults import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
import settings

urlpatterns = patterns('',
	url(r'^',include('apps.wiki.urls')),
	url(r'^wiki/admin/',include(admin.site.urls)),
	(r'^static/(?P<path>.*)$','django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
	(r'^media/(?P<path>.*)$','django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),	
)