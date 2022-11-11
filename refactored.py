from openpyxl import Workbook
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import pickle
import time



class Scraper():

    '''This is a class used to scrape information of the google jobs website'''

    def __init__(self):

        '''First we initialise all the information lists we want to retrieve,
        then we ask the user to specify their search query following the options allowed on Google jobs
        this is then formatted to match the url that google jobs requires
        then the driver is started with the particular url'''

        self.job_info = [] 
        self.job_info_formatted = []
        self.job_description = []
        self.job_links = []

        self.job_search_query = ''
        self.job_search = input('What jobs would you like to search for? ').split()
        self.job_location = input('What location would you like to search in? ').split()
        self.job_radius = input('What radius would you like to search with (miles), input either 2, 5, 15, 30, 60 or 200 ')

        for word in self.job_search:
            self.job_search_query = self.job_search_query + '+' + word

        for word in self.job_location:
            self.job_search_query = self.job_search_query + '+' + word

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("window-size=1920,1080")
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        chrome_options.add_argument(f'user-agent={user_agent}')
        self.driver = webdriver.Chrome(executable_path="chromedriver", options=chrome_options)
        time.sleep(5)
        self.URL = 'https://www.google.com/search?q=' + self.job_search_query + '&oq=' + self.job_search_query + '&aqs=chrome.0.69i59j69i57j0i512l3j69i60j69i61j69i60.2372j0j4&sourceid=chrome&ie=UTF-8&ibp=htl;jobs&sa=X&ved=2ahUKEwiSnLaS4vD6AhXASkEAHbGeCmIQutcGKAF6BAgPEAY&sxsrf=ALiCzsYBgFpn29JiT-bmDitHpZhnSS8_KA:1666336217212#fpstate=tldetail&htivrt=jobs&htidocid=yMtX4QFL-SgAAAAAAAAAAA%3D%3D'
        self.driver.get(self.URL)

    def accept_cookies(self):

        '''this function locates and clicks the accept cookies button'''

        accept_cookies_button = self.driver.find_element(by=By.XPATH, value ='//button[@aria-label="Accept all"]')
        accept_cookies_button.click()
        time.sleep(2)
        
    def specify_location(self):

        '''finds location button and clicks to reveal the radius options, 
        then takes user specified radius and clicks on this option to reveal the specific job postings'''

        location_button = self.driver.find_element(by=By.XPATH, value = '//span[@jsname="ZwfL4c" and @class="cS4btb is1c5b" and @data-facet="city"]')
        location_button.click()
        time.sleep(2)

        miles_specified = self.driver.find_element(by=By.XPATH, value = '//div[@data-display-value="' + self.job_radius + ' mi"]')
        miles_specified.click()
    
    def scroll_to_load(self):

        all_job_postings = self.driver.find_elements(by=By.XPATH, value = '//div[@class="PwjeAc"]')
        for i in all_job_postings:
                self.driver.execute_script("arguments[0].scrollIntoView();", i)   
                time.sleep(0.5)
        
        all_job_postings = self.driver.find_elements(by=By.XPATH, value = '//div[@class="PwjeAc"]')
        for i in all_job_postings:
                self.driver.execute_script("arguments[0].scrollIntoView();", i)
                time.sleep(0.5)

        all_job_postings.reverse()
        for i in all_job_postings:
            self.driver.execute_script("arguments[0].scrollIntoView();", i)
            time.sleep(0.5)

    def get_job_info(self):

        '''retrieves a list of basic job information for each job posting,
        each item in the list is another job posting and is of the format;
        (Nothing (as has picture of company logo) OR First letter of company name \n 
        Job Name \n Company Name \n Location \n via Recruiters \n When Posted \n Salary \n Hours
        So the text is then split along these \n and appended to our job info list'''

        job_info_list = (self.driver.find_elements(by=By.XPATH, value = '//div[@class="PwjeAc"]'))
        time.sleep(10)
        for job in job_info_list:
            time.sleep(1)
            job_text = job.text.splitlines() 
            self.job_info.append(job_text)
        return self.job_info
                 
    def get_description(self):
        
        '''The first part of this function is dealing with the first job posting anomoly,
        as this job is the only one actually loaded when the webpage is opened, 
        it therefore checks whether this initial description is split into two pieces and if it is
        retrieves both parts and combines them and adds them to the last item in the list - as this 
        is where the first description is added to (this discrepancy is sorted later when formatting)
        
        Next, the remainder of the descriptions are retrieves, if they are split in two web elements
        this function will combine the two and add them to the complete description list'''
            
        description_part_1 = self.driver.find_elements(by=By.XPATH, value = '//span[@class="HBvzbc"]')
        for desc_1 in description_part_1:
            first_half_of_description = desc_1.get_attribute('innerText')
            self.job_description.append(first_half_of_description)
            time.sleep(0.5)

        first_job_exception_locator = self.driver.find_elements(by=By.XPATH, value = '/html/body/div[2]/div/div[2]/div[1]/div/div/div[3]/div[2]/div/div[1]/div/div/div[4]/div/span/span[2]')
        if len(first_job_exception_locator) != 0:
            for job in first_job_exception_locator:
                first_job_exception_description = job.get_attribute('innerText')
                self.job_description[-1] = self.job_description[-1] + ' ' + first_job_exception_description
                break


        description_part_2 = self.driver.find_elements(by=By.XPATH, value = '//span[@class="WbZuDe"]')   
        for count, desc_2 in enumerate(description_part_2):
            second_half_of_description = desc_2.get_attribute('innerText')
            self.job_description[count] = self.job_description[count] + ' ' + second_half_of_description

        return(self.job_description)
                      
    def get_links(self):

        '''this locates all the links to apply and retrieves the links and appends them to our link list'''

        find_link_location = self.driver.find_elements(by=By.XPATH, value = '//span[@class="DaDV9e"]')
        for location in find_link_location:
            a_tag = location.find_element(by=By.TAG_NAME, value = 'a')
            link = a_tag.get_attribute('href')
            self.job_links.append(link)
        return(self.job_links)

    def pickle(self):

        '''This allows a easy transfer of these lists to the next class so to avoid overdependencies 
        between the classes - 'saves' these lists to use in the following classes'''

        with open('info_list', 'wb') as il:
            pickle.dump(self.job_info, il)

        with open('des_list', 'wb') as dl:
            pickle.dump(self.job_description, dl)

        with open('link_list', 'wb') as ll:
            pickle.dump(self.job_links, ll)

    def scrape(self):

        '''This function runs the entire scraping process'''

        self.accept_cookies()
        time.sleep(5)
        self.specify_location()
        time.sleep(10)
        self.scroll_to_load()
        time.sleep(5)
        self.get_links()
        self.get_job_info()
        self.get_description()
        self.pickle()
        print('Done')

class DataProcessing():

    '''This is a class used to process and format the data and resolve any issues within the data'''

    def __init__(self):

        '''The initialiser first unpickles the lists from the scraper class 
        and also initialises the full formatted job info list that will include all the data including
        the links, descriptions all in one list where each item is a list of all the info for each job posting'''

        with open('info_list', 'rb') as il:
            self.job_info = pickle.load(il)

        with open('des_list', 'rb') as dl:
            self.description_list = pickle.load(dl)

        with open('link_list', 'rb') as ll:
            self.link_list = pickle.load(ll)

        self.job_info_formatted = []

    def clean_job_info_list(self):

        '''This function sorts the info data - solves the following two problems:

        - some companies without a picture logo google instead puts the first character of the company name 
        and this is retrieved as text and is futile for us. Thankfully this is the first item retrieved and 
        so we can check whether the first item has a length of 1 and if it does remove it
        
        - the optional categories for each job postings like when posted, salary, whether it is WFH and 
        whether it is full or part time - the majority of jobs are missing most of this data so we want to 
        slice just the required fields so we don't have a mass of missing data'''

        for each_job in self.job_info:
            
            if len(each_job[0]) == 1: 
                each_job = each_job[1:]
                each_job = each_job[:4]
                self.job_info_formatted.append(each_job)
            else:
                each_job = each_job[:4]
                self.job_info_formatted.append(each_job)

        return(self.job_info_formatted)
    
    def shift_link_and_description_data_left(self):

        '''for some reason both the link and description list seemed to have the first job posting appear
        at the end of the list, the second job posting was the first item of the list etc, so the list needs
        to be moved to the left by one to ensure the data matches the correct job posting - this function
        achieves this'''

        self.description_list = [self.description_list[-1]] + self.description_list[:-1]
        self.link_list = [self.link_list[-1]] + self.link_list[:-1]
        return(self.description_list, self.link_list)

    def collate_all_data_in_one_list(self, info_list_formatted, link_and_desc_lists):

        '''this function creates one big nested list of all the job information - it creates a 
        nested list of the format of [[job name 1, company name 1, ... , link 1, desc 1], [job name 2, 
        company name 2, ... , link 2, desc 2]... '''

        for count, value in enumerate(self.description_list):
            self.job_info_formatted[count].append(value)

        for count,value in enumerate(self.link_list):
            self.job_info_formatted[count][3] = value

        return self.job_info_formatted

    def edit_excel(self, job_info_formatted):

        '''This function adds the data to an excel spreadsheet and correctly names each column'''

        headers = ['Job Name', 'Company Name', 'Location', 'Link to Apply', 'Description']
        workbook_name = 'Job Data.xlsx'
        wb = Workbook()
        page = wb.active
        page.title = 'Python Jobs'
        page.append(headers)
        for info in self.job_info_formatted:
            page.append(info)

        wb.save(filename = workbook_name)

    def pickle(self):

        '''This function pickles this full job list for use in the data analysis class'''

        with open('full_info_list', 'wb') as fil:
            pickle.dump(self.job_info_formatted, fil)

    def sort_data(self):

        '''This function calls the functions to complete the processing in the correct order'''

        info_list_formatted = self.clean_job_info_list()
        link_and_desc_lists = self.shift_link_and_description_data_left()
        info_list_formatted = self.collate_all_data_in_one_list(info_list_formatted, link_and_desc_lists)
        self.edit_excel(info_list_formatted)
        self.pickle()

