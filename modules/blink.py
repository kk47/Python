#!/usr/bin/env python
# blink the disk light

import commands
import getopt
import sys
import os
import re

class BlinkDisk():
    def __init__(self):
        megacli = '/opt/MegaRAID/MegaCli/MegaCli64'
        self.megacli = megacli

    def resetAll(self):
        
        cmd = 'lspci -v |grep LSI ' 
        status, output = commands.getstatusoutput(cmd)
        if status != 0:
            return False
        if "Logic SAS" in output:
            for cn in xrange(2):
                cmd = 'sas2ircu ' + str(cn) + ' display|grep -A 15 "Enclosure information"|grep -E "Enclosure#|Numslots"|awk -F: \'{print $2}\'|tr -d " "'
                #print cmd
                status, output = commands.getstatusoutput(cmd)
                if status == 0 and output != '':
                    enclosure = output.split('\n')[0]
                    slotnu = output.split('\n')[1]
                    for s in xrange(int(slotnu)):
                        cmd = 'sas2ircu ' + str(cn) + ' locate ' + enclosure + ":" + str(s) + " off"
                        #print cmd
                        output = commands.getoutput(cmd)
                else:
                    continue

        elif "Logic MegaRAID SAS" in output:
            for cn in xrange(2):
                cmd = self.megacli + ' -PDList -a' + str(cn) + ' | egrep \'Enclosure position:|Slot\''
                #print cmd
                status, output = commands.getstatusoutput(cmd)
                if status != 0:
                    continue
                maxslot = 0 
                slot = 0
                enclosure = ''
                for line in output.split('\n'):
                    if "Slot" in line:
                        slot = int(line.split(':')[1].strip())
                        if slot > maxslot:
                            maxslot = slot
                        continue
                    if enclosure == ''and "Enclosure" in line:
                        enclosure = line.split(':')[1].strip()
                for slot in xrange(maxslot + 1):     
                    cmd = self.megacli + ' -PdLocate -stop -physdrv \[' + enclosure + ':' + str(slot) + '\] -a' + str(cn)
                    #print cmd
                    status, output = commands.getoutput(cmd)
                else:
                    continue
        else:
            #print "Can't find disk controller type."
            return False
        return True

    def uuidDrive(self, uuid):

        cmd = 'blkid -U ' + uuid
        status,output = commands.getstatusoutput(cmd)
        if status != 0:
            return False,""
        else:
            drivename = output
            return True,drivename 

    def getSerialNo(self, drivename):
        
        cmd = 'smartctl -a ' + drivename + ' | grep -i "Serial Number:" | awk -F: \'{print $2}\' | tr -d " " '
        status,output = commands.getstatusoutput(cmd)
        if status != 0:
            return False,""
        elif output != '':
            serialno = output
            return True,serialno
        else:
            return False,""
            
    
    def sasBlinkOnoff(self, onoff, uuid='', drivename=''):
       
        if uuid != '' and drivename == '':
            res,drivename = self.uuidDrive(uuid)
            if not res:
                msg = "Can't get drive name."
                return False, msg

        drivename = re.sub("[0-9]+$", "", drivename)
        res,serialno = self.getSerialNo(drivename)
        if not res:
            msg = "Get serial number failed."
            return False, msg
        
        cnlist = ["0","1"]
        slot = ''
        enclosure = ''
        for cn in cnlist:
            cmd = 'sas2ircu ' + cn + ' display | grep -B 7 ' + serialno + ' | grep -E "Slot|Enclosure" | awk -F: \'{print $2}\' | tr -d " "'
            status,output = commands.getstatusoutput(cmd)
            if status != 0:
                continue
            elif output != '':
                enclosure = output.split("\n")[0]
                slot = output.split("\n")[1]
                break
        if slot != '' or enclosure != '': 
            cmd = "sas2ircu " + cn + " locate " + enclosure + ":" + slot + " " + onoff
            status,output = commands.getstatusoutput(cmd)
            if status != 0 :
                msg = "Blinking disk failed."
                return False, msg
            else:
                msg = "Blinking operation succeed."
                return True, msg
        else:
            msg = "Get enclosure and slot failed."
            return False, msg

    def msasBlinkOnoff(self, onoff, uuid='', drivename=''):

        if uuid != '' and drivename == '':
            res,drivename = self.uuidDrive(uuid)
            if not res:
                msg = "Can't get drive name."
                return False, msg

        drivename = re.sub("[0-9]+$","",drivename)
        res,serialno = self.getSerialNo(drivename)
        if not res:
            msg = "Get serial number failed."
            return False, msg
       
        cnlist = ["0","1"]
        slot = ''
        enclosure = ''
        for cn in cnlist:
            cmd = self.megacli + ' -PDList -a' + cn + ' | egrep \'Adapter|Enclosure position:|Slot|Inquiry\' | grep -B 2 "WD-WCC131060931" | grep -v "WD-WCC131060931" |awk -F: \'{print $2}\''
            status,output = commands.getstatusoutput(cmd)
            if status != 0:
                continue
            elif output != '':
                enclosure = output.split("\n")[1].strip()
                slot = output.split("\n")[0].strip()
                break

        if slot != '' and enclosure != '': 
            if onoff.lower() == 'on':
                cmd = self.megacli + ' -PdLocate -start -physdrv \[' + enclosure + ':' + slot + '\] -a' + cn
            elif onoff.lower() == 'off':
                cmd = self.megacli + ' -PdLocate -stop -physdrv \[' + enclosure + ':' + slot + '\] -a' + cn
            status,output = commands.getstatusoutput(cmd)
            if status != 0:
                msg = "Get enclosure and slot failed."
                return False, msg 
            else:
                msg = "Blinking operation succeed."
                return True, msg
        else:
            msg = "Get enclosure and slot failed."
            return False, msg

    def blink(self, onoff, uuid='', drivename=''):
        
        res, blinkway = self.findType(uuid, drivename)
        if not res:
            msg = 'Unsupported blink'
            return False, msg

        if blinkway == "sas": 
            res, msg = self.sasBlinkOnoff(onoff, uuid, drivename)
            if not res:
                return False, msg
            else:
                return True, msg
        elif blinkway == "msas":
            res, msg = self.msasBlinkOnoff(onoff, uuid, drivename)
            if not res:
                return False, msg
            else:
                return True, msg
        else:
            msg = 'Unsupported blink'
            return False, msg
             

    def findType (self, uuid='', drivename=''):
        
        adapteraddr = ''
        blinkway = ''

        if uuid != '' and drivename == '':
            res, drivename = self.uuidDrive(uuid)
            if not res:
                return False, ''
        if len(drivename) == 0:
            return False, ''
            
        drivename = re.sub("[0-9]+$","",drivename)
        drivename = drivename[5:]
        cmd = 'ls -l /dev/disk/by-path/ | grep -E ' + drivename + '$ | awk \'{print $9}\'|awk -F\'-\' \'{print $2}\''
        status, output = commands.getstatusoutput(cmd)
        if status == 0:
            adapteraddr = output[5:]
        cmd = 'lspci -v |grep LSI | grep ' + adapteraddr
        status, output = commands.getstatusoutput(cmd)
        if status == 0:
            if "Logic SAS" in output:
                blinkway = "sas"
            elif "Logic MegaRAID SAS" in output:
                blinkway = "msas"
            else:
                pass
        if blinkway == '':
            return False, ''
        else:
            return True, blinkway
            
def usage():
    u = """
    Name:
        python %s - blinking disk according to drivename
    
    Synopsis:
        python %s [-h] [-d drivename|-u uuid] [-e enable[on|off]]
    
    Example:
        python %s -d /dev/sdb -e on
        python %s -d /dev/sdc1 -e off
        python %s -u e708619d-9c2e-47f3-9218-084d53c371d5 -e off
    """
    prog = os.path.basename(sys.argv[0])
    print "Usage :"
    print u % (prog,prog,prog,prog,prog)
        
if __name__ == "__main__":
    drivename = ''
    onoff = ''
    uuid = ''
    reset = False
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hsu:d:e:")
    except getopt.GetoptError, msg:
        sys.exit(1)
   
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit(0)
        elif opt == '-u':
            uuid = arg
        elif opt == '-s':
            reset = True
        elif opt == '-d':
            drivename = arg
        elif opt == '-e':
            onoff = arg
        else:
            usage()
            sys.exit(1)
    
    bd = BlinkDisk()
    
    if reset:
        bd.resetAll()
        sys.exit(0)

    if onoff != '':
        if drivename != '' or uuid != '':
            res,msg = bd.blink(onoff, uuid, drivename)
            if not res:
                print msg
                sys.exit(1)
            else:
                print msg
        else:
            usage()
            sys.exit(1)
    else:
        usage()
        sys.exit(1)
