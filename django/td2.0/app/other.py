from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger,InvalidPage
from models import *
from forms import *

def paging(data,page,url):
	if url == "jigui":
		paginator = Paginator(data,10)
	if url == "switch":
	        paginator = Paginator(data,9)
	if url == "yserver":
		paginator = Paginator(data,5)
	if url == "rserver":
		paginator = Paginator(data,5)
	if url == "repair":
		paginator = Paginator(data,5)
	if url == "ipaddr":
		paginator = Paginator(data,30)
	if url == "cacti":
		paginator = Paginator(data,30)
	if url == "swcacti":
		paginator = Paginator(data,30)
        try:
                newpage=int(page)
        except ValueError:
                newpage=1
        try:
                contacts = paginator.page(newpage)
        except PageNotAnInteger:
                contacts = paginator.page(1)
        except EmptyPage:
                contacts = paginator.page(paginator.num_pages)
        return contacts

def Modelskey(key):
        Models =  { 'jigui':Room,
		    'yserver':Mac,
		    'rserver':Server,
		    'switch':Switch,
		    'repair':Repair,
		    'cacti':Server,
		    'ipaddr':Server,
		    'cactilist':Server,
		    'swcacti':Switch,
		    'swcactilist':Switch,
                }
        return Models[key]

def Formskey(key):
        forms = { 'jigui':FormRoom,
		  'yserver':FormMac,
		  'rserver':FormServer,
		  'switch':FormSwitch,
		  'repair':FormRepair,
		  'ipaddr':FormServer,
		
                }
        return forms[key]

def Forskey(url,pag):
        forskey = {
                        'jifang':pag.cabinet_set.all(),
                        'jigui':pag.server_set.all(),
                }
	return forskey[url]

def Searchkey(content):
	searchs = {'1':Room.objects.filter(jigui__exact=q),
		   '2':Mac.objects.filter(eth0__exact=q),
		   '3':Server.objects.filter(ip__exact=q),
		   '4':Server.objects.filter(fuwu__exact=q),
  		}
	return searchs[content,q]
		 

