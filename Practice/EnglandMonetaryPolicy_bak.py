import re
import urllib.parse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.common import action_chains, keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

link = 'https://www.bankofengland.co.uk/news/news'


class TaleoJobScraper(object):
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-gpu')
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options, executable_path='C:\\Users\\rku172\\Documents\\PythonPractice\chromedriver.exe')
        self.driver.set_window_size(1120, 700)
        self.wait = WebDriverWait(self.driver, 10)


    def scrape(self):
        self.driver.get(link)
        self.driver.find_element_by_xpath("""/ html / body / div[1] / div[3] / div / button""").click()
        element = self.driver.find_element_by_xpath("""//*[@id="checkbox-Topic2"]""")
        #element = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, "checkbox-Topic2")))
        #self.driver.execute_script("el = document.getElementById('SearchResults');el.innerHTML = ''")
        self.driver.execute_script("$(arguments[0].checked=true);", element)
        #self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        #self.driver.refresh()
        sleep(6)
        #element.click()
        allelements = self.driver.find_element_by_id("SearchResults")
        # col3 = allelements.find_elements_by_class_name('col3')
        #a_tags = allelements.find_elements_by_xpath('//*[@id="SearchResults"]/div/a')
        print (allelements.get_attribute('innerHTML'))
        

        self.driver.quit()
        return allelements

    # def scrape_job_links(self):
    #     self.driver.get(link)
    #
    #    # element = driver.find_element_by_xpath("""//*[@id="NewsListingPage"]/div/div[1]/div[2]/div/label[1]""").click()
    #     allelements = self.driver.find_elements_by_class_name('release-news')
        return allelements


if __name__ == '__main__':
    scraper = TaleoJobScraper()
    ret = scraper.scrape()