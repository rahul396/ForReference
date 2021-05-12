import re, os
import urllib.parse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import requests
from bs4 import BeautifulSoup
from time import sleep

link = 'https://www.bankofengland.co.uk/news/news'

class UKMonetaryPolicy(object):
    def __init__(self):
        options = webdriver.ChromeOptions()
        #options.set_headless(headless=True)
        options.add_argument("--proxy-server='direct://'");
        options.add_argument("--proxy-bypass-list=*");
        options.add_argument('--disable-gpu')
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options, executable_path='C:\\Users\\rku172\\Documents\\PythonPractice\chromedriver.exe')
        #self.driver.set_window_size(1120, 700)
        self.wait = WebDriverWait(self.driver, 10)

    def iterate_pages(self, pages):
        print ('inside pages')
        for page in pages:
            res = requests.get(page)
            if res.status_code==200:
                soup = BeautifulSoup(res.text, 'html.parser')
                content = soup.findAll('div',{'class':'content-block'})[0]
                a_tags = content.findAll('a')
                for a in a_tags:
                    #urls.append('https://www.bankofengland.co.uk/news'+a['href'])

                    fname = 'https://www.bankofengland.co.uk/news'+a['href']
                    response = requests.get(fname)
                    url = a['href'].split('/')
                    foldername = url[-2]
                    filename = r"C:\Users\rku172\Desktop\UKMonitaryPolicyDocuments\\" + foldername + r"\\"
                    if not os.path.exists(os.path.dirname(filename)):
                        try:
                            os.makedirs(os.path.dirname(filename))
                        except OSError as exc:
                            print (str(exc))
                    with open(filename + a.text.strip() + ".pdf", "wb") as pdf:
                        for chunk in response.iter_content(chunk_size=1024):
                            if chunk:
                                pdf.write(chunk)
                    print(a.text + " Downloaded Successfuly!")
    
    def load_new_pages(self,index):
        allelements = self.driver.find_element_by_id("SearchResults")
        html = allelements.get_attribute('innerHTML')
        soup = BeautifulSoup(html,'html.parser')
        print (index)
        col3 = soup.find_all('div',{'class':'col3'})[index:]
        pages = []
        for col in col3:
            a_tag = col.find('a')['href']
            pages.append('https://www.bankofengland.co.uk'+a_tag)
        #urls = []
        col3_webElement = self.driver.find_elements_by_xpath('//*[@id="SearchResults"]/div')[index:]
        self.iterate_pages(pages)
        self.driver.execute_script("arguments[0].scrollIntoView();",col3_webElement[-1])
        #new_col3 = self.driver.find_elements_by_xpath('//*[@id="SearchResults"]/div')
        sleep(5)
        # wait = WebDriverWait(self.driver,10)
        # wait.until(len(new_col3)>index+10)
        print ('col3 elements: {}'.format(len(col3)))
        index += len(col3)-1
        if index<100:
            self.load_new_pages(index)
        

    def scrape(self):
        self.driver.get(link)
        self.driver.find_element_by_xpath("""/ html / body / div[1] / div[3] / div / button""").click()
        sleep(3)
        self.driver.find_element_by_xpath("""//*[@id="NewsListingPage"]/div/div[1]/div[2]/div/label[3]""").click()
        sleep(3)
        
        # col3 = soup.find_all('div',{'class':'col3'})
        # pages = []
        # print ('getting 1st level urls')
        # for col in col3:
        #     a_tag = col.find('a')['href']
        #     pages.append('https://www.bankofengland.co.uk'+a_tag)
        # #urls = []
        # self.iterate_pages(pages)
        # self.driver.execute_script("arguments[0].scrollIntoView(true);",col3[-1])
        # sleep(3)
        self.load_new_pages(0)

        self.driver.quit()


    



if __name__ == '__main__':
    scraper = UKMonetaryPolicy()
    scraper.scrape()
