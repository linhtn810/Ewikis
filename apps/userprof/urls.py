from django.conf.urls.defaults import *
from apps.userprof.views import *

urlpatterns = patterns('',
    (r'^user/login/$', 'django.contrib.auth.views.login'),
)
urlpatterns += patterns('apps.userprof.views',
    (r'^user/register/$', register_page),
    (r'^user/edit_profile/$', edit_profile_page),
    (r'^user/change_password/$', change_password_page),
    (r'^user/logout/$', logout_page),
    (r'^user/(\w+)/$', user_profile_page),
    (r'^$', home_page),
)
