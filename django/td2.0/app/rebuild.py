# coding: utf-8
#!/usr/bin/python
import os,sys
from models import Server
#import rrdtool
from django.http import HttpResponse,HttpResponseRedirect

ROOT_PATH = os.path.split(os.path.abspath(os.path.dirname(__file__)))

def rebulidcpu(ip):
        fp = "%s/rrd/%s-cpu.rrd" % (ROOT_PATH[0],str(ip))
        if os.path.isfile(fp):
		os.remove(fp)
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


def rebulidmem(ip):
        fp = "%s/rrd/%s-mem.rrd" % (ROOT_PATH[0],str(ip))
        if os.path.isfile(fp):
		os.remove(fp)
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

def rebuliddisk(ip):
        fp = "%s/rrd/%s-disk.rrd" % (ROOT_PATH[0],str(ip))
        if os.path.isfile(fp):
		os.remove(fp)
	ret = rrdtool.create(fp,"--step","300","--start","0",
	"DS:avaldisk:GAUGE:600:0:U",
	"DS:useddisk:GAUGE:600:0:U",
	"RRA:AVERAGE:0.5:1:600",
	"RRA:AVERAGE:0.5:4:700",
	"RRA:AVERAGE:0.5:24:775",
	"RRA:AVERAGE:0.5:228:797")
        if ret:
                return rrdtool.error()


def rebuildnet(ip):
        fp = "%s/rrd/%s-net.rrd" % (ROOT_PATH[0],str(ip))
        if os.path.isfile(fp):
		os.remove(fp)
	ret = rrdtool.create(fp,"--step","300","--start","0",
	"DS:Indata:COUNTER:600:U:U",
	"DS:Outdata:COUNTER:600:U:U",
	"RRA:AVERAGE:0.5:1:600",
	"RRA:AVERAGE:0.5:4:700",
	"RRA:AVERAGE:0.5:24:775",
	"RRA:AVERAGE:0.5:228:797")
        if ret:
                return rrdtool.error()

def rebuildswitch(ip,ports):
	for port in ports:
        	fp = "%s/rrd/%s-%s.rrd" % (ROOT_PATH[0],str(ip),str(port))
		if os.path.isfile(fp):
			os.remove(fp)
		ret = rrdtool.create(fp,"--step","300","--start","0",
		"DS:Indata:COUNTER:600:U:U",
                "DS:Outdata:COUNTER:600:U:U",
                "RRA:AVERAGE:0.5:1:600",
                "RRA:AVERAGE:0.5:4:700",
                "RRA:AVERAGE:0.5:24:775",
                "RRA:AVERAGE:0.5:228:797")
		if ret:
			return rrdtool.error()

