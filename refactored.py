from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import openpyxl
from openpyxl import Workbook, load_workbook



class Scraper():

    def __init__(self):
      
        self.job_info = []
        self.job_info_formatted = []
        self.job_description = []
        self.driver = webdriver.Chrome()
        self.URL = 'https://www.google.com/search?q=junior+%22python%22+&oq=junior&aqs=chrome.0.69i59j46i512j0i131i433i512j46i131i175i199i433i512j0i433i512j69i61j69i60j69i61.1164j0j7&sourceid=chrome&ie=UTF-8&ibp=htl;jobs&sa=X&ved=2ahUKEwj2nObB3uv6AhWMQkEAHSstDrsQutcGKAF6BAgKEAY&sxsrf=ALiCzsYQI5IhM4tuqlfkEd3fJWNNOEUUmw:1666163444131#htivrt=jobs&fpstate=tldetail&htilrad=24.1401&htichips=city:8_MXt1sbdkgKsgA5eS6RSQ%3D%3D&htischips=city;8_MXt1sbdkgKsgA5eS6RSQ%3D%3D:London&htidocid=Ad8ENHx4r_AAAAAAAAAAAA%3D%3D'
        self.driver.get(self.URL)
    
    def accept_cookies(self):
        accept_cookies_button = self.driver.find_element(by=By.XPATH, value ='//button[@aria-label="Accept all"]')
        accept_cookies_button.click()
        time.sleep(2)

    def specify_location(self):
        location_button = self.driver.find_element(by=By.XPATH, value = '//span[@jsname="ZwfL4c" and @class="cS4btb is1c5b" and @data-facet="city"]')
        location_button.click()
        time.sleep(2)
        fifteen_miles = self.driver.find_element(by=By.XPATH, value = '//div[@data-display-value="15 mi"]')
        fifteen_miles.click()
    
    def get_job_info(self):
        job_info_list = (self.driver.find_elements(by=By.XPATH, value = '//div[@class="PwjeAc"]'))
        for job in job_info_list:
            job_text = job.text.splitlines()
            self.job_info.append(job_text)
        return(self.job_info)
        

    def format_job_list(self, full_job_info_list):
        for job in full_job_info_list:
            job = job[:4]
            if len(job[0]) == 1:
                job = job[1:]
                job = job[:4]
                self.job_info_formatted.append(job)
            else:
                job = job[:4]
                self.job_info_formatted.append(job)
                

        print(self.job_info_formatted)

    def get_description(self):
        find_description = (self.driver.find_elements(by=By.XPATH, value = '//span[@class="HBvzbc"]'))
        for description in find_description:
            description_text = description.get_attribute('innerText')
            self.job_description.append(description_text)

    def scrape(self):
        self.accept_cookies()
        self.specify_location()
        time.sleep(10)
        #self.get_description()
        full_job_info_list =  self.get_job_info()
        self.format_job_list(full_job_info_list)
        

test1 = Scraper()


    

test1.scrape()

