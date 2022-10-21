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

        self.driver = webdriver.Chrome()
        self.URL = 'https://www.google.com/search?q=junior+%22python%22+&oq=junior&aqs=chrome.0.69i59j46i512j0i131i433i512j46i131i175i199i433i512j0i433i512j69i61j69i60j69i61.1164j0j7&sourceid=chrome&ie=UTF-8&ibp=htl;jobs&sa=X&ved=2ahUKEwj2nObB3uv6AhWMQkEAHSstDrsQutcGKAF6BAgKEAY&sxsrf=ALiCzsYQI5IhM4tuqlfkEd3fJWNNOEUUmw:1666163444131#htivrt=jobs&fpstate=tldetail&htilrad=24.1401&htichips=city:8_MXt1sbdkgKsgA5eS6RSQ%3D%3D&htischips=city;8_MXt1sbdkgKsgA5eS6RSQ%3D%3D:London&htidocid=Ad8ENHx4r_AAAAAAAAAAAA%3D%3D'
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

        fifteen_miles = self.driver.find_element(by=By.XPATH, value = '//div[@data-display-value="15 mi"]')
        fifteen_miles.click()
    
    def get_job_info(self):

        #retrieve basic job info in a list

        job_info_list = (self.driver.find_elements(by=By.XPATH, value = '//div[@class="PwjeAc"]'))
        for job in job_info_list:
            job_text = job.text.splitlines() #each item in list has format Job Name \n Company Name \n Location \n via Recruiters \n When Posted \n Salary \n Hours
            self.job_info.append(job_text)
            time.sleep(2)
        for each_job in self.job_info:
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
                first_half_of_description = str((desc_1.get_attribute('innerText')))
                self.job_description.append(first_half_of_description)
            description_2 = self.driver.find_elements(by=By.XPATH, value = '//span[@class="WbZuDe"]')
            for count, value in enumerate(description_2):
                second_half_of_description = str(value.get_attribute('innertext'))
                self.job_description[count] = str(self.job_description[count]) + ' ' + second_half_of_description
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

