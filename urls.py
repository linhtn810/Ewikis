from django.conf.urls.defaults import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
import settings

urlpatterns = patterns('',
	url(r'^(\w+)/$','apps.wiki.views.wiki'),
	url(r'^(\w+)/(\d+)/edit/$','apps.wiki.views.editsection'),
	url(r'^(\w+)/deletesection/$','apps.wiki.views.deletesection'),
	url(r'^(\w+)/addtext/$','apps.wiki.views.addtext'),
	url(r'^(\w+)/addimage/','apps.wiki.views.addimage'),
	url(r'^wiki/main/$','apps.wiki.views.main'),
	url(r'^(\w+)/editwiki/$','apps.wiki.views.editwiki'),
	url(r'^(\w+)/deletewiki/$','apps.wiki.views.deletewiki'),
	url(r'^wiki/create/$','apps.wiki.views.createwiki'),
	url(r'^wiki/like/$','apps.wiki.views.likewiki'),
	url(r'^/',include('apps.wiki.urls'))
	url(r'^wiki/admin/',include(admin.site.urls)),
	(r'^static/(?P<path>.*)$','django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
	(r'^media/(?P<path>.*)$','django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),	
)