#!/usr/bin/env
import time
import logging

class Profiler(object):

    def _profiler(func):
        def func_wrapper(self, *args, **kwargs):
            start_time = time.time()
            res = func(self, *args, **kwargs)
            logging.warning("Function %s spend %s", func.__name__, time.time() - start_time)
            return res
        return func_wrapper
    
    @_profiler
    def foo(self, arg1, arg2):
        msg = "A message, %s %s" % (arg1, arg2)
        time.sleep(2)
        return True, msg 

    @_profiler
    def bar(self, arg1):
        msg = "A message, %s" % arg1
        time.sleep(3)
        return True, msg 

if __name__ == "__main__":
    
    t = Profiler()
    print t.foo("Lucky", 'boy')
    print t.bar('Handsome')
