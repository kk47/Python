#!/usr/bin/env python
# --*coding:utf-8*--
# manager alert message , include list, set, edit, clear, delete.

import sys, os
import getopt
import commands
import socket 
import datetime
import fcntl
import shutil
import smtplib
import dayu_client
import cms_pb2
import alertconf

class AlertMgmt():
    
    def __init__(self):
        alertpath = "/dayudata/cms/message/alerts/"
        notifipath = "/dayudata/cms/message/notifis/"
        self.alertpath = alertpath
        self.notifipath = notifipath
        threshold = 1000
        self.threshold = threshold

    def check(self, type="ALERT"):
        ''' check alert file path , delete old files when directory is large enough.'''
        if type == "NOTIFI":
            msgpath = self.notifipath
        elif type == "ALERT":
            msgpath = self.alertpath
        else:
            msg = "wrong message type"
            return False, msg

        if not os.path.exists(msgpath):
            msg = '%s not exists.' % msgpath
            return False, msg, ''
        beyond = False
        if len(os.listdir(msgpath)) > self.threshold:
            beyond = True
        return True, beyond
        
    def list(self, num, beginseq='', skipnum='', reverse=False, delflag=False, type="ALERT"):
        ''' list alert message , called by dayugui.py , return protobuf object.
        num : message numbers of every page, beginseq: the first one of every page,
        skipnum: skipnum/num is page numbers for jump, reverse: true means pageup,
        delflag: true means delete old alert messages, type: classify of message can be set to ALERT and NOTIFI'''
        
        if type == "ALERT":
            msgpath = self.alertpath
        elif type == "NOTIFI":
            msgpath = self.notifipath
        else:
            msg = "wrong message type"
            return False, msg, '', '', '' 

        if not os.path.exists(msgpath):
            os.makedirs(msgpath)
         
        try:
            alertfiles = os.listdir(msgpath)
        except Exception, e:
            return False, e.__doc__, '', '', ''
        num=int(num)
        total = len(alertfiles)

        # check and delete old alert files.
        if delflag == True:
            rmlist = alertfiles[self.threshold:] 
            res, msg = self.delete(rmlist)
            if not res:
                return False, msg, '', '', ''

        # sort the message files by timeseq number from small to large
        # which means alertfiles[0] is the earliest and alertfiles[max] is latest.
        alertfiles.sort(reverse=True)

        if beginseq != '':
            if type(reverse) != bool:
                msg = 'the para reverse is not type bool.'
                return False, msg, '', '', ''
            if not reverse :
                if skipnum == '':
                    #this is for list 'num' alert from beginseq
                    cur = alertfiles.index(str(beginseq))
                else:
                    #this is for pagedown and jump down
                    if alertfiles.index(str(beginseq)) + int(skipnum) >= total:
                        cur = alertfiles.index(str(beginseq))
                    else:
                        cur = alertfiles.index(str(beginseq)) + int(skipnum)
            else:
                if skipnum == '':
                    #this is for pageup 
                    if alertfiles.index(str(beginseq)) < num:
                        cur = 0
                    else:
                        cur = alertfiles.index(str(beginseq)) - num
                else:
                    #this is for jump forward from beginseq
                    if int(skipnum) > alertfiles.index(str(beginseq)):
                        cur = 0
                    else:
                        cur = alertfiles.index(str(beginseq)) - int(skipnum)
            maxfiles = alertfiles[cur:cur+num]
            pagenum = cur/num + 1
        else:
            if type(reverse) != bool:
                msg = 'the para reverse is not type bool.'
                return False, msg, '', '', ''
            if not reverse:
                if skipnum == '':
                    #this is normal list 'num' alert, also home page
                    maxfiles = alertfiles[:num]
                    pagenum = 1
                else:
                    #this is jump 'skipnum' alert from home page 
                    maxfiles = alertfiles[int(skipnum):num]
                    pagenum = int(skipnum)/num + 1
            else:
                if skipnum == '':
                    #this is end page
                    if total % num == 0:
                        cur = (total/num - 1) * num
                        pagenum = total/num
                    else:
                        cur = total/num * num
                        pagenum = total/num + 1
                    maxfiles = alertfiles[cur:]
                else:
                    #this is jump 'skipnum' alert from end page
                    cur = int(skipnum) + num
                    maxfiles = alertfiles[-cur:-int(skipnum)]
                    pagenum = total/num + 1 - skipnum/num
                
        res, msg, alerts = self.getPbstr(maxfiles, type)
        if not res:
            return False, msg, '', '', ''
        return True, '', alerts, total, pagenum

    def getPbstr(self, msglist):
        if len(msglist) < 1:
            msg = "message list is empty"
            return False, msg, ''
        
        als = cms_pb2.Alerts()
        al = cms_pb2.Alert()

        for file in msglist:
            try:
                f = open(os.path.join(msgpath, file), 'r')
                ap = f.read()
                f.close()
                if num > 1:
                    tmp = als.alert.add()
                else:
                    return True, '', ap, total, pagenum
                al.ParseFromString(ap)
                tmp.seqno = al.seqno
                tmp.level = al.level
                tmp.date = al.date
                tmp.subject = al.subject
                tmp.action = al.action
                tmp.desc = al.desc
                tmp.markread = al.markread
                tmp.type = al.type
            except Exception, e:
                return False, e.__doc__, ''
        alerts = als.SerializeToString()
        return True, '', alerts
        
    def set(self, para):
        ''' set alert message , stored in files. '''
        options = para.strip('\'').split('|||')
        if len(options) != 4:
            msg = "Invalid alert format"
            return False, msg  
        
        res, cfgdict = SendAlert.loadCfg()
        if not res:
            msg = 'Load nodes.cfg failed.'
            return False, msg

            
        cms_ips = cfgdict['cms_ips']
        eenvid = cfgdict['eenvid']
        if "@]" in options[1]:
            subject = options[1].split(']',1)[0] + eenvid + ']' + options[1].split(']',1)[1]
        else:
            subject = options[1].strip()
        
        alert = cms_pb2.Alert()
        now = datetime.datetime.now()
        alert.seqno = int(now.strftime("%s"))
        alert.level = options[0].strip()
        alert.date = now.strftime("%Y-%m-%d %H:%M")
        alert.subject = subject
        alert.action = options[2].strip()
        alert.desc = options[3].strip()
        alert.markread = False

        if options[0].upper() == "NOTIFI":
            alert.type = "NOTIFI"
            msgpath = self.notifipath
        elif options[0].upper() == "ALERT":
            alert.type = "ALERT"
            msgpath = self.alertpath
        else:
            msg = "wrong message type"
            return False, msg

        filename = str(alert.seqno)
        filepath = os.path.join(msgpath, filename)
        tmppath = '/tmp/' + filename
        try:
            a = alert.SerializeToString()
            f = open(tmppath, "a")
            f.write(a)
            f.close()
            for cms in cms_ips:
                cmd = '/usr/bin/scp ' + tmppath + ' root@' + cms + ':' + filepath
                status,output = commands.getstatusoutput(cmd)
                if status == 0:
                    break
                else:
                    continue
            if status != 0:
                return False, output
            os.remove(tmppath)
        except Exception, e:
            return False, e.__doc__
        return True, ''
            
    def touch(self, seqno, type="ALERT"):
        ''' flash alert message files , change markread flag. '''
        filename = str(seqno)
        if type == "NOTIFI":
            msgpath = self.notifipath
        elif type == "ALERT":
            msgpath = self.alertpath
        else:
            msg = "wrong message type"
            return False, msg
                
        filepath = os.path.join(msgpath, filename)
        if not os.path.exists(filepath):
            msg = '%s not exists.' % filepath
            return False, msg

        alert = cms_pb2.Alert()
        bakpath = filepath + '-'
        tmppath = filepath + '.tmp'
        try:
            shutil.copyfile(filepath, bakpath)
            shutil.copyfile(filepath, tmppath)
            f = open(tmppath, 'r+')
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            fc = f.read()
            alert.ParseFromString(fc)
            alert.markread = True
            fc = alert.SerializeToString()
            f.seek(0)
            f.truncate()
            f.write(fc)
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            f.close()
            os.rename(tmppath, filepath)
            os.remove(bakpath)

        except Exception, e:
            return False, e.__doc__

        return True, ''

    def delete(self, rmlist, type="ALERT"):
        ''' delete alert message by seqno '''
        
        if type == "NOTIFI":
            msgpath = self.notifipath
        elif type == "ALERT":
            msgpath = self.alertpath
        else:
            msg = "wrong message type"
            return False, msg

        for filename in rmlist:
            filepath = os.path.join(msgpath, filename)
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except Exception, e:
                    msg = 'Delete %s failed : %s' % (filepath, e.__doc__)
                    return False, msg
        return True, ''
        
    def rmalert(self, seqlist, type="ALERT"):
        ''' move alert messages from alerts dir to backup dir'''

        if type == "NOTIFI":
            msgpath = self.notifipath
        elif type == "ALERT":
            msgpath = self.alertpath
        else:
            msg = "wrong message type"
            return False, msg
        bakdir = '/dayudata/cms/alert_backup/' + type.lower()

        try:
            if not os.path.exists(bakdir):
                os.mkdir(bakdir)
            if type(seqlist) == list:
                for filename in seqlist:
                    filepath = os.path.join(msgpath, filename)
                    bakpath = bakdir + filename
                    os.rename(filepath,bakpath)
            else: 
                filepath = os.path.join(msgpath, str(seqlist))
                bakpath = bakdir + str(seqlist)
                os.renmae(filepath, bakpath)
            return True, '' 
        except Exception, e:
            return False, e.__doc__

