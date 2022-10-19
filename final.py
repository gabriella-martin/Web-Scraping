from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
URL = 'https://www.google.com/search?q=junior+python+jobs&oq=jun&aqs=chrome.0.69i59j69i57j46i131i433i512j46i433i512j0i433i512j69i61j69i60j69i61.819j0j4&sourceid=chrome&ie=UTF-8&ibp=htl;jobs&sa=X&ved=2ahUKEwinz-Xf8en6AhVXPcAKHZhiCYMQutcGKAF6BAgQEAY&sxsrf=ALiCzsaYrhYUO4lOURleqjVQnBtjCSo8lg:1666099887835#htivrt=jobs&fpstate=tldetail&htichips=&htischips=&htidocid=7PLPViTybSQAAAAAAAAAAA%3D%3D'
driver.get(URL)

time.sleep(2)



def accept_cookies():
    accept_cookies_button = driver.find_element(by=By.XPATH, value ='//button[@aria-label="Accept all"]')
    accept_cookies_button.click()

def find_jobs():
    job_preview_button = driver.find_elements(by=By.XPATH, value = '//li[@class="iFjolb gws-plugins-horizon-jobs__li-ed"]')
    for job in job_preview_button:
        time.sleep(2)
        job.click()
        time.sleep(2)
        description = driver.find_element(by=By.XPATH, value = '//span[@class="HBvzbc"]')
        print(description.text)


accept_cookies()

time.sleep(4)

find_jobs()

