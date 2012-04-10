from apps.wiki.models import *
from apps.wiki.forms import *
from apps.wiki.wiki import *

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.template import Context, RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q
#from pure_pagination.paginator import Paginator

import re
import settings

def about(request):
	return render_to_response("wiki/about.html", context_instance=RequestContext(request))
def main(request):
	wiki = Wiki.objects.all().order_by('-like')[:5]
	var = RequestContext(request,{
		'wiki': wiki,
	})
	return render_to_response("wiki/main.html",var)

def wiki(request,title_id):
	wiki = get_object_or_404(Wiki,pk = title_id)
	userlike = wiki.userlike.filter(username = request.user.username)
	section = wiki.section_set.all()
	var = RequestContext(request,{
		'wiki': wiki,
		'section': section,
		'userlike': userlike,	
	})
	return render_to_response('wiki/wiki.html', var)

@login_required	
def addtext(request, title_id):
	wiki = Wiki.objects.get(pk = title_id)
	if request.method == 'POST':
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
@login_required	
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
@login_required
def editsection(request, title_id, sec_id):
	section = get_object_or_404(Section, pk = sec_id)
	wiki = get_object_or_404(Wiki, pk = title_id)
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
	return render_to_response('wiki/addtext.html',var)

@login_required	
def deletesection(request, title_id):
	if 'id' in request.GET:
		sec_id = request.GET['id']
		section = Section.objects.get(pk = sec_id)
		section.delete()
	return HttpResponseRedirect("/"+ title_id)
	
@login_required	
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
@login_required	
def editwiki(request, title_id):
	wiki = get_object_or_404(Wiki,pk = title_id)
	section = wiki.section_set.all()
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
			if title_id != temp_title_id:
				for sec in section:
					wiki.section_set.create(title = sec.title,content = 			 
					sec.content, content_markdown = sec.content_markdown)
				wikiold = Wiki.objects.get(pk = temp_title_id)
				wiki.like = wikiold.like
				for user in wikiold.userlike.all():
					wiki.userlike.add(user)
				wiki.save()
				wikiold.delete()
			return HttpResponseRedirect("/"+ wiki.titleid)
	else:
		form = CreateWikiForm(instance = Wiki.objects.get(pk = title_id))
	var = RequestContext(request,{'form':form,'wiki': wiki})
	return render_to_response('wiki/createwiki.html',var)
	
@login_required
def deletewiki(request, title_id):
	wiki = Wiki.objects.get(pk = title_id)
	section = wiki.section_set.all()
	for sec in section:
		sec.delete()
	wiki.delete()
	return HttpResponseRedirect("/wiki/main")
	
@login_required
def likewiki(request, titleid):
	wiki = get_object_or_404(Wiki,pk = titleid)
	section = wiki.section_set.all()
	userlike = wiki.userlike.filter(username = request.user.username)
	if not userlike:
		wiki.like +=1
		wiki.userlike.add(request.user)
		wiki.save()
	var = RequestContext(request,{
		'wiki': wiki,
		'userlike': userlike,
		'section': section,
	})
	if request.GET.has_key('like'):
		return render_to_response('wiki/wiki_like.html', var)
	else:
		return render_to_response('wiki/wiki.html', var)
@login_required	
def movesection(request, titleid,sectionid):
	'''
	request.GET['move'] = 1 => up; 0 => down

	'''
	wiki = get_object_or_404(Wiki, pk = titleid)
	section = wiki.section_set.all()
	current_section = Section.objects.get(id__exact = sectionid)
	pre,next = get_pre_or_next_section(current_section,section)
	if 'move'in request.GET:
		move = request.GET['move']
		if move == '1':
			if pre:
				swap_data(pre,current_section)
		if move == '0':
			if next:
				swap_data(next,current_section)			
		return HttpResponseRedirect('/' + titleid)
	
	raise Http404
	