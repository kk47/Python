# coding: utf-8
from django.db import models

class Room(models.Model):
        U_NUMBER = (
                (u'世纪互联','世纪互联'),
                (u'鹏博士IDC','鹏博士IDC'),
                (u'兆维','兆维')
        )
        jifang = models.CharField(verbose_name="机房名称",max_length=10,choices=U_NUMBER,default=0)
        jigui = models.CharField(verbose_name="机柜号",max_length=20,unique=True)
        start_time = models.DateTimeField(verbose_name="起始时间")
        end_time = models.DateTimeField(verbose_name="截止时间")
        class Meta:
                verbose_name="机房"
                verbose_name_plural="机房"

        def __unicode__(self):
                return self.jigui



class Switch(models.Model):
        U_device = (
                (u'route','route'),
                (u'switch','switch'),
		(u'firewall','firewall')
        )
        ip = models.IPAddressField(verbose_name="IP",max_length=50,unique=True)
        device = models.CharField(verbose_name="设备类型",max_length=10,choices=U_device,default=0)
        devices = models.CharField(verbose_name="设备型号",max_length=60)
	port = models.IntegerField(max_length=2,verbose_name='交换机总口数')
	paihao = models.IntegerField(max_length=2, verbose_name='交换机位置')
        idroom = models.ForeignKey(Room,on_delete=models.PROTECT)

	def __unicode__(self):
		return self.ip




class Mac(models.Model):
        U_NUMBER = (
                (u'1U','1U'),
                (u'2U','2U'),
                (u'4U','4U'),
                (u'6U','6U'),
                (u'刀片机','刀片机')
        )
	
	DISK = (
		(u'146G*6','146G*6'),
		(u'146G*8','146G*8'),
		(u'300G','300G'),
		(u'300G*6','300G*6'),
		(u'300G*8','300G*8'),
		(u'500G*6','500G*6'),
		(u'500G*8','500G*8'),
		(u'1TB*6','1TB*6'),
		(u'1TB*8','1TB*8'),
		(u'2TB*6','2TB*6'),
		(u'2TB*8','2TB*8')
	)		

	MEM = (
		(u'4G*2','4G*2'),
		(u'4G*3','4G*3'),
		(u'4G*4','4G*4'),
		(u'4G*5','4G*5'),
		(u'4G*6','4G*6'),
		(u'4G*7','4G*7'),
		(u'4G*8','4G*8'),
		(u'4G*9','4G*9'),
		(u'4G*10','4G*10'),
		(u'4G*12','4G*12'),
		(u'4G*14','4G*14'),
		(u'4G*16','4G*16'),
		(u'4G*18','4G*18')
	)
	eth0 = models.CharField(verbose_name="eth0 MAC",max_length=50,unique=True)
        eth1 = models.CharField(verbose_name="eth1 MAC",max_length=50,unique=True)
        eth2 = models.CharField(verbose_name="eth2 MAC",max_length=50,unique=True)
        eth3 = models.CharField(verbose_name="eth3 MAC",max_length=50,unique=True)
        qcode = models.CharField(verbose_name="快速服务代码",max_length=50,unique=True)
        cpu = models.CharField(verbose_name="CPU",max_length=30)
        mem = models.CharField(verbose_name="内存",max_length=30,choices=MEM,default=0)
        disk = models.CharField(verbose_name="硬盘",max_length=30,choices=DISK,default=0)
	uname = models.CharField(verbose_name="U数",max_length=10,choices=U_NUMBER,default=0)
	paihao = models.IntegerField(max_length=2, verbose_name='服务器位置')
	idroom = models.ForeignKey(Room,on_delete=models.PROTECT)
        def __unicode__(self):
                return self.eth0,self.eth1,self.eth2,self.eth3



class Server(models.Model):
        U_device = (
                (u'server','server'),
		(u'vm','vm')
        )
        ip = models.IPAddressField(verbose_name="IP",max_length=50,unique=True)
	device = models.CharField(verbose_name="设备类型",max_length=10,choices=U_device,default=0)
	devices = models.CharField(verbose_name="设备型号",max_length=60)
        mouth = models.IntegerField(verbose_name="对联交换口",max_length=2)
        fuwu = models.CharField(verbose_name="运行服务",max_length=30)
        version = models.CharField(verbose_name="服务版本",max_length=30)
        ports = models.IntegerField(verbose_name="服务端口",max_length=2)
        configid = models.CharField(verbose_name="Configld",max_length=30)
        whoandyou = models.CharField(verbose_name="被谁依赖",max_length=30)
	youandwho = models.CharField(verbose_name="依赖于谁",max_length=30)
	start_time = models.DateTimeField(verbose_name="起始时间")
	end_time = models.DateTimeField(verbose_name="截至时间")
	is_avlie = models.IntegerField(max_length=1,verbose_name="机器是否存活",default=1)
        idroom = models.ForeignKey(Room,on_delete=models.PROTECT)
        idmac = models.ForeignKey(Mac,on_delete=models.PROTECT,related_name='Mac__paihao')
	idswitch = models.ForeignKey(Switch,on_delete=models.PROTECT)

        def __unicode__(self):
                return self.ip

class Repair(models.Model):
        repair = models.TextField(verbose_name="维修记录",max_length=100)
        idmac =  models.ForeignKey(Mac,on_delete=models.PROTECT)

        def __unicode__(self):
                return self.repair
