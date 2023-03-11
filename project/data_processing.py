import pickle
from openpyxl import Workbook

class DataProcessing():

    '''This is a class used to process and format the data and resolve any issues within the data'''

    def __init__(self):

        '''The initialiser first unpickles the lists from the scraper class 
        and also initialises the full formatted job info list that will include all the data including
        the links, descriptions all in one list where each item is a list of all the info for each job posting'''

        with open('list_0', 'rb') as il:
            self.job_info = pickle.load(il)

        with open('list_1', 'rb') as dl:
            self.description_list = pickle.load(dl)

        with open('list_2', 'rb') as ll:
            self.link_list = pickle.load(ll)

    def clean_job_info_list(self):
        
        job_info_formatted = []
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
                job_info_formatted.append(each_job)
            else:
                each_job = each_job[:4]
                job_info_formatted.append(each_job)

        return job_info_formatted
    
    def shift_link_and_description_data_left(self):

        '''for some reason both the link and description list seemed to have the first job posting appear
        at the end of the list, the second job posting was the first item of the list etc, so the list needs
        to be moved to the left by one to ensure the data matches the correct job posting - this function
        achieves this'''

        description_list = [self.description_list[-1]] + self.description_list[:-1]
        link_list = [self.link_list[-1]] + self.link_list[:-1]

        return(link_list, description_list)

    def collate_all_data_in_one_list(self, job_info_formatted, link_and_desc_lists):

        '''this function creates one big nested list of all the job information - it creates a 
        nested list of the format of [[job name 1, company name 1, ... , link 1, desc 1], [job name 2, 
        company name 2, ... , link 2, desc 2]... '''

        link_list = link_and_desc_lists[0]
        description_list = link_and_desc_lists[1]

        for count, value in enumerate(description_list):
            job_info_formatted[count].append(value)

        for count,value in enumerate(link_list):
            job_info_formatted[count][3] = value

        return job_info_formatted

    def edit_excel(self, job_info_formatted):

        '''This function adds the data to an excel spreadsheet and correctly names each column'''

        headers = ['Job Name', 'Company Name', 'Location', 'Link to Apply', 'Description']
        workbook_name = 'Job Data.xlsx'
        wb = Workbook()
        page = wb.active
        page.title = 'Python Jobs'
        page.append(headers)
        for info in job_info_formatted:
            page.append(info)

        wb.save(filename = workbook_name)

    def pickle(self, job_info_formatted):

        '''This function pickles this full job list for use in the data analysis class'''

        with open('full_info_list', 'wb') as fil:
            pickle.dump(job_info_formatted, fil)

    def sort_data(self):

        '''This function calls the functions to complete the processing in the correct order'''

        job_info_formatted = self.clean_job_info_list()
        link_and_desc_lists = self.shift_link_and_description_data_left()
        job_info_formatted = self.collate_all_data_in_one_list(job_info_formatted, link_and_desc_lists)
        self.edit_excel(job_info_formatted)
        self.pickle(job_info_formatted)


if __name__ == '__main__':

    dp = DataProcessing()
    dp.sort_data()
