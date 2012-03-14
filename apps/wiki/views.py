from apps.wiki.models import *
from apps.wiki.forms import *

from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.template import Context, RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q

import re
import settings

def main(request):
	wiki = Wiki.objects.all()
	var = RequestContext(request,{
		'wiki': wiki,
	})
	return render_to_response("wiki/index.html", {'wiki': wiki},var)

def wiki(request,title_id):
	wiki = get_object_or_404(Wiki,pk = title_id)
	section = wiki.section_set.all()
	var = RequestContext(request,{
		'wiki': wiki,
		'section': section,	
	})
	return render_to_response('wiki/main.html', var)
	
def addtext(request, title_id):
	wiki = Wiki.objects.get(pk = title_id)
	if request.method == 'POST':
		if request.user == wiki.user:
			textform = TextForm(request.POST)
			if textform.is_valid():
				inp = textform.cleaned_data
				wiki.section_set.create(title = inp['title'],
										content = inp['content'],
										content_markdown = inp['content'])
				return HttpResponseRedirect("/"+ title_id)
		textform = TextForm()
	else:
		textform = TextForm()
	var = RequestContext(request,{
			'textform':textform,
			'wiki': wiki,	
			})
	return render_to_response('wiki/addtext.html',var)

def addimage(request, title_id):
	wiki = Wiki.objects.get(pk = title_id)
	image = None
	if request.user.is_authenticated and request.user == wiki.user:
		if request.method == 'POST':
			imageform = ImageForm(request.POST, request.FILES)
			if imageform.is_valid():
				title = imageform.cleaned_data['title']
				uploadphoto = imageform.cleaned_data['photo']
				image = Image.objects.create(
					user = request.user,
					photo = uploadphoto,
					title = title
				)
				image.save()
				content_image_markdown = '![%s](%s)'% (image.title, image.photo.url)
				wiki.section_set.create(
						title = title, 
						content = content_image_markdown,
						content_markdown = content_image_markdown
					)
				return HttpResponseRedirect("/"+ title_id)
			imageform = ImageForm()

	imageform = ImageForm()
	var = RequestContext(request,{
		'imageform':imageform,
		'wiki':wiki,
		})
	return render_to_response('wiki/addimage.html',var)

def editsection(request, title_id, sec_id):
	section = Section.objects.get(pk = sec_id)
	wiki = Wiki.objects.get(pk = title_id)
	if request.method == 'POST':
		textform = TextForm(request.POST)
		if textform.is_valid():
			inp = textform.cleaned_data
			section.title = inp['title']
			section.content = inp['content']
			section.content_markdown = inp['content']
			section.save()
		return HttpResponseRedirect("/"+ title_id)
	else: 
		textform = TextForm(instance=Section.objects.get(pk = sec_id))
	var = RequestContext(request,{
			'textform':textform,
			'wiki': wiki})
	return render_to_response('wiki/edit.html',var)

def deletesection(request, title_id):
	if 'id' in request.GET:
		sec_id = request.GET['id']
		section = Section.objects.get(pk = sec_id)
		section.delete()
	return HttpResponseRedirect("/"+ title_id)
	
def createwiki(request):
	if request.method == 'POST':
		form = CreateWikiForm(request.POST)
		if form.is_valid():
			inp = form.cleaned_data
			title_id = inp['title'].lower()
			title_id = ''.join(re.compile(r'\W+').split(title_id))
			check_titleid  = Wiki.objects.all()
			# check link to access wiki
			for check in check_titleid:
				if title_id == check.titleid:
					title_id = title_id + '_1'
			userlike = User.objects.get(username = request.user.username)
			wiki = Wiki(
				user = request.user,
				title = inp['title'],
				titleid = title_id,
				description = inp['description'],
				gradelevel = inp['gradelevel'],
				subject = inp['subject'],
				lessontype = inp['lessontype'],
				like = 0,
				)
			wiki.save()
			return HttpResponseRedirect("/"+ title_id)
	else:
		form = CreateWikiForm()
	var = RequestContext(request,{'form':form,})
	return render_to_response('wiki/createwiki.html',var)
	
def editwiki(request, title_id):
	wiki = Wiki.objects.get(pk = title_id)
	temp_title_id  = title_id
	if request.method == 'POST':	
		form = CreateWikiForm(request.POST)
		if form.is_valid():
			inp = form.cleaned_data
			title_id = inp['title'].lower()
			title_id = ''.join(re.compile(r'\W+').split(title_id))
			check_titleid  = Wiki.objects.all()
			for check in check_titleid:
				if title_id == check.titleid:
					if title_id != temp_title_id:
						title_id = title_id + '_1'
			wiki.titleid = title_id
			wiki.title = inp['title']
			wiki.description = inp['description']
			wiki.gradelevel = inp['gradelevel']
			wiki.subject = inp['subject']
			wiki.lessontype = inp['lessontype']
			section = wiki.section_set.all()
			for sec in section:
				wiki.section_set.create(title = sec.title,content = 			 
				sec.content, content_markdown = sec.content_markdown)
			wiki.save()
			if title_id != temp_title_id:
				wikiold = Wiki.objects.get(pk = temp_title_id)
				wikiold.delete()
			return HttpResponseRedirect("/"+ wiki.titleid)
	else:
		form = CreateWikiForm(instance = Wiki.objects.get(pk = title_id))
	var = RequestContext(request,{'form':form,'wiki': wiki})
	return render_to_response('wiki/createwiki.html',var)
	
def deletewiki(request, title_id):
	wiki = Wiki.objects.get(pk = title_id)
	section = wiki.section_set.all()
	for sec in section:
		sec.delete()
	wiki.delete()
	return HttpResponseRedirect("/wiki/main")
	
def likewiki(request):
	if 'titleid' in request.GET:
		titleid = request.GET['titleid']
		wiki = Wiki.objects.get(pk = titleid)
		wiki.like +=1
		wiki.save()
	return HttpResponseRedirect("/wiki/main")
