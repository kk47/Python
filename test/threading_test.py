#!/usr/bin/env python

import threading
import time
import subprocess
import multiprocessing

def fun(a1):
    print a1 + " going to sleep"
    a = "\0" * 1024 * 1024
    try:
        with open("/mnt/dayu/keventest", 'wb') as f:
            for i in range(100):
                f.write(a)
            f.flush()
    except Exception, e:
        print str(e)
        f.close()
    return

if __name__ == "__main__":
    
    a1 = "kk"
    
    p = multiprocessing.Process(target=fun, args=("a1",))
    p.daemon = True
    p.start()
    
    #subproc = subprocess.Popen([fun,a1], stderr=subprocess.PIPE)
    #print subproc.pid
    '''
    t = threading.Thread(target=fun, args=(a1))
    t.setDaemon(True)
    t.start()
    #t.join()'''
