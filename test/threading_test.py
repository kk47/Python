#!/usr/bin/env python

import sys
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
    
    '''a1 = "kk"
    
    p = multiprocessing.Process(target=fun, args=("a1",))
    p.daemon = True
    p.start()
    
    t = threading.Thread(target=fun, args=(a1))
    t.setDaemon(True)
    t.start()
    #t.join()'''

    sub1 = subprocess.Popen('./prog1.sh'.split(), stdout=subprocess.PIPE)
    sub2 = subprocess.Popen('./prog2.sh'.split(), stdout=subprocess.PIPE)

    sublist = [sub1, sub2]
    
    com_list = []
    while len(com_list) != 2:
        for sub in sublist:
            out = sub.stdout.readline()
            if not out and sub.poll() != None:
                if sub not in com_list:
                    com_list.append(sub)
            if out:
                sys.stdout.write(out)
