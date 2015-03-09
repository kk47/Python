# coding: utf-8
#!/usr/bin/python
import os,sys
from models import Switch
#import rrdtool
#import Image
import cStringIO
import tempfile
from django.http import HttpResponse,HttpResponseRedirect

ROOT_PATH = os.path.split(os.path.abspath(os.path.dirname(__file__)))

def createswitch(ip,port):
	ports = int(port)
	for p in range(1,ports+1):
		fp = "%s/rrd/%s-%s.rrd" % (ROOT_PATH[0],str(ip),int(p))
		if os.path.isfile(fp): 
			return	'file is exists'
		else:
			ret = rrdtool.create(fp,"--step","300","--start","0",
        	        "DS:Indata:COUNTER:600:U:U",
               	 	"DS:Outdata:COUNTER:600:U:U", 
                	"RRA:AVERAGE:0.5:1:600",
			"RRA:AVERAGE:0.5:4:700", 
			"RRA:AVERAGE:0.5:24:775", 
			"RRA:AVERAGE:0.5:228:797")
		if ret:
			return rrdtool.error()

def swimage(request,id,ports):
	if request.user.is_authenticated() and id:
		data = Switch.objects.filter(id=id)
		for ip in data:
			if ip.ip:
				fp = "%s/rrd/%s-%s.rrd" % (ROOT_PATH[0],str(ip.ip),int(ports))
        	                fd,path = tempfile.mkstemp('.png')
                	        ret = rrdtool.graph(path,"--start","-1m","-t",str(ip.ip)+ "--" +str(ports),"-v","Today",
                        	"DEF:in_bytes="+fp+":Indata:AVERAGE",
                                "DEF:out_bytes="+fp+":Outdata:AVERAGE",
                                "LINE:in_bytes#0000ff:in",
                                "GPRINT:in_bytes:MAX:MAX IN\: %6.2lf %Sbps",
                                "LINE2:out_bytes#ff0000:out:STACK",
                                "GPRINT:out_bytes:MAX:MAX OUT\: %6.2lf %Sbps",
                                "-w","800")
                                im = Image.open(path)
                                out = cStringIO.StringIO()
                                im.save(out,format='png')
                                room = out.getvalue()
                               	out.close()
                                os.remove(path)
                                return HttpResponse(room,'image/png')
                        if ret:
                                return rrdtool.error()

	return HttpResponseRedirect('/login/')

