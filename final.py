
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import openpyxl
from openpyxl import Workbook, load_workbook

wb = load_workbook('Job Data.xlsx')
ws = wb.active
ws.append(['Gab', 'is', 'gay'])
wb.save('Job Data.xlsx')

driver = webdriver.Chrome()
URL = 'https://www.google.com/search?q=junior+%22python%22+&oq=junior&aqs=chrome.0.69i59j46i512j0i131i433i512j46i131i175i199i433i512j0i433i512j69i61j69i60j69i61.1164j0j7&sourceid=chrome&ie=UTF-8&ibp=htl;jobs&sa=X&ved=2ahUKEwj2nObB3uv6AhWMQkEAHSstDrsQutcGKAF6BAgKEAY&sxsrf=ALiCzsYQI5IhM4tuqlfkEd3fJWNNOEUUmw:1666163444131#htivrt=jobs&fpstate=tldetail&htilrad=24.1401&htichips=city:8_MXt1sbdkgKsgA5eS6RSQ%3D%3D&htischips=city;8_MXt1sbdkgKsgA5eS6RSQ%3D%3D:London&htidocid=Ad8ENHx4r_AAAAAAAAAAAA%3D%3D'
driver.get(URL)

time.sleep(2)

def specify_location():
    location_button = driver.find_element(by=By.XPATH, value = '//span[@jsname="ZwfL4c" and @class="cS4btb is1c5b" and @data-facet="city"]')
    location_button.click()
    time.sleep(2)
    fifteen_miles = driver.find_element(by=By.XPATH, value = '//div[@data-display-value="15 mi"]')
    fifteen_miles.click()
    pass

def accept_cookies():
    accept_cookies_button = driver.find_element(by=By.XPATH, value ='//button[@aria-label="Accept all"]')
    accept_cookies_button.click()
    time.sleep(2)

job_info = []

def get_job_info():
    job_info_list = (driver.find_elements(by=By.XPATH, value = '//div[@class="PwjeAc"]'))
    for job in job_info_list:
        job_text = job.text
        job_info.append(job_text)

        


description_list = []

def get_description():
    find_description = (driver.find_elements(by=By.XPATH, value = '//span[@class="HBvzbc"]'))
    for description in find_description:
        description_text = description.get_attribute('innerText')
        description_list.append(description_text)


accept_cookies()
specify_location()

time.sleep(10)

get_job_info()



get_description()

my_list = (job_info[0])

split_list = my_list.splitlines()

print(split_list)
