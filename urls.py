from django.conf.urls.defaults import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'EWikis.views.home', name='home'),
    # url(r'^EWikis/', include('EWikis.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	url(r'^wiki/(?P<wiki_title>[^/]+)/$','apps.wiki.views.main'),
	#url(r'^wiki/(?P<wiki_title>[^/]+)/edit/$','apps.wiki.views.edit'),
    url(r'^admin/', include(admin.site.urls)),

	#url(r'^static/(?P<path>.*)$','django.views.static.serve', {'document_root': setting.MEDIA_ROOT}),

)
