from apps.userprof.forms import *
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.models import check_password, User
from django.contrib.auth.decorators import login_required
from django.contrib.redirects.models import Redirect
from django.views.generic.simple import direct_to_template
from apps.userprof.forms import register_form, change_password_form, edit_profile_form
from apps.userprof.models import Profile

@login_required
def change_password_page(request):
    if request.method == "POST":
        form = change_password_form(request.POST)
        if form.is_valid():
            user, f = User.objects.get_or_create(username=request.user.username)
            raw_password = form.cleaned_data['password']
            new_password = form.cleaned_data['password1']
            enc_password = user.password
            if check_password(raw_password, enc_password):
                user.set_password(new_password)
                user.save()
                return HttpResponseRedirect('/logout/')
            else:
                return HttpResponseRedirect('/change_password/')
    else:
        form = change_password_form()
    variables = RequestContext(request, {'form': form})
    return render_to_response('registration/change_password.html', variables)


@login_required
def edit_profile_page(request):
    if request.method == "POST":
        form = edit_profile_form(request.POST)
        if form.is_valid():
            _edit_profile_page(request, form)
            return HttpResponseRedirect('/')
    else:
        profile = Profile.objects.get(user=request.user)
        first_name = profile.user.first_name
        last_name = profile.user.last_name
        website_blog = profile.website_blog
        location = profile.location
        about = profile.about
        form = edit_profile_form({
            'first_name': first_name,
            'last_name': last_name,
            'website_blog': website_blog,
            'location': location,
            'about': about
        })
    variables = RequestContext(request, {'form': form})
    return render_to_response('registration/edit_profile.html', variables)


def _edit_profile_page(request, form):
    user, f = User.objects.get_or_create(username=request.user.username)
    user.first_name = form.cleaned_data['first_name']
    user.last_name = form.cleaned_data['last_name']
    user.save()
    profile, f = Profile.objects.get_or_create(user=request.user)
    profile.website_blog = form.cleaned_data['website_blog']
    profile.location = form.cleaned_data['location']
    profile.about = form.cleaned_data['about']
    profile.save()
    return profile


def home_page(request):
    try:
        profile = Profile.objects.get(user=request.user)
        variables = RequestContext(request, {'profile': profile})
    except:
        variables = RequestContext(request, {'user': request.user})
    return render_to_response('home.html', variables)


@login_required
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/wiki/main/')


def register_page(request):
    if request.method == "POST":
        form = register_form(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'])
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            prof = Profile.objects.create(user=user, website_blog='', location='', about='')
            prof.save()
            return HttpResponseRedirect('/login/')
    else:
        form = register_form()
    variables = RequestContext(request, {'form': form})
    return render_to_response('registration/register.html', variables)


def user_profile_page(request, username):
    owner = False
    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        if user == request.user:
            owner = True
        variables = RequestContext(request, {'profile': profile, 'owner': owner})
    except User.DoesNotExist, Profile.DoesNotExist:
        variables = RequestContext(request, {'profile': False, 'owner': owner})
    return render_to_response('user_profile.html', variables)