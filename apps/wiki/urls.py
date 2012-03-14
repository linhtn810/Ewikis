from django.conf.urls.defaults import patterns, include, url
urlpatterns = patterns('apps.wiki.views',
	url(r'^(\w+)/$','wiki'),
	url(r'^(\w+)/(\d+)/edit/$','editsection'),
	url(r'^(\w+)/deletesection/$','deletesection'),
	url(r'^(\w+)/addtext/$','addtext'),
	url(r'^(\w+)/addimage/','addimage'),
	url(r'^wiki/main/$','main'),
	url(r'^(\w+)/editwiki/$','editwiki'),
	url(r'^(\w+)/deletewiki/$','deletewiki'),
	url(r'^wiki/create/$','createwiki'),
	url(r'^wiki/like/$','likewiki'),	
)