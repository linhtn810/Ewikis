from django.contrib import admin
from apps.wiki.models import *
class SectionInline(admin.StackedInline):
	model = Section
	extra = 1
class WikiAdmin(admin.ModelAdmin):
	inlines = [SectionInline]

admin.site.register(Wiki, WikiAdmin)
admin.site.register(Image)