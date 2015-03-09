import os,sys
import re
import commands
import ping
import subprocess
import getopt
import threading
import socket,fcntl,struct
import time
import cms_pb2
import clustrun_pb2

reload(sys)

sys.setdefaultencoding('utf8')
class ClusterRun() :
    '''running command on full dayu cluster and get return message.
       you can run this module at command line.'''
    def __init__(self):
        self.mutex = threading.RLock() 
        
    def pingTest(self,host) :
        try :
            retcode = ping.quiet_ping(host,timeout=1,count=1)[0]
            if retcode != 0 :
                return False
            else :
                return True
        except :
            return False

    def setCron(self,cmd,host) :
        ''' set the running failed command to cron job list'''
        dir = '/mnt/dayu/.dayu/failedcmd/' + host + "/"
        try : 
            os.listdir('/mnt/dayu/.dayu')
            file = dir + str(time.time())
        
            if not os.path.isdir(dir):
                os.makedirs(dir)
            
            with open(file,"w") as f:
                f.write(cmd)
        except Exception,e:
            return e
        
    
    def getNodesInfo(self):
        '''get the hostlist from nodes.cfg'''
        nodelist=[]
        with open('/var/local/dayu/nodes.cfg') as f:
            for line in f:
                if line.startswith('HOSTS'):
                    nodelist = line.split('=')[1].strip()
        return nodelist

    def runAll(self,action) :
        ''' receive an protobuf object from parm and return a protobuf object
            running command on all nodes,get retrun msg and code from command line'''
        global rdict 
        global netlose
        cmd = action.cmd
        netflag = 0
        runflag = 0
        dnode = action.hostname
        res = clustrun_pb2.Results()
        
        if dnode == [] :
            dnode = self.getNodesInfo()
            dnode = dnode.split()
        
        l = []
        rdict = {}
        output = []
        try:
            for host in dnode:
                if not self.pingTest(host):
                    self.setCron(cmd,host) 
                    rdict[host]='1=1=Connection failed'
                else:
                    t = threading.Thread(target=self.singleRun,args=(host,cmd))
                    t.setDaemon(True)
                    t.start()
                    l.append(t)
        except:
            raise    
        #use t.join() to wait threading complete. 
        for t in l:
            t.join()
        for host in dnode:
            result = res.reses.add()
            result.host = host
            if rdict[host].split('=',2)[0] == '1':
                netflag += 1
            if rdict[host].split('=',2)[1] != '0':
                runflag += 1 
            result.status.errcode = int(rdict[host].split('=',2)[1])
            result.status.errmsg = rdict[host].split('=',2)[2]
            
        if netflag == 0 and runflag == 0 :
            res.rcode = 0
        elif runflag == 0:
            res.rcode = 1
        else :
            res.rcode = 2 
        return res
    
    def singleRun(self,host,cmd):
        global rdict
        runlose = False
        output=[]
        status = 1
        try :
            ssh = "ssh -o User=root -o StrictHostKeyChecking=no "
            pcmd = ssh + host + " " + '"' + cmd + '"'
            status,output = commands.getstatusoutput(pcmd)
            output = output.decode("utf8")
            if status != 0:
                runlose = True
                status = status >> 8
        except Exception, e:
            status = 1
            output = str(e)

        #deal with global object and paramaters,use dict, like 'neterror=runerror=msg'     
        if self.mutex.acquire(1):
            if host not in rdict.keys():
                if status != 0:
                    runlose = True
                    rdict[host]='0=' + str(status) + '=' + output
                else :
                    rdict[host]='0=0=' + output
            self.mutex.release()

    def getIpAddr(self,ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
                    s.fileno(),
                    0x8915, # SIOCGIFADDR 
                    struct.pack('256s', ifname[:15])
                    )[20:24])

    def syncAll(self,target):
        dnode = self.getNodesInfo()
        ssh = "ssh -o User=root -o StrictHostKeyChecking=no "
        ifname = ["bond0","em1","eth0"]
        for inte in ifname:
            try:
                ip = self.getIpAddr(inte)
            except IOError,msg:
                continue

        hostname = socket.gethostname()

        if hostname in dnode.split():
            local = hostname
        elif ip in dnode.split():
            local = ip
        else:
            local = 'losthost'

        for host in dnode.split():
            sync = 'tar -cPf - ' + target +'|'+ ssh + ' ' + host + ' tar xPvf - &>/dev/null'
            try :
                #status,output = commands.getstatusoutput(sync)
                p = subprocess.Popen(sync,shell=True)
                pid,retcode = os.waitpid(p.pid, 0)
            except OSError:
                return retcode
            if retcode != 0 :
                self.setCron(sync,local)
         

def Usage(name):
    u = """
    Options:
        -c  command
        -l  the command running node list
        -h  help
    Example:
        python %s -c "ls /root" -l "d01 d02"
    """
    print "usage:"
    print u % name
	
if __name__ == "__main__":
    cmd=""
    dnode=""
    name = os.path.basename(sys.argv[0])
    p = ClusterRun()
    try:
        opts,args = getopt.getopt(sys.argv[1:],"c:l:h")
    except getopt.GetoptError, msg:
        print msg
        sys.exit(1)
    for op,value in opts:    
        if op == "-c":
            cmd = value
        elif op == "-l":
            dnode = value
        elif op == "-h":
            Usage(name)
            sys.exit(1)
        else :
            sys.exit(1)
                
    if cmd == "" or re.match('\s',cmd):
        sys.exit(1)
    action = clustrun_pb2.ClustAct()
    action.cmd = cmd
    if dnode == "" :
        dnode = p.getNodesInfo()
    for i in dnode.split():
        action.hostname.append(i)
    res = p.runAll(action)
    print res 
