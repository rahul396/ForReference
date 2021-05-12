import threading
from threading import Thread, Event
import time
import re
import urllib.request
import urllib.parse
from multiprocessing import Queue
import requests


class CustomThread(Thread):

    def __init__(self, target=None, args=(), kwargs=None):
        Thread.__init__(self, target=target, args=args, kwargs=kwargs)
        self._stopper = False
        self._target = target
        self._args = args
        self._kwargs = kwargs
        self._queue = Queue()

    def run(self):
        t = Thread(target=lambda q, *args1, **kwargs1: q.put(self._target(*args1, **kwargs1)),args=(self._queue, *self._args), kwargs=self._kwargs)
        # if self._args and not self._kwargs:
        #     t = Thread(target=lambda q, *arg1: q.put(self._target(*arg1)),
        #                args=(self._queue, *self._args))
        #     #t = Thread(target=self._target,args=self._args)
        # elif self._kwargs and not self._args:
        #     t = Thread(target=lambda q, **kwargs1: q.put(self._target(**kwargs1)), args=(self._queue, **self._kwargs))
        #     #t = Thread(target=self._target, kwargs=self._kwargs)
        # elif self._args and self._kwargs:
        #     t = Thread(target=lambda q, *args1, **kwargs1: q.put(self._target(*args1, **kwargs1)),
        #                args=(self._queue, *self._args, **self._kwargs))
        #     #t = Thread(target=self._target,args=self._args, kwargs=self._kwargs)
        # else:
        #     t = Thread(target=lambda q: q.put(
        #         self._target()), args=(self._queue,))
        #   #t = Thread(target=self._target)
        t.daemon = True
        t.start()
        # print(self._stopper)
        # if self._stopper:
        #     raise TimeoutError('Time has passed')
        while True:
            if not t.isAlive():
                break
            if self._stopper:
                raise TimeoutError('Time has passed')

    def stop(self, timeout):
        time.sleep(timeout)
        self._stopper = True


    def get_return_value(self):
        #Thread.join(self,timeout)
        #super(CustomThread, self).join()
        #print('Queue empty: {}'.format(self._queue.empty()))
        #print ("checking queue")
        if not self._queue.empty():
            #print ("queue not empty")
            return self._queue.get()


def counter(limit=0):
    for n in range(limit):
        print('                                      '+str(n))
        time.sleep(1)


def timeout(t):
    def wrapper(fn):
        def wrapped(*args, **kwargs):
            print('{} has been wrapped for {} seconds'.format(fn.__name__, str(t)))
            timer = Thread(target=counter, args=(t,))
            func = CustomThread(target=fn, args=args, kwargs=kwargs)
            timer.start()
            func.start()
            #timer.join()
            #func.join()
            # print (threading.current_thread())
            # Blocking only for t seconds
            #ret_value = func.join(t)
            while True:
                #print ("Timer: "+str(timer.isAlive()))
                #print ("Function: "+str(func.isAlive()))
                if not timer.isAlive() and func.isAlive():
                    print ('Stoping the target thread')
                    func.stop(1)
                    break
                elif not func.isAlive():
                    break
            ret_value = func.get_return_value()

            return ret_value
        return wrapped
    return wrapper



class AppURLopener(urllib.request.FancyURLopener):
    version = "Chrome/70.0"


@timeout(20)
def find_text(urls, search_texts):
    result = []
    opener = AppURLopener()
    for i, url in enumerate(urls):
        #print (url)
        website_data = opener.open(url).read().__str__()
        search_result = re.findall(search_texts[i], website_data)
        result.append(len(search_result))
    print('It completed')
    return result


if __name__ == '__main__':
    urls = ['https://www.toptal.com/python/beginners-guide-to-concurrency-and-parallelism-in-python',
            'https://developers.google.com/edu/python/regular-expressions',
            'https://stackoverflow.com/questions/2275359/jquery-parsejson-throws-invalid-json-error-due-to-escaped-single-quote-in-json']
    search_texts = ('queue', 'pattern', 'quote')
    result = find_text(urls, search_texts)
    print(result)
