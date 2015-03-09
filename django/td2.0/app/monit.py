# coding: utf-8
#!/usr/bin/python
import os,sys
from models import Server
#import rrdtool
#import Image
import cStringIO
import tempfile
from django.http import HttpResponse,HttpResponseRedirect

ROOT_PATH = os.path.split(os.path.abspath(os.path.dirname(__file__)))

def createcpu(ip):
	fp = "%s/rrd/%s-cpu.rrd" % (ROOT_PATH[0],str(ip))
	if os.path.isfile(fp): 
		return	'file is exists'
	else:
		ret = rrdtool.create(fp,"--step","300",
                "DS:onecpu:GAUGE:600:0:U",
		"DS:fivecpu:GAUGE:600:0:U",	
		"DS:fifteencpu:GAUGE:600:U:U",
                "RRA:AVERAGE:0.5:1:600",
		"RRA:AVERAGE:0.5:4:700", 
		"RRA:AVERAGE:0.5:24:775", 
		"RRA:AVERAGE:0.5:228:797")
	if ret:
		return rrdtool.error()

def createmem(ip):
        fp = "%s/rrd/%s-mem.rrd" % (ROOT_PATH[0],str(ip))
        if os.path.isfile(fp):
                return  'file is exists'
        else:
                ret = rrdtool.create(fp,"--step","300","--start","0",
                "DS:membuffer:GAUGE:600:0:U",
                "DS:memcache:GAUGE:600:0:U",
		"DS:memfree:GAUGE:600:0:U",
		"DS:memtotal:GAUGE:600:0:U",
                "RRA:AVERAGE:0.5:1:600",
                "RRA:AVERAGE:0.5:4:700",
                "RRA:AVERAGE:0.5:24:775",
                "RRA:AVERAGE:0.5:228:797")
        if ret:
                return rrdtool.error()

def createdisk(ip):
        fp = "%s/rrd/%s-disk.rrd" % (ROOT_PATH[0],str(ip))
        if os.path.isfile(fp):
                return  'file is exists'
        else:
                ret = rrdtool.create(fp,"--step","300","--start","0",
                "DS:avaldisk:GAUGE:600:0:U",
                "DS:useddisk:GAUGE:600:0:U",
                "RRA:AVERAGE:0.5:1:600",
                "RRA:AVERAGE:0.5:4:700",
                "RRA:AVERAGE:0.5:24:775",
                "RRA:AVERAGE:0.5:228:797")
        if ret:
                return rrdtool.error()

def createnet(ip):
        fp = "%s/rrd/%s-net.rrd" % (ROOT_PATH[0],str(ip))
        if os.path.isfile(fp):
                return  'file is exists'
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


