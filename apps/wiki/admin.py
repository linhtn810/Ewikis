from django.contrib import admin
from apps.wiki.models import *
admin.site.register(Wiki)
admin.site.register(Section)
admin.site.register(PageOne)
admin.site.register(PageTwo)
admin.site.register(Image)