import sys
import unittest 
sys.path.insert(1, '/Users/gabriellamartin/Web Scraping' )
from project.data_scraper import Scraper

class ScraperTestCase(unittest.TestCase):
    def setUp(self):
        self.scraper = Scraper(search_query='+developer+london', radius=2)
        self.scraper._accept_cookies()
        self.scraper._specify_location()
        self.scraper._scroll_to_load()
    
    def test_get_job_info(self):
        # check it is a non empty list 
        job_info = self.scraper.get_job_info()
        self.assertIs(type(job_info), list)
        self.assertIsNotNone(job_info)

    def test_get_description(self):
        # check it is a non empty list 
        job_description = self.scraper.get_description()
        self.assertIs(type(job_description), list)
        self.assertIsNotNone(job_description)

    def test_get_links(self):
        job_links = self.scraper.get_links()
        self.assertIs(type(job_links), list)
        self.assertIsNotNone(job_links)   
            
    def tearDown(self):
        self.scraper.driver.quit()
        del self.scraper

if __name__ == '__main__':
    unittest.main()