# coding: utf-8
#!/usr/bin/python
import os,sys
from django.core.management import setup_environ
import netsnmp
#import rrdtool
ROOT_PATH = os.path.split(os.path.abspath(os.path.dirname(__file__)))

string = 'public'
snmpport = '161'
ver = 2

def updaterrd():
        set = os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
        from app.models import Server,Switch 
	server = Server.objects.all()
	switch = Switch.objects.all()
	if set and server:
		for ip in server:
			servercheck(str(ip))
	if switch:
		for ip in switch:
			if ip:
				for port in range(1,int(ip.port)+1):
					switchcheck(str(ip),str(port))
def switchcheck(ip,port):
	fp = "%s/rrd/%s-%s.rrd" % (ROOT_PATH[0],ip,port)
        fd = netsnmp.Session(DestHost=ip,Version=ver,RemotePort=snmpport,Timeout=400000,Retries=1,Community=string)
        Inbytes = netsnmp.Varbind('ifInOctets.'+port)
        Outbytes = netsnmp.Varbind('ifOutOctets.'+port)
        list = [Inbytes,Outbytes]
        output = fd.get(list)
	if output[0]!=None and output[1]!=None:
               ret = rrdtool.update(fp,'N:%s:%s' %(output[0],output[1]))
               if ret:
                       print 'error'

	
def servercheck(ip):
	fd = netsnmp.Session(DestHost=ip,Version=ver,RemotePort=snmpport,Timeout=400000,Retries=1,Community=string)
	Inbytes = netsnmp.Varbind('ifInOctets.2')
	Outbytes = netsnmp.Varbind('ifOutOctets.2')
	list = [Inbytes,Outbytes]
	output = fd.get(list)
	if output[0]!=None and output[1]!=None:
                set = os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
                from app.models import Server
                datas = Server.objects.get(ip=ip)
                datas.is_avlie = 1
                datas.save()
		cpuupdate(fd,ip)
		memupdate(fd,ip)
		diskupdate(fd,ip)
		netupdate(fd,ip)	
	else:
		set = os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
		from app.models import Server
		datas = Server.objects.get(ip=ip)
		datas.is_avlie = 0
		datas.save()	


def cpuupdate(fd,ip):
       fp = "%s/rrd/%s-cpu.rrd" % (ROOT_PATH[0],str(ip))
       onecpu = netsnmp.Varbind('laLoad.1')
       fivecpu = netsnmp.Varbind('laLoad.2')
       fifteencpu = netsnmp.Varbind('laLoad.3')
       list = [onecpu,fivecpu,fifteencpu]
       output = fd.get(list)
       if output[0]!=None and output[1]!=None:
               ret = rrdtool.update(fp,'N:%s:%s:%s' %(output[0],output[1],output[1]))
               if ret:
                       print 'error'

def memupdate(fd,ip):
       fp = "%s/rrd/%s-mem.rrd" % (ROOT_PATH[0],str(ip))
       membuffer = netsnmp.Varbind('.1.3.6.1.4.1.2021.4.14.0')
       memcache = netsnmp.Varbind('.1.3.6.1.4.1.2021.4.15.0')
       memfree = netsnmp.Varbind('.1.3.6.1.4.1.2021.4.6.0')
       memtotal = netsnmp.Varbind('.1.3.6.1.4.1.2021.4.5.0')
       list = [membuffer,memcache,memfree,memtotal]
       output = fd.get(list)
       if output[0]!=None and output[1]!=None:
               ret = rrdtool.update(fp,'N:%s:%s:%s:%s' %(output[0],output[1],output[2],output[3]))
               if ret:
                       print 'error'

def diskupdate(fd,ip):
       fp = "%s/rrd/%s-disk.rrd" % (ROOT_PATH[0],str(ip))
       Avaldisk = netsnmp.Varbind('hrStorageSize.31')
       Useddisk = netsnmp.Varbind('hrStorageUsed.31')
       list = [Avaldisk,Useddisk]
       output = fd.get(list)
       if output[0]!=None and output[1]!=None:
               ret = rrdtool.update(fp,'N:%s:%s' %(output[0],output[1]))
               if ret:
                       print 'error'



def netupdate(fd,ip):
       fp = "%s/rrd/%s-net.rrd" % (ROOT_PATH[0],str(ip))
       Inbytes = netsnmp.Varbind('ifInOctets.2')
       Outbytes = netsnmp.Varbind('ifOutOctets.2')
       list = [Inbytes,Outbytes]
       output = fd.get(list)
       if output[0]!=None and output[1]!=None:
               ret = rrdtool.update(fp,'N:%s:%s' %(output[0],output[1]))
               if ret:
                       print 'error'

		
if __name__=="__main__":
        lsPath = os.path.split(os.path.realpath(__file__))
        sys.path.insert(0,ROOT_PATH[0])
        import settings
	updaterrd()
			
	
 	
	
