from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
URL = 'https://www.google.com/search?q=junior+%22python%22+&oq=junior&aqs=chrome.0.69i59j46i512j0i131i433i512j46i131i175i199i433i512j0i433i512j69i61j69i60j69i61.1164j0j7&sourceid=chrome&ie=UTF-8&ibp=htl;jobs&sa=X&ved=2ahUKEwj2nObB3uv6AhWMQkEAHSstDrsQutcGKAF6BAgKEAY&sxsrf=ALiCzsYQI5IhM4tuqlfkEd3fJWNNOEUUmw:1666163444131#htivrt=jobs&fpstate=tldetail&htilrad=24.1401&htichips=city:8_MXt1sbdkgKsgA5eS6RSQ%3D%3D&htischips=city;8_MXt1sbdkgKsgA5eS6RSQ%3D%3D:London&htidocid=Ad8ENHx4r_AAAAAAAAAAAA%3D%3D'
driver.get(URL)

driver.maximize_window()
driver.implicitly_wait(30)
j = 1
for i in range(50):
    element = driver.find_element(by=By.XPATH, value = '//li[@class="iFjolb gws-plugins-horizon-jobs__li-ed"]')
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    j =  j + 1