class DataAnalysis():

    '''This class enables data analysis to be done on the job descriptions and gain insight in to the job
    market as a whole'''

    def __init__(self):

        '''First opens the full formatted job list and initialises the lists needed to engage with the data 
        in our analysis'''

        with open('full_info_list', 'rb') as fil:
            self.job_info_formatted = pickle.load(fil)

        self.list_of_descriptions = []
        self.skill_query = []
        self.percentages_of_skill = []
        self.sorted_dictionary_of_skills = {}
    
    def get_list_of_descriptions_only(self):

        '''This function retrieves only the job descriptions into a new list as we want to analyse only
        the descriptions'''

        for info in self.job_info_formatted:
            self.list_of_descriptions.append(info[4])
        return(self.list_of_descriptions)

    def find_prominance_of_skill(self,list_of_descriptions):

        '''This function repeatedly asks the user for a particular skill, like 'AWS', it then searches each 
        description and if the skill is found in the description a count is increased, once done this count
        is then turned into a percentage of prominance of skill by taking the number of descriptions that the
        skill appeared in and dividing by the total of the descriptions
        
        By specifying that the count must be >1 we remove any arbitrary skill searches from our final list.
        Each sucessful search query and corresponding percentage of prominance is added to a list'''

        while True:
            skill_query = str(input('What skill would you like to search for? If you are done type quit ')).lower()
            if skill_query == 'quit':
                break
            else:
                count = 0
                for desc in self.list_of_descriptions:
                    desc = desc.lower()
                    if skill_query in desc:
                        count += 1
                if count > 1:
                    percentage_of_skill = round((count/len(self.list_of_descriptions))*100)
                    self.skill_query.append(skill_query)
                    self.percentages_of_skill.append(percentage_of_skill)

        return(self.skill_query, self.percentages_of_skill)

    def make_skill_dictionary(self, skills_and_percentages):

        '''This function takes both the skill queried list and percentages and creates a dictionary'''

        self.dictionary_of_skills_and_percentages = {self.skill_query[i]: self.percentages_of_skill[i] for i in range(len(self.skill_query))}
        return(self.dictionary_of_skills_and_percentages)

    def order_dictionary(self, dictionary_of_skills_and_percentages):

        '''This function takes the dictionary and orders in in descending order - so most important technologies
        are seen first'''

        ordered_values = sorted(self.dictionary_of_skills_and_percentages.values())
        ordered_values.reverse()
        for i in ordered_values:
            for k in self.dictionary_of_skills_and_percentages.keys():
                if self.dictionary_of_skills_and_percentages[k] == i:
                    self.sorted_dictionary_of_skills[k] = dictionary_of_skills_and_percentages[k]
        print(self.sorted_dictionary_of_skills)

    def analyse_data(self):

        '''This function compiles the entire data analysis process'''

        list_of_descriptions = self.get_list_of_descriptions_only()
        skills_and_percentages = self.find_prominance_of_skill(list_of_descriptions)
        dictionary_of_skills_and_percentages = self.make_skill_dictionary(skills_and_percentages)
        self.order_dictionary(dictionary_of_skills_and_percentages)

    

a = Scraper()
a.scrape()

b = DataProcessing()
b.sort_data()
'''
c = DataAnalysis()
c.analyse_data()
'''



