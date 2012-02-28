# Create your views here.
from apps.wiki.models import Wiki
from django.http import Http404
from django.shortcuts import render_to_response
def main(request, wiki_title):
	try:
		wiki = Wiki.objects.get(pk = wiki_title)
	except Wiki.DoesNotExist:
		raise Http404("Wiki does not exit")