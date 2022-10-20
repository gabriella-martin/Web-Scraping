from openpyxl import Workbook
import pickle

with open('info_list', 'rb') as il:
    info_list = pickle.load(il)

with open('des_list', 'rb') as dl:
    description_list = pickle.load(dl)

with open('link_list', 'rb') as ll:
    link_list = pickle.load(ll)

description_list = [description_list[-1]] + description_list[:-1]
link_list = [link_list[-1]] + link_list[:-1]

for count, value in enumerate(description_list):
    info_list[count].append(value)

for count,value in enumerate(link_list):
    info_list[count][3] = value



headers = ['Job Name', 'Company Name', 'Location', 'Link to Apply', 'Description']
workbook_name = 'Job Data.xlsx'
wb = Workbook()
page = wb.active
page.title = 'Junior Python'
page.append(headers)
for info in info_list:
    page.append(info)

wb.save(filename = workbook_name)




















'''def workbook(self):
    wb = load_workbook('Job Data.xlsx')
    ws = wb.active
    ws.append(self.job_info)
    wb.save('Job Data.xlsx')''

list_of_lists = [['Anna', 'Sumner', '22', 'QEGS'], ['Rosie', 'Gebbie', '23', 'St Bedes']]


small_list = ['Blonde', 'Brunette']

for count, value in enumerate(small_list):
    list_of_lists[count].append(value)
  
print(list_of_lists)find_postings = self.driver.find_elements(by=By.XPATH, value = '//li[@class="iFjolb gws-plugins-horizon-jobs__li-ed"]')
        for posting in find_postings:
            posting.click()
            time.sleep(3)'''