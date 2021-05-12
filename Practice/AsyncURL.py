from threading import Thread
import time
from urllib2 import urlopen
import re as RegularExpression


# def task_to_run(name,delay,repeat):
# 	while repeat>0:
# 		time.sleep(delay)
# 		website_data = urlopen('https://www.toptal.com/python/beginners-guide-to-concurrency-and-parallelism-in-python')
# 		search_results = re.findall('Thread',website_data.read())
# 		print name+ ' returned'+str(len(search_results))+' matches'
# 		repeat-=1
# 	print name+' has finished'

class AsyncURLOpener(Thread):
    def __init__(self, name, url, search_text):
        Thread.__init__(self)
        self.name = name
        self.url = url
        self.search_text = search_text

    def run(self):
        website_data = urlopen(self.url).read()
        search_results = RegularExpression.findall(self.search_text, website_data)
        print self.name + ' returned ' + str(len(search_results)) + ' matches for ' + self.search_text
        print 'Exiting {}'.format(self.name)
        return search_results


if __name__ == '__main__':
    urls = ['https://www.toptal.com/python/beginners-guide-to-concurrency-and-parallelism-in-python', \
            'https://developers.google.com/edu/python/regular-expressions', \
            'https://stackoverflow.com/questions/2275359/jquery-parsejson-throws-invalid-json-error-due-to-escaped-single-quote-in-json']
    t1 = AsyncURLOpener('Thread1', urls[0], 'queue')
    t2 = AsyncURLOpener('Thread2', urls[1], 'pattern')
    t3 = AsyncURLOpener('Thread3', urls[2], 'quote')
    r1 = t1.start()
    r2 = t2.start()
    r3 = t3.start()
    print 'Continuining main function'
    t1.join()
    t2.join()
    t3.join()
    print 'Main function has ended with r1={}, r2={},r3={}'.format(r1, r2, r3)