class SendAlert():
    
    nodecfg = '/var/local/dayu/nodes.cfg'
    def __init__(self):
        dayudir = '/usr/local/dayu/'
        alertlog = '/var/log/dayu/alert.log'
        smsshell = dayudir + 'scripts/dayusmssend'
        self.dayudir = dayudir
        self.alertlog = alertlog
        self.smsshell = smsshell
        al = AlertMgmt()
        self.al = al

    @classmethod 
    def loadCfg(cls):
        try:
            nodecfg = cls.nodecfg
            f = open(nodecfg, "r")
            lines = f.readlines()
            f.close()
        except IOError, e:
            print 'open cfg file failed'
            return False, e

        cms_ips = []
        mailto = []
        cfgdict = {}
        for line in lines:
            if line.startswith('CMSES'):
                vec = line.split('=')
                if len(vec) != 2 :
                    msg = 'failed to get CMS hosts'
                    return False, msg
                chosts = vec[1].strip().split(' ')
                if len(chosts) == 1:
                    cfgdict['cms_vip'] = chosts[0]
                for ep in chosts:
                    if len(ep) != 0:
                        cms_ips.append(ep.strip())
                cfgdict['cms_ips'] = cms_ips
                continue
            if line.startswith('CMS_VIP='):
                vec = line.split('=')
                if len(vec) != 2 :
                    continue
                cfgdict['cms_vip'] = vec[1].strip()
                continue
            
            if line.startswith('EMAIL_ALERT'):
                vec = line.split('=')
                if len(vec) != 2 :
                    continue
                if vec[1].strip().lower() == 'true':
                    cfgdict['alertmail'] = True
                else:
                    cfgdict['alertmail'] = False
            if line.startswith('SEND_ALERT_TO'):
                vec = line.split('=')
                if len(vec) != 2 :
                    continue
                maillist = vec[1].strip().split(' ')
                for m in maillist:
                    if len(m) != 0:
                        mailto.append(m)
                        cfgdict['mailto'] = mailto
                continue
            if line.startswith('EMAIL_HUB'):
                vec = line.split('=')
                if len(vec) != 2 :
                    continue
                cfgdict['mailhub'] = vec[1].strip()
                continue
            if line.startswith('EMAIL_USER'):
                vec = line.split('=')
                if len(vec) != 2 :
                    continue
                cfgdict['mailuser'] = vec[1].strip()
                continue
            if line.startswith('EMAIL_PWD'):
                vec = line.split('=')
                if len(vec) != 2 :
                    continue
                cfgdict['mailpwd'] = vec[1].strip()
                continue
            if line.startswith('EMAIL_ENV_ID'):
                vec = line.split('=')
                if len(vec) != 2 :
                    continue
                cfgdict['eenvid'] = vec[1].strip()
                continue
            #for sms
            if line.startswith('SMS_ALERT'):
                vec = line.split('=')
                if len(vec) != 2 :
                  continue
                if vec[1].strip().lower() == 'true':
                    cfgdict['alertsms'] = True
                else:
                    cfgdict['alertsms'] = False
                continue
            if line.startswith('SMS_SENDTO'):
                vec = line.split('=')
                if len(vec) != 2 :
                    continue
                cfgdict['smssendto'] = vec[1].strip()
                continue
            if line.startswith('SMS_SHELL'):
                vec = line.split('=')
                if len(vec) != 2 :
                    continue
                cfgdict['smsshell'] = vec[1].strip()
                continue
        return True, cfgdict              

    def sendMail(self, para, mailto=''):
        '''Send mail to mail address according to nodes.cfg config , or send to the given address''' 
        
        res, cfgdict = self.loadCfg()
        if not res:
            msg = 'Load nodes.cfg failed.'
            return False, msg
        
        cms_ips = cfgdict['cms_ips']
        mailscript = self.dayudir + 'scripts/dayumail.py'
        ssh = '/usr/bin/ssh -o StrictHostKeyChecking=no '
        try :
            if not os.path.exists(mailscript):
                msg = 'The scripts of send mail not exists.'
                return False, msg
            # read first line to check whether is shell or python scripts
            cmd = mailscript + " -p \' " + para + "\' -m \' " + mailto + " \'"
            for cms in cms_ips:
                cms = 'root@' + cms
                mailcmd = ssh + cms + ' \" ' + cmd + '\"'
                status,output = commands.getstatusoutput(mailcmd)
                if status == 0:
                    break
                else:
                    continue
            
            if status != 0:
                return False, output
        except Exception, e:
            return False, e.__doc__
        return True, ''

    def sendSms(self, para, smssendto=''):
        '''Send short message according to nodes.cfg config , or send to the given phone number'''

        res, cfgdict = self.loadCfg()
        if not res:
            msg = 'Load nodes.cfg failed.'
            return False, msg
        
        cms_ips = cfgdict['cms_ips']
        alertsms = cfgdict['alertsms']
        if smssendto == '':
            smssendto = cfgdict['smssendto']

        smsshell = cfgdict['smsshell']
        if len(smsshell) == 0:
            smsshell = self.smsshell
        eenvid = cfgdict['eenvid']

        options = para.strip('\'').split('|||')
        if len(options) != 4:
            msg = "Invalid alert format"
            return False, msg
        if alertsms == False:
            msg = "alert sms is disable, do nothing"
            return False, msg
        if len(smssendto) == 0:
            msg = "none recive phone given"
            return False, msg
        if "@]" in options[1]:
            subject = options[1].split(']',1)[0] + eenvid + ']' + options[1].split(']',1)[1]
        else:
            subject = options[1].strip()
        ssh = '/usr/bin/ssh -o StrictHostKeyChecking=no '
        try :
            smsshell = os.path.abspath(self.smsshell)
            if not os.path.exists(smsshell):
                msg = 'The scripts of send short message not exists.'
                return False, msg
            # read first line to check whether is shell or python scripts
            cmd = smsshell + " -p '" + smssendto + "' -s '" + subject + "'"
            for cms in cms_ips:
                cms = 'root@' + cms
                smscmd = ssh + cms + ' \"' + cmd + '\"'
                status,output = commands.getstatusoutput(smscmd)
                if status == 0:
                    break
                else:
                    continue
            if status != 0:
                return False, output
                
        except Exception, e:
            return False, e.__doc__
        return True, ''

    def reportToCms(self, para):
        '''Report the alert message to cms node'''
        
        res, cfgdict = self.loadCfg()
        if not res:
            msg = 'Load nodes.cfg failed.'
            return False, msg
        cms_vip = cfgdict['cms_vip']
        eenvid = cfgdict['eenvid']
   
        options = para.strip('\'').split('|||')
        if len(options) != 4:
            msg = "Invalid alert format"
            return False, msg
        
        if "@]" in options[1]:
            subject = options[1].split(']',1)[0] + eenvid + ']' + options[1].split(']',1)[1]
        else:
            subject = options[1].strip()

        try :
            sclient = dayu_client.SimpleClient()
            req = cms_pb2.ReportAlertReq()
            req.host = socket.gethostname()
            req.alert.level = options[0].strip()
            now = datetime.datetime.now()
            req.alert.date = now.strftime("%Y-%m-%d %H:%M") 
            req.alert.subject = subject
            req.alert.action = options[2].strip()
            req.alert.desc = options[3].strip()
            endpoint = (cms_vip, 8003)
            resp = sclient.send(endpoint, req)
            if resp:
                if resp.status.errcode != 0:
                    return False, resp
                return True, ''
        except Exception,e:
            msg = 'failed to report alert to CMS'
            #traceback.print_exc(file=sys.stdout)
            #traceback.print_exc(limit=1, file=sys.stdout)
            return False, msg
    
    def send(self, para):
        '''Send alert message use email or short message and report to cms node'''
        
        msg = ""
        res1, msg1 = self.al.set(para)
        if not res1:
            msg = "set alert,"
        res2, msg2 = self.sendSms(para)
        if not res2:
            msg += "send short message,"
        res3, msg3 = self.sendMail(para)
        if not res3:
            msg += "send mail,"
        res4, msg4 = self.reportToCms(para)
        if not res4:
            msg += "report to cms"
        if not res1 or not res4:
            now = datetime.datetime.now().strftime("%b %d %T")
            msg = now + " Failed to " + msg
            return False, msg

        return True, ''

def usage():
    u = """
    Name:
        %s - dayu alert message management
    
    Synopsis:
        %s [-h] [-c command] [-p options] 
    
    Description:
        Arguments are as following:
            -h      print the help message
            -c      command list:
                        SetAlert      
                        ListAlert
                        TouchAlert
                        SendMail
                        SendSms
                        ReportToCms
                        SendAlert
            -p      command parameters       
            -n      list alert number
    """
    prog = os.path.basename(sys.argv[0])
    print "Usage :"
    print u %(prog, prog)


if __name__ == "__main__":
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:p:n:")
    except getopt.GetoptError, msg:
        print msg
        sys.exit(1)
    cmd = ''
    para = ''
    num = '1'
    for opt, arg in opts:
        if opt == "-h":
            usage()
            sys.exit(0)
        elif opt == "-c":
            cmd = arg
        elif opt == "-p":
            para = arg.strip()
        elif opt == "-n":
            num = arg
        else:
            usage()
            sys.exit(1)

    if len(cmd) == 0:
        usage()
        sys.exit(1)
    
    al = AlertMgmt()
    aps = cms_pb2.Alerts()
    ap = cms_pb2.Alert()

    sa = SendAlert()

    if cmd == "SetAlert":
        res, msg = al.set(para)
        print msg
    elif cmd == "ListAlert":
        res, msg, alerts, total, pagenum = al.list(num, type="notifi")
        if int(num) > 1: 
            aps.ParseFromString(alerts)
            print aps
        else:
            ap.ParseFromString(alerts) 
            print ap
             
    elif cmd == "TouchAlert":
        res, msg = al.touch(para)
        if not res:
            print msg
    elif cmd == "SendMail":
        res, msg = sa.sendMail(para) 
        if not res:
            print msg
    elif cmd == "SendSms":
        res, msg = sa.sendSms(para)
        if not res:
            print msg
    elif cmd == "ReportToCms":
        res, msg = sa.reportToCms(para)
        if not res:
            print msg
    elif cmd == "SendAlert":
        res, msg = sa.send(para)
        if not res:
            print msg
    else:
        print "unknow command : %s" % cmd
        usage()
        sys.exit(1)