def cpuimage(request,id=None):
	if request.user.is_authenticated() and id:
		data = Server.objects.filter(id=id)
		for ip in data:
			if ip.ip:
				fp = "%s/rrd/%s-cpu.rrd" % (ROOT_PATH[0],str(ip.ip))
				fd,path = tempfile.mkstemp('.png')
				print fp
				ret = rrdtool.graph(path,"--start","-23h","-t",str(ip.ip)+"-----Cpu load average","-v","Today CPU",
				"DEF:Onecpu="+fp+":onecpu:AVERAGE",
				"DEF:Fivecpu="+fp+":fivecpu:AVERAGE",
				"DEF:Fifteencpu="+fp+":fifteencpu:AVERAGE",
				"AREA:Onecpu#00CC66:1 Minute Average",
				"GPRINT:Onecpu:LAST:Current\:%8.2lf",
				"LINE2:Fivecpu#330099:5 Minute Average",
				"GPRINT:Fivecpu:LAST:Current\:%8.2lf",
				"LINE2:Fifteencpu#CC0000:15 Minute Average",
                        	"GPRINT:Fifteencpu:LAST:Current\:%8.2lf",
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
	

def memimage(request,id=None):
#        if request.user.is_authenticated() and id:
	data = Server.objects.filter(id=id)
	for ip in data:
		if ip.ip:
			fp = "%s/rrd/%s-mem.rrd" % (ROOT_PATH[0],str(ip.ip))
			fd,path = tempfile.mkstemp('.png')
			ret = rrdtool.graph(path,"--start","-23h","-t",str(ip.ip)+"-----Memory","-v","Today Mem",
			"DEF:Membuffer="+fp+":membuffer:AVERAGE",
		        "DEF:Memcache="+fp+":memcache:AVERAGE",
			"DEF:Memfree="+fp+":memfree:AVERAGE",
			"DEF:Memtotal="+fp+":memtotal:AVERAGE",
			"CDEF:Mem_buffer=Membuffer,1024,/",
			"CDEF:Mem_cache=Memcache,1024,/",
			"CDEF:Mem_free=Memfree,1024,/",
			"CDEF:Mem_total=Memtotal,1024,/",
                        "AREA:Mem_free#8F005CFF:Memory Free",
                        "GPRINT:Mem_free:LAST:Current \:%8.2lf%S",
			"GPRINT:Mem_free:AVERAGE:Average \:%8.2lf%S",
			"GPRINT:Mem_free:MAX:Maxinum \:%8.2lf%S",
                        "AREA:Mem_buffer#FF5700FF:Memory Buffers:STACK",
                        "GPRINT:Mem_buffer:LAST:Current \:%8.2lf%S",
                        "GPRINT:Mem_buffer:AVERAGE:Average \:%8.2lf%S",
                        "GPRINT:Mem_buffer:MAX:Maxinum \:%8.2lf%S",
			"AREA:Mem_cache#FFC73BFF:Cache Memory:STACK",
                        "GPRINT:Mem_cache:LAST:Current \:%8.2lf%S",
                        "GPRINT:Mem_cache:AVERAGE:Average \:%8.2lf%S",
                        "GPRINT:Mem_cache:MAX:Maxinum \:%8.2lf%S",
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
#        return HttpResponseRedirect('/login/')

def diskimage(request,id=None):
        if request.user.is_authenticated() and id:
                data = Server.objects.filter(id=id)
                for ip in data:
                        if ip.ip:
                                fp = "%s/rrd/%s-disk.rrd" % (ROOT_PATH[0],str(ip.ip))
                                fd,path = tempfile.mkstemp('.png')
                                ret = rrdtool.graph(path,"--start","-23h","-t",str(ip.ip)+"-----Disk","-v","Today disk",
                                "DEF:Avaldisk="+fp+":avaldisk:AVERAGE",
                                "DEF:Useddisk="+fp+":useddisk:AVERAGE",
                                "CDEF:Aval_disk=Avaldisk,1024,*",
                                "CDEF:Used_disk=Useddisk,1024,*",
                                "AREA:Aval_disk#0000ff:Avaldisk",
                                "GPRINT:Aval_disk:AVERAGE:usedisk\: %6.2lf %S",
                                "AREA:Used_disk#ff0000:Useddisk:STACK",
                                "GPRINT:Used_disk:AVERAGE:freedisk\: %6.2lf %S",
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



def netimage(request,id=None):
        if request.user.is_authenticated() and id:
                data = Server.objects.filter(id=id)
                for ip in data:
                        if ip.ip:
                                fp = "%s/rrd/%s-net.rrd" % (ROOT_PATH[0],str(ip.ip))
                                fd,path = tempfile.mkstemp('.png')
                                ret = rrdtool.graph(path,"--start","-1d","-t",str(ip.ip)+"-----Net","-v","Today net",
                                "DEF:in_bytes="+fp+":Indata:AVERAGE",
                                "DEF:out_bytes="+fp+":Outdata:AVERAGE",
                                "AREA:in_bytes#0000ff:in",
                                "GPRINT:in_bytes:AVERAGE:Average\: %6.2lf %Sbps",
				"GPRINT:in_bytes:MAX:Maxinum\: %6.2lf %Sbps",
                                "AREA:out_bytes#ff0000:out:STACK",
                                "GPRINT:out_bytes:AVERAGE:Average\: %6.2lf %Sbps",
				"GPRINT:out_bytes:MAX:Maxinum\: %6.2lf %Sbps",
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



def monthimage(request,id=None):
        if request.user.is_authenticated() and id:
                data = Server.objects.filter(id=id)
                for ip in data:
                        if ip.ip:
                                fp = "%s/rrd/%s-disk.rrd" % (ROOT_PATH[0],str(ip.ip))
                                fd,path = tempfile.mkstemp('.png')
                                ret = rrdtool.graph(path,"--start","-1m","-t",str(ip.ip),"-v","Today",
                                "DEF:in_bytes="+fp+":Indata:AVERAGE",
                                "DEF:out_bytes="+fp+":Outdata:AVERAGE",
                                "LINE:in_bytes#0000ff:in",
                                "GPRINT:in_bytes:MAX:MAX IN\: %6.2lf %S",
                                "LINE2:out_bytes#ff0000:out:STACK",
                                "GPRINT:out_bytes:MAX:MAX OUT\: %6.2lf %S",
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

