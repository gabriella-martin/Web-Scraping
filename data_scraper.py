import argparse
import pickle
import time
from openpyxl import Workbook
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


def get_search_query():
    parser = argparse.ArgumentParser(description='Specify your job search query')
    parser.add_argument('JobTitle', type=str, help ='What jobs do you want to search for', default='Developer')
    parser.add_argument('Location', type=str, help='What location would you like to search in?', default='London')
    parser.add_argument('Radius', type=int, help='What radius would you like to search with (mi)? 2, 5, 15, 30, 60 or 200', default=2)
    args = parser.parse_args()
    job_title_query = (args.JobTitle).split() 
    location_query = (args.Location).split()
    radius = args.Radius
    search_query = ''
    for word in job_title_query:
        search_query = search_query + '+' + word
    for word in location_query:
        search_query = search_query + '+' + word
    return search_query, radius

arguments = get_search_query()

class Scraper():

    def __init__(self,search_query=arguments[0], radius=arguments[1]):
        # DOCSTRING
        self.radius = radius
        self.search_query = search_query
        self.url = 'https://www.google.com/search?q=' + self.search_query + '&oq=' + self.search_query + '&aqs=chrome.0.69i59j69i57j0i512l3j69i60j69i61j69i60.2372j0j4&sourceid=chrome&ie=UTF-8&ibp=htl;jobs&sa=X&ved=2ahUKEwiSnLaS4vD6AhXASkEAHbGeCmIQutcGKAF6BAgPEAY&sxsrf=ALiCzsYBgFpn29JiT-bmDitHpZhnSS8_KA:1666336217212#fpstate=tldetail&htivrt=jobs&htidocid=yMtX4QFL-SgAAAAAAAAAAA%3D%3D'
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("window-size=1920,1080")
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        chrome_options.add_argument(f'user-agent={user_agent}')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        time.sleep(1)
        self.driver.get(self.url)

    def _accept_cookies(self):
        try:
            accept_cookies_button = self.driver.find_element(by=By.XPATH, value ='//button[@aria-label="Accept all"]')
            accept_cookies_button.click()
        except:
            pass

    def _specify_location(self):
        try:
            location_button = self.driver.find_element(by=By.XPATH, value = '//span[@jsname="ZwfL4c" and @class="cS4btb is1c5b" and @data-facet="city"]')
            location_button.click()
            time.sleep(1)
            miles_string = ' mi'
            miles_specified = self.driver.find_element(by=By.XPATH, value = f'//div[@data-display-value="{self.radius}{miles_string}"]')
            miles_specified.click()
        except:
            pass

    def _scroll_to_load(self):
        for num in range(0,5):
            all_job_postings = self.driver.find_elements(by=By.XPATH, value = '//div[@class="PwjeAc"]')
            for i in all_job_postings:
                    self.driver.execute_script("arguments[0].scrollIntoView();", i)   
                    time.sleep(1)

        all_job_postings.reverse()
        for num in range(0,5):
            for i in all_job_postings:
                self.driver.execute_script("arguments[0].scrollIntoView();", i)
                time.sleep(1)

    def get_job_info(self):
        job_infos = []
        job_info_list = (self.driver.find_elements(by=By.XPATH, value = '//div[@class="PwjeAc"]'))
        time.sleep(2)
        for job in job_info_list:
            time.sleep(1)
            job_text = job.text.splitlines() 
            job_infos.append(job_text)
        return job_infos

    def get_description(self):

        job_descriptions = []
        description_part_1 = self.driver.find_elements(by=By.XPATH, value = '//span[@class="HBvzbc"]')
        for desc_1 in description_part_1:
            first_half_of_description = desc_1.get_attribute('innerText')
            job_descriptions.append(first_half_of_description)
            time.sleep(0.5)

        first_job_exception_locator = self.driver.find_elements(by=By.XPATH, value = '/html/body/div[2]/div/div[2]/div[1]/div/div/div[3]/div[2]/div/div[1]/div/div/div[4]/div/span/span[2]')
        if len(first_job_exception_locator) != 0:
            for job in first_job_exception_locator:
                first_job_exception_description = job.get_attribute('innerText')
                job_descriptions[-1] = job_descriptions[-1] + ' ' + first_job_exception_description
                break
        
        description_part_2 = self.driver.find_elements(by=By.XPATH, value = '//span[@class="WbZuDe"]')   
        for count, desc_2 in enumerate(description_part_2):
            second_half_of_description = desc_2.get_attribute('innerText')
            job_descriptions[count] = job_descriptions[count] + ' ' + second_half_of_description

        return(job_descriptions)

    def get_links(self):

        job_links = []
        find_link_location = self.driver.find_elements(by=By.XPATH, value = '//span[@class="DaDV9e"]')
        for location in find_link_location:
            a_tag = location.find_element(by=By.TAG_NAME, value = 'a')
            link = a_tag.get_attribute('href')
            job_links.append(link)
        return(job_links) 

    def run_scraper(self):

        self._accept_cookies()
        time.sleep(2)
        self._specify_location
        time.sleep(7)
        self._scroll_to_load()
        time.sleep(2)
        job_infos = self.get_job_info()
        job_descriptions = self.get_description()
        job_links = self.get_links()
        lists_to_be_pickled = [job_infos, job_descriptions, job_links]
        return lists_to_be_pickled

    def _pickle_lists(self):
 
        lists_to_be_pickled = self.run_scraper()
        for index, list_item in enumerate(lists_to_be_pickled):
            with open(f'list_{index}', 'wb') as li:
                pickle.dump(list_item, li)


if __name__ == '__main__':
    s = Scraper()
    s._pickle_lists()