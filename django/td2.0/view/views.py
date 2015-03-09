# coding: utf-8
from app.models import *
from app.forms import *
from django.shortcuts import render_to_response,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.template import Template,loader,RequestContext
from django.db import IntegrityError
import time,datetime
from app.other import *
from django.views.decorators.csrf import csrf_exempt
from app.monit import *
from app.switch import *
from app.rebuild import *

def index(request):
	if request.user.is_authenticated():
		if request.method == 'GET':
			rooms_list = []
			rooms = Room.objects.all()
			for room in rooms:
				jigui = Server.objects.filter(idmac__idroom=room.id).order_by('idmac__paihao')
				switch = Switch.objects.filter(idroom = room.id).order_by('paihao')
				rooms_list.append([room,jigui,switch])
		return render_to_response("index.html",{'room':rooms_list},RequestContext(request))
	return HttpResponseRedirect('/login/')

def mainview(request,url):
	if request.user.is_authenticated():
		data = Modelskey(url).objects.all()
		modeldata = paging(data,request.GET.get('page','1'),url)
        	return render_to_response(url+'.html',{'data':modeldata,'today':datetime.datetime.today(),'url':url},context_instance=RequestContext(request))
	return HttpResponseRedirect('/login/')

@csrf_exempt
def add(request,url):
	if request.user.is_authenticated():
	        form = Formskey(url)(request.POST)
        	if request.method == 'POST':
			if  request.POST.get('paihao',''):
				paihao = request.POST.get('paihao','')
				if int(paihao) > 15:
                        		errors = "亲！交换机或者服务器位置输入的数字不要大于12，返回去从输吧"
                        		return render_to_response('error.html',{'errors':errors},context_instance=RequestContext(request))	
				if request.POST.get('idroom',''):
					idroom = request.POST.get('idroom','')
					switch = Switch.objects.filter(idroom=idroom).filter(paihao=int(paihao))
					mac = Mac.objects.filter(idroom=idroom).filter(paihao=int(paihao))
					if switch:
						for data  in switch:
							error = data.ip
						errors = "Has already been switch used %s" % error
						return render_to_response('error.html',{'errors':errors},context_instance=RequestContext(request))
					if mac:
						for data in mac:
							error = data.eth0
						errors = "Has already been server used %s" % error
						return render_to_response('error.html',{'errors':errors},context_instance=RequestContext(request))
                	if form.is_valid():
                        	form.save()
				if ( url == 'rserver' and request.POST['ip'] != ''):
                                	createcpu(request.POST['ip'])
                                	createmem(request.POST['ip'])
                                	createdisk(request.POST['ip'])
                                	createnet(request.POST['ip'])
				if ( url == 'switch' and request.POST['ip'] != ''):
					createswitch(request.POST['ip'],request.POST['port'])
				return HttpResponseRedirect('/'+url+'/')
		if url=='repair':
			maclist1 = Mac.objects.all()
			return render_to_response(url+'add.html',{'form':form,'maclist1':maclist1},context_instance=RequestContext(request))
		if url=="switch":
			datalist1 = Room.objects.all()
                	return render_to_response(url+'add.html',{'form':form,'datalist1':datalist1},context_instance=RequestContext(request))

		if url=="yserver":
			datalist1 = Room.objects.all()
			return render_to_response(url+'add.html',{'form':form,'datalist1':datalist1},context_instance=RequestContext(request))
        	if url=="rserver":
			switchlist1 = Switch.objects.all()
			maclist1 = Mac.objects.all()
			datalist1 = Room.objects.all()
			return render_to_response(url+'add.html',{'form':form,'maclist1':maclist1,'datalist1':datalist1,'switchlist1':switchlist1},context_instance=RequestContext(request))
		data = Modelskey(url).objects.all()
        	modeldata = paging(data,request.GET.get('page','1'),url)
        	return render_to_response(url+'add.html',{'form':form},context_instance=RequestContext(request))
	return HttpResponseRedirect('/login/')

