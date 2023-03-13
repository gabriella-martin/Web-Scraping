import os
import pickle
import sys
import unittest
from openpyxl import load_workbook
sys.path.insert(1, '/Users/gabriellamartin/Web Scraping' )
from project.data_processing import DataProcessing

class TestDataProcessing(unittest.TestCase):

    def setUp(self):
        self.processing = DataProcessing()

    def test_clean_job_info_list(self):
        formatted_list = self.processing.clean_job_info_list()
        for job_info in formatted_list:
            self.assertGreater(len(job_info), 0)
            self.assertGreater(len(job_info[0]), 0)

    def test_shift_link_and_description_data_left(self):
        link_list, description_list = self.processing.shift_link_and_description_data_left()
        self.assertEqual(len(link_list), len(description_list))
        self.assertEqual(len(link_list), len(self.processing.job_info))

    def test_collate_all_data_in_one_list(self):
        job_info_formatted = self.processing.clean_job_info_list()
        link_and_desc_lists = self.processing.shift_link_and_description_data_left()
        collated_list = self.processing.collate_all_data_in_one_list(job_info_formatted, link_and_desc_lists)
        for job_info in collated_list:
            self.assertEqual(len(job_info), 5)

    def test_edit_excel(self):
        job_info_formatted = self.processing.clean_job_info_list()
        link_and_desc_lists = self.processing.shift_link_and_description_data_left()
        job_info_formatted = self.processing.collate_all_data_in_one_list(job_info_formatted, link_and_desc_lists)
        self.processing.edit_excel(job_info_formatted)
        self.assertTrue(os.path.isfile('Job Data.xlsx'))
        wb = load_workbook(filename = 'Job Data.xlsx')
        page = wb.active
        headers = [cell.value for cell in page[1]]
        self.assertEqual(headers, ['Job Name', 'Company Name', 'Location', 'Link to Apply', 'Description'])
        self.assertGreater(len(page['A']), 1)

    def test_pickle(self):
        job_info_formatted = self.processing.clean_job_info_list()
        link_and_desc_lists = self.processing.shift_link_and_description_data_left()
        job_info_formatted = self.processing.collate_all_data_in_one_list(job_info_formatted, link_and_desc_lists)
        self.processing.pickle(job_info_formatted)
        self.assertTrue(os.path.isfile('full_info_list'))
        with open('full_info_list', 'rb') as f:
            loaded_list = pickle.load(f)
        self.assertEqual(len(loaded_list), len(job_info_formatted))
        
    def tearDown(self):
        del self.processing
        
if __name__ == '__main__':
    unittest.main()