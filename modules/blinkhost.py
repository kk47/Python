#!/usr/bin/env python
# running blink.py in any 
import commands

class BlinkDiskHost():
   
    def blinkHost(self, host, onoff, uuid='', drivename=''):
        path = "/usr/local/dayu/python/blink.py "
        ssh = "ssh -o User=root -o StrictHostKeyChecking=no "

        if uuid != '' and drivename == '':
            cmd = "/usr/bin/python " + path + " -u " + uuid + " -e " + onoff
        elif uuid == '' and drivename != '':
            cmd = "/usr/bin/python " + path + " -d " + drivename + " -e " + onoff
        else:
            msg = 'parameter error'
            return False, msg 
        
        pcmd = ssh + host + ' "' + cmd + ' "'
        status,output = commands.getstatusoutput(pcmd)
        if status != 0:
            return False, output
        else:
            return True, ''

    def resetHost(self, host):

        path = "/usr/local/dayu/python/blink.py "
        ssh = "ssh -o User=root -o StrictHostKeyChecking=no "

        cmd = "/usr/bin/python " + path + " -s"
        pcmd = ssh + host + ' "' + cmd + ' "'
        status,output = commands.getstatusoutput(pcmd)
        if status != 0:
            return False, output
        else:
            return True, '' 
        
