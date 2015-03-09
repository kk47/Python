# coding: utf-8
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm,SetPasswordForm
from django.contrib.auth.models import User
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def login_view(request):
        error = False
        if request.method == 'POST':
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(username=username,password=password)
                if user is not None:
                        if user.is_active:
                                login(request,user)
                                return HttpResponseRedirect('/')
                else:
                        error = True
                        return render_to_response('login.html',{'error':error})
        return render_to_response('login.html')

@csrf_exempt
def logout_view(request):
        logout(request)
        return HttpResponseRedirect('/login/')

@csrf_exempt
def register(request):
        if (request.user.is_authenticated() and request.user.has_perm('pro.add_server')):
                if request.method == 'POST':
                        form = UserCreationForm(request.POST)
                        if form.is_valid():
                                form.save()
                                return HttpResponseRedirect('/user/')
                form = UserCreationForm()
                room = User.objects.all()
                return render_to_response('useradd.html',{'form':form,'room':room},context_instance=RequestContext(request))
        errors = "你好像无权访问吧?"
        return render_to_response('error.html',{'errors':errors})

@csrf_exempt
def change_pass(request):
        if request.user.is_authenticated():
                if request.method == 'POST':
                        form = PasswordChangeForm(request.user,request.POST)
                        if form.is_valid():
                                form.save()
                                return HttpResponseRedirect('/')
                form = PasswordChangeForm(user=request.user)
                return render_to_response('change_pass.html',{'form':form},context_instance=RequestContext(request))
        errors = "你好像无权访问吧?"
        return render_to_response('error.html',{'errors':errors})

@csrf_exempt
def setpassword(request,id):
        if (request.user.is_authenticated() and request.user.has_perm('pro.add_server')):
                user = User.objects.get(id=id)
                if request.method == 'POST':
                        form = SetPasswordForm(user,request.POST)
                        if form.is_valid():
                                form.save()
                                return HttpResponseRedirect('/')
                form = SetPasswordForm(user)
                return render_to_response('change_pass.html',{'form':form},context_instance=RequestContext(request))
        errors = "你好像无权访问吧?"
        return render_to_response('error.html',{'errors':errors})

def delete(request,id):
        Del = get_object_or_404(User,pk=id)
        Del.delete()
        return HttpResponseRedirect('/user/')