@csrf_exempt
def edit(request,url,id):
	if request.user.is_authenticated():
		Modelsurl = get_object_or_404(Modelskey(url),pk=id)
		form = Formskey(url)(instance=Modelsurl)
		if request.method == 'POST':
        		form = Formskey(url)(request.POST,instance=Modelsurl)
                        if  request.POST.get('paihao',''):
                                paihao = request.POST.get('paihao','')
                                if int(paihao) > 15:
                                        errors = "亲！交换机或者服务器位置输入的数字不要大于15，返回去从输吧"
                                        return render_to_response('error.html',{'errors':errors},context_instance=RequestContext(request))
                                if request.POST.get('idroom',''):
                                        idroom = request.POST.get('idroom','')
					ipaddr = request.POST.get('ip','')
					qcode =  request.POST.get('qcode','')
					switchs = Switch.objects.filter(idroom=idroom).filter(paihao=int(paihao)).filter(ip=ipaddr)
					macs = Mac.objects.filter(idroom=idroom).filter(paihao=int(paihao)).filter(qcode=qcode)
					switchspaihao = ''
					macspaihao = ''
					if switchs:
						for validation in switchs:
							switchspaihao = validation.paihao
					if macs:
						for validation in macs:
							macspaihao = validation.paihao
					if int(paihao) != switchspaihao and int(paihao) != macspaihao:
						switch = Switch.objects.filter(idroom=idroom).filter(paihao=int(paihao))
						mac = Mac.objects.filter(idroom=idroom).filter(paihao=int(paihao))
						if switch:
							for data  in switch:
                                                                error = data.ip
                                                        errors = "Has already been switch used %s" % error
                                                        return render_to_response('error.html',{'errors':errors},context_instance=RequestContext(request))
                                                if mac:
                                                        for data in mac:
                                                                error = data.eth0
                                                        errors = "Has already been server used %s" % error
                                                        return render_to_response('error.html',{'errors':errors},context_instance=RequestContext(request))

			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/'+url+'/')
        	if url=="switch":
			form = Formskey(url)(instance=Modelsurl)
                        datalist1 = Room.objects.all()
                        return render_to_response(url+'add.html',{'form':form,'datalist1':datalist1},context_instance=RequestContext(request))
        	if url=='repair':
			form = Formskey(url)(instance=Modelsurl)
                        maclist1 = Mac.objects.all()
                        return render_to_response(url+'add.html',{'form':form,'maclist1':maclist1},context_instance=RequestContext(request))
        	if url=="yserver":
			form = Formskey(url)(instance=Modelsurl)
                        datalist1 = Room.objects.all()
                        return render_to_response(url+'add.html',{'form':form,'datalist1':datalist1},context_instance=RequestContext(request))
        	if url=="rserver":
			form = Formskey(url)(instance=Modelsurl)
                        switchlist1 = Switch.objects.all()
                        maclist1 = Mac.objects.all()
                        datalist1 = Room.objects.all()
                        return render_to_response(url+'add.html',{'form':form,'maclist1':maclist1,'datalist1':datalist1,'switchlist1':switchlist1},context_instance=RequestContext(request))
		return render_to_response(url+'edit.html',{'form':form},context_instance=RequestContext(request))
	return HttpResponseRedirect('/login/')

@csrf_exempt
def delete(request,url,id):
	if request.user.is_authenticated():
		Del = get_object_or_404(Modelskey(url),pk=id)
		try:
			Del.delete()
		except  IntegrityError:
			errors = "底下有分类数据未清空！无法删除"
			return render_to_response('error.html',{'errors':errors},context_instance=RequestContext(request))
		else:
			return HttpResponseRedirect('/'+url+'/')
	return HttpResponseRedirect('/login/')

def cactilist(request,id):
	if request.user.is_authenticated():
		url = 'cactilist'
		data = Modelskey(url).objects.filter(id=id)
		return render_to_response('cactilist.html',{'data':data},context_instance=RequestContext(request))
	return HttpResponseRedirect('/login/')

def swcactilist(request,id):
        if request.user.is_authenticated():
		ports =[]
                url = 'swcactilist'
                data = Modelskey(url).objects.filter(id=id)
		for ip in data:
			ports =  range(1,ip.port+1)
                return render_to_response('swcactilist.html',{'ip':ip,'ports':ports},context_instance=RequestContext(request))
        return HttpResponseRedirect('/login/')



def search(request):
	if request.user.is_authenticated():
		if 'q' in request.GET and 'content' in request.GET:
			q = request.GET['q']
			content = request.GET['content']
			datalist =''
			if  q and content:
				if content == '1':
					datalist = Room.objects.filter(jigui__iexact=q)
					return render_to_response('jigui.html',{'data':datalist},context_instance=RequestContext(request))
				if content == '2':
					datalist = Mac.objects.filter(eth0__iexact=q)
					return render_to_response('yserver.html',{'data':datalist},context_instance=RequestContext(request))
				if content == '3':
					datalist = Server.objects.filter(ip__iexact=q)
					return render_to_response('rserver.html',{'data':datalist},context_instance=RequestContext(request))
				if content == '4':
					datalist = Server.objects.filter(fuwu__iexact=q)
					return render_to_response('rserver.html',{'data':datalist},context_instance=RequestContext(request))
		return render_to_response('search.html',context_instance=RequestContext(request))
	return HttpResponseRedirect('/login/')

def rebuild(request,url,id):
	if request.user.is_authenticated():
		if request.method == 'GET':
			if url == "cacti":
				ip = Server.objects.get(id=id)
				if ip.ip:
					rebulidcpu(ip.ip)
					rebulidmem(ip.ip)
					rebuliddisk(ip.ip)
					rebuildnet(ip.ip)
					infor = "重建成功"
			if url == 'switch':
				switchs = Switch.objects.get(id=id)
				ports =  range(1,switchs.port+1)
				rebuildswitch(switchs.ip,ports)
				infor = "重建成功"
		return render_to_response('rebuild.html',{'infor':infor},context_instance=RequestContext(request))
	return HttpResponseRedirect('/login/')		

	
