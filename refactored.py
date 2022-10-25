from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pickle


class Scraper():

    def __init__(self):
      
        #the empty lists the data will go in

        self.job_info = [] 
        self.job_info_formatted = []
        self.job_description = []
        self.job_links = []

        #initialised the scraper
        self.job_search_query = ''
        self.job_search = input('What jobs would you like to search for? ').split()
        self.job_location = input('What location would you like to search in? ').split()
        self.job_radius = input('What radius would you like to search with (miles), input either 2, 5, 15, 30, 60 or 200 ')

        for word in self.job_search:
            self.job_search_query = self.job_search_query + '+' + word

        for word in self.job_location:
            self.job_search_query = self.job_search_query + '+' + word


        self.driver = webdriver.Chrome()
        self.URL = 'https://www.google.com/search?q=' + self.job_search_query + '&oq=' + self.job_search_query + '&aqs=chrome.0.69i59j69i57j0i512l3j69i60j69i61j69i60.2372j0j4&sourceid=chrome&ie=UTF-8&ibp=htl;jobs&sa=X&ved=2ahUKEwiSnLaS4vD6AhXASkEAHbGeCmIQutcGKAF6BAgPEAY&sxsrf=ALiCzsYBgFpn29JiT-bmDitHpZhnSS8_KA:1666336217212#fpstate=tldetail&htivrt=jobs&htidocid=yMtX4QFL-SgAAAAAAAAAAA%3D%3D'
        self.driver.get(self.URL)


    def accept_cookies(self):

        #find and click accept cookies button

        accept_cookies_button = self.driver.find_element(by=By.XPATH, value ='//button[@aria-label="Accept all"]')
        accept_cookies_button.click()
        time.sleep(2)
        
    def specify_location(self):

        #find and click location option tab (already routed to London)

        location_button = self.driver.find_element(by=By.XPATH, value = '//span[@jsname="ZwfL4c" and @class="cS4btb is1c5b" and @data-facet="city"]')
        location_button.click()
        time.sleep(2)

        #chose radius of 15 miles

        fifteen_miles = self.driver.find_element(by=By.XPATH, value = '//div[@data-display-value="' + self.job_radius + ' mi"]')
        fifteen_miles.click()
    
    def get_job_info(self):

        #retrieve basic job info in a list

        job_info_list = (self.driver.find_elements(by=By.XPATH, value = '//div[@class="PwjeAc"]'))
        for job in job_info_list:
            job_text = job.text.splitlines() #each item in list has format Job Name \n Company Name \n Location \n via Recruiters \n When Posted \n Salary \n Hours
            self.job_info.append(job_text)
            time.sleep(2)
        for each_job in self.job_info:
            time.sleep(0.5)
            if len(each_job[0]) == 1: #logo compared to no logo
                each_job = each_job[1:]
                each_job = each_job[:4]
                self.job_info_formatted.append(each_job)
            else:
                each_job = each_job[:4]
                self.job_info_formatted.append(each_job)
        return(self.job_info_formatted)
             
    def get_description(self):
            description_1 = self.driver.find_elements(by=By.XPATH, value = '//span[@class="HBvzbc"]')
            for desc_1 in description_1:
                first_half_of_description = desc_1.get_attribute('innerText')
                self.job_description.append(first_half_of_description)
                time.sleep(0.5)

            first_job_exception_locator = self.driver.find_element(by=By.XPATH, value = '/html/body/div[2]/div/div[2]/div[1]/div/div/div[3]/div[2]/div/div[1]/div/div/div[4]/div/span/span[2]')
            first_job_exception_description = first_job_exception_locator.get_attribute('innerText')
            self.job_description[-1] = self.job_description[-1] + ' ' + first_job_exception_description
            

            description_2 = self.driver.find_elements(by=By.XPATH, value = '//span[@class="WbZuDe"]')
            
            for count, desc_2 in enumerate(description_2):
                second_half_of_description = desc_2.get_attribute('innerText')
                self.job_description[count] = self.job_description[count] + ' ' + second_half_of_description

            return(self.job_description)
           
            
    def get_links(self):
        find_link_location = self.driver.find_elements(by=By.XPATH, value = '//span[@class="DaDV9e"]')
        for location in find_link_location:
            a_tag = location.find_element(by=By.TAG_NAME, value = 'a')
            link = a_tag.get_attribute('href')
            self.job_links.append(link)
        return(self.job_links)
        
    def scrape(self):
        self.accept_cookies()
        self.specify_location()
        time.sleep(10)
        self.get_links()
        self.get_job_info()
        self.get_description()
        self.pickle()
        print('Done')

    def pickle(self):
        with open('info_list', 'wb') as il:
            pickle.dump(self.job_info_formatted, il)

        with open('des_list', 'wb') as dl:
            pickle.dump(self.job_description, dl)

        with open('link_list', 'wb') as ll:
            pickle.dump(self.job_links, ll)

test1 = Scraper()

test1.scrape()

