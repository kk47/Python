#!/usr/bin/env python
# modify the cfgdir

import os
import sys
import getopt
import re
import types
import shutil
import time
import clustrun
import alertmgmt


class MailConf():

    def __init__(self):
        cfgdir = '/var/local/dayu/nodes.cfg'
        c = clustrun.ClusterRun()
        self.cfgdir = cfgdir
        self.c = c
        tmpcfg = self.cfgdir + '.tmp'
        self.tmpcfg = tmpcfg
        sa = alertmgmt.SendAlert()
        self.sa = sa

    def openFile(self):
        try:
            shutil.copy(self.cfgdir, self.tmpcfg)
            f = open(self.tmpcfg, "r+")
            lines = f.readlines()
            f.close()
        except IOError, iomsg:
            return False, iomsg, ''
        return True, '', lines

    def listMail(self):
        res, msg, lines = self.openFile()
        if not res:
            return False, msg, '', ''
        me = ''
        ml = ''
        for line in lines:
            if line.strip().startswith("EMAIL_ALERT"):
                me = line.rstrip("\n").split("=")
                if me[1].lower() == 'true':
                    me = True
                else :
                    me = False
                continue
            if line.startswith("SEND_ALERT_TO"):
                ml = line.rstrip("\n").split("=")
                ml = ml[1].strip()
                continue
            if me != '' and ml != '':
                break
        return True, "", me, ml

    def enableMail(self, EMAIL_ALERT):
        
        res,msg,lines = self.openFile()
        if not res:
            return False, msg
        try:
            o=open(self.tmpcfg, 'w')
            for line in lines:
                if line.strip().startswith("EMAIL_ALERT"):
                    l = line.split("=")
                    temp = l[0] + "=" + EMAIL_ALERT + "\n"
                    o.write(temp)
                else:
                    o.write(line)
            o.close()
            shutil.copy(self.tmpcfg,self.cfgdir)
            self.c.syncAll(self.cfgdir)
            return True, ''
        except Exception, e:
            return False, e
        
    def addMail(self, address):
        
        res, msg = self.emailCheck(address)
        if not res:
            return False, msg

        res, msg, lines = self.openFile()

        if not lines:
            msg='open nodes.cfg failed'
            return False, msg
        try:
            o=open(self.tmpcfg, 'w')
            for line in lines:
                if line.strip().startswith("SEND_ALERT_TO"):
                    l = line.strip()
                    temp = l + " " + str(address) + "\n"
                    o.write(temp)
                else:
                    o.write(line)
            o.close()
            shutil.copy(self.tmpcfg,self.cfgdir)
            self.c.syncAll(self.cfgdir)
        except Exception, e:
            return False, e
        
        subject = "You have been added to dayufs alert list."
        para = 'Info ||| ' + subject + ' ||| None ||| This message is send by dayufs management.'
        res, msg = self.sa.sendMail(para, mailto=address)
        if not res:
            msg = "Warnning: failed to send notification e-mail."
            return True, msg

        return True, ''

    def deleteMail(self, address):
        
        res, msg, ee, el = self.listMail()
        if address not in el.split():
            msg = 'email address not exist'
            return False, msg
    
        res, msg, lines = self.openFile()
        if not lines:
            return False, msg
        
        try:
            o=open(self.tmpcfg, 'w')
            for line in lines:
                if line.strip().startswith("SEND_ALERT_TO"):
                    l = line.split("=")
                    l1 = l[1].strip(" ")
                    temp = l[0] + "=" + l1.replace(address, "")
                    o.write(temp)
                else:
                    o.write(line)
            o.close()
            shutil.copy(self.tmpcfg,self.cfgdir)
            self.c.syncAll(self.cfgdir)
        except exception, e:
            return False, e

        subject = "You have been deleted from dayufs alert list."
        para = 'Info ||| ' + subject + ' ||| None ||| This message is send by dayufs management.'
        res, msg = self.sa.sendMail(para, address)
        if not res:
            msg = "Warnning: failed to send notification e-mail."
            return True, msg

        return True, msg
    
    def modifyMail(self, address, taddr):

        res, msg = self.emailCheck(taddr)
        if not res:
            return False, msg
        
        res, msg, lines = self.openFile()
        if not lines:
            return False, msg

        try:
            o=open(self.tmpcfg, 'w')
            for line in lines:
                if line.strip().startswith("SEND_ALERT_TO"):
                    l = line.split("=")
                    l1 = l[1].strip(" ")
                    temp = l[0] + "=" + l1.replace(address, taddr)
                    o.write(temp)
                else:
                    o.write(line)
            o.close()
            shutil.copy(self.tmpcfg,self.cfgdir)
            self.c.syncAll(self.cfgdir)
        except Exception, e:
            return False, e

        return True, ''

    def emailCheck(self, address):

        res, msg, ee, el = self.listMail()
        if address != "" and address in el.split():
            msg = "email: %s address already exist" % address
            return False, msg
        #if re.match("^[-a-zA-Z0-9._%+]+@[-a-zA-Z0-9._%]+.[a-zA-Z]{2,6}$",  address) == None:
        if re.match("^([a-zA-Z0-9]+[_|\-|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\-|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$",  address) == None:
            msg = "Wrong email address format : %s" % address
            return False, msg
        return True, ''

class SmsConf():

    def __init__(self):
        cfgdir = '/var/local/dayu/nodes.cfg'
        c = clustrun.ClusterRun()
        self.cfgdir = cfgdir
        self.c = c         
        sa = alertmgmt.SendAlert()
        self.sa = sa

        f = open(self.cfgdir, "r+")
        lines = f.readlines()
        f.close()
        
        if "SMS_ALERT" and "SMS_SENDTO" and "SMS_SHELL" not in str(lines):
            f = open(self.cfgdir,"a")
            f.write('SMS_ALERT=false\n')
            f.write('SMS_SENDTO=\n')
            f.write('SMS_SHELL=\n')
            f.close()
            self.c.syncAll(self.cfgdir)

        tmpcfg = cfgdir + '.tmp' 
        self.tmpcfg = tmpcfg

    def openFile(self):

        try:
            shutil.copy(self.cfgdir,self.tmpcfg)
            f = open(self.cfgdir, "r+")
            lines = f.readlines()
            f.close()
        except IOError, iomsg:
            return False, iomsg, ''
        return True, '', lines

    def listPhone(self):

        res, msg, lines = self.openFile()
        if not res:
            return False, msg, ''

        pe = '' 
        pl = ''
        for line in lines:
            if line.strip().startswith("SMS_ALERT"):
                pe = line.rstrip("\n").split("=")
                if pe[1].lower() == 'true':
                    pe = True
                else:
                    pe = False
                continue
            if line.startswith("SMS_SENDTO"):
                pl = line.rstrip("\n").split("=")
                pl = pl[1].strip(" ")
                continue
            if pe != '' and pl != '':
                break

        return True, '', pe, pl

    def enableSms(self, SMS_ALERT):

        res, msg, lines = self.openFile()
        if not res:
            return False, msg

        try:
            o=open(self.tmpcfg, 'w')
            for line in lines:
                if line.strip().startswith("SMS_ALERT"):
                    l = line.split("=")
                    temp = l[0] + "=" + SMS_ALERT + "\n"
                    o.write(temp)
                else:
                    o.write(line)
            o.close()
            shutil.copy(self.tmpcfg,self.cfgdir)
            self.c.syncAll(self.cfgdir)
            return True, ''
        except Exception, e:
            return False, e
                    
    def addPhone(self, phone):

        res, msg = self.phoneCheck(phone)
        if not res:
            return False, msg

        res, msg, lines = self.openFile()
        if not res:
            return False, msg

        try:
            o=open(self.tmpcfg, 'w')
            for line in lines:
                if line.strip().startswith("SMS_SENDTO"):
                    l = line.strip()
                    temp = l + " " + str(phone) + "\n"
                    o.write(temp)
                else:
                    o.write(line)
            o.close()
            shutil.copy(self.tmpcfg,self.cfgdir)
            self.c.syncAll(self.cfgdir)
        except Exception, e:
            return False, e

        subject = "You have been added to dayufs alert list."
        para = 'Info ||| ' + subject + ' ||| None ||| This message is send by dayufs management.'
        res, msg = self.sa.sendSms(para, smssendto=phone)
        if not res:
            msg = "Warnning: failed to send notification short message."
            return True, msg
        return True, ''

    def deletePhone(self, phone):
        
        res, msg, se, pl = self.listPhone()
        if phone not in pl.split():
            msg = 'phone number not exist'
            return False,msg

        res, msg, lines = self.openFile()
        if not res:
            return False, msg
        
        try:
            o=open(self.tmpcfg, 'w')
            for line in lines:
                if line.strip().startswith("SMS_SENDTO"):
                    l = line.split("=")
                    l1 = l[1].strip(" ")
                    temp = l[0] + "=" + l1.replace(phone, "")
                    o.write(temp)
                else:
                    o.write(line)
            o.close()
            shutil.copy(self.tmpcfg,self.cfgdir)
            self.c.syncAll(self.cfgdir)

        except Exception, e:
            return False, e

        subject = "You have been deleted from dayufs alert list."
        para = 'Info ||| ' + subject + ' ||| None ||| This message is send by dayufs management.'
        res, msg = self.sa.sendSms(para, smssendto=phone)
        if not res:
            msg = "Warnning: failed to send notification short message."
            return True, msg
        return True, ''

    def modifySms(self, phone, tphone):

        res, msg = self.phoneCheck(tphone)
        if not res: 
            return False, msg

        res, msg, lines = self.openFile()
        if not res:
            return False, msg

        try:
            o=open(self.tmpcfg, 'w')
            for line in lines:
                if line.strip().startswith("SMS_SENDTO"):
                    l = line.split("=")
                    l1 = l[1].strip(" ")  
                    temp = l[0] + "=" + l1.replace(phone, tphone)
                    o.write(temp)
                else:
                    o.write(line)
            o.close()
            shutil.copy(self.tmpcfg,self.cfgdir)
            self.c.syncAll(self.cfgdir)
            return True, ''
        except Exception, e:
            return False, e

    def phoneCheck(self, phone):

        res, msg, se, pl = self.listPhone()
        if phone != "" and phone in pl.split():
            msg = "phone: %s address already exist" % phone
            return False, msg
        #if re.match("^1\d{10}$",  phone) == None:
        if re.match("^(13[0-9]|15[0-9]|17[0-9]|18[0-9]){1}[0-9]{8}$",phone) == None:
            msg = "Wrong phone number format : %s" % phone
            return False, msg
        return True, ''
    
    
def usage():
    u = """
    Options:
            -c  email alert management command, support:
                    add
                    modify
                    delete
            -m  the email address you want operation.
            -p  the phone you want operation
            -l  get the email address list.
            --enable  turn on/off email alert, support:
                    true
                    false
            -h
            --help
            
    Example:
            python %s -c add [-m, -p] support@aggstor.com 
            python %s -c modify [-m, -p] support@aggstor.com -t dayu@aggstor.com
            python %s -c delete [-m, -p] dayu@aggstor.com
            python %s -e '[mail, sms]=[true, false]'
            python %s -l [mail, phone]
    """
    prog = os.path.basename(sys.argv[0])
    print "usage:"
    print u % (prog, prog, prog, prog, prog)


if __name__ == "__main__":

    #cfgdir = '/var/local/dayu/nodes.cfg'
    EMAIL_ALERT = ''
    SMS_ALERT = ''
    cmd = ''
    phone = ''
    address = ''
   # c = clustrun.ClusterRun()
    m = MailConf()
    s = SmsConf()
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hl:c:m:p:t:e:", ["help"])
    except getopt.GetoptError, msg:
        print msg
        sys.exit(1)
    for op, value in opts:
        if op in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif op == "-l":
            if value == 'phone':
                print s.listPhone(), 
                sys.exit(0)
            elif value == 'mail':
                print m.listMail(), 
                sys.exit(0)
            else:
                print 'value of -l option wrong'
                sys.exit(0)
        elif op == "-c":
            cmd = value
        elif op == "-m":
            address=value
        elif op == "-p":
            phone=value
        elif op == "-t":
            if phone != '':
                tphone=value
            else:
                taddr=value
        elif op == "-e":
            if value.startswith('mail'):
                EMAIL_ALERT=value.split('=')[1]
            elif value.startswith('sms'):
                SMS_ALERT=value.split('=')[1]
            else:
                print 'Wrong para of -e'
                sys.exit(1)
        else :
            print "Detect unknow options"

#add cluster model object, use it to run all node

    if EMAIL_ALERT.lower() == 'true' or EMAIL_ALERT.lower() == 'false':
        print m.enableMail(EMAIL_ALERT)
    elif SMS_ALERT.lower() == 'true' or SMS_ALERT.lower() == 'false':
        print s.enableSms(SMS_ALERT)
    else:
        pass
        
    if cmd == "add":
        if phone != '':
            print s.addPhone(phone)
            # c.syncAll(cfgdir)

        elif address != '': 
            print  m.addMail(address)
            # c.syncAll(cfgdir)
        else:
            print 'command add missing next option'
            sys.exit(1)

    elif cmd == "delete":
        if phone != '':
            print s.deletePhone(phone)
            # c.syncAll(cfgdir)
        elif address != '':
            print m.deleteMail(address)
            #  c.syncAll(cfgdir)
        else:
            print 'command delete missing next option'
            sys.exit(1)

    elif cmd == "modify":
        if phone != '':
            print s.modifySms(phone, tphone)
            # c.syncAll(cfgdir)
        elif address != '':
            print m.modifyMail(address, taddr)
            # c.syncAll(cfgdir)
        else:
            print 'command modify missing next option'
            sys.exit(1)

    elif cmd != "" :
        usage() 
