import unittest 
from refactored import Scraper


''' 
Questions:

- 6 tests takes 180 seconds seems long but not sure if fine - i have many waits in other program to ensure 
everything loads prior to scraping
- not sure how to test the scroller
- not sure if tests are thorough enough
- is it okay to put all the method calls in the setUP?
- two other functions pickle and scrape - do these need a unit test?'''



class ScraperTestCase(unittest.TestCase):
    def setUp(self):
        self.scraper = Scraper('data science', 'london', '2')
        self.cookies = self.scraper.accept_cookies()
        self.location = self.scraper.specify_location()
        self.job_info = self.scraper.get_job_info()
        self.job_description = self.scraper.get_description()
        self.job_links = self.scraper.get_links()

    def test_accept_cookies(self):
        
        try:
            expected1 = 'Cookies Accepted'
            self.assertEqual(self.cookies, expected1)
            
        except:
            expected2 = 'No Cookies To Accept'
            self.assertEqual(self.cookies, expected2)
    
    def test_specify_location(self):
        
        try:
            expected1 = 'Location and Radius inputted'
            self.assertEqual(expected1,self.location)
        
        except:
            expected2 = 'Explained fault to user and exited program'
            self.assertEqual(expected2, self.location )

    def test_scroll_to_load(self):
        # not sure how to test this
        pass
    
    def test_get_job_info(self):
        # check it is a non empty list 
        self.assertIs(type(self.job_info), list)
        self.assertIsNotNone(self.job_info)

    def test_get_description(self):
        # check it is a non empty list 
        self.assertIs(type(self.job_description), list)
        self.assertIsNotNone(self.job_description)

    def test_get_links(self):
        self.assertIs(type(self.job_links), list)
        self.assertIsNotNone(self.job_links)   
            
    def tearDown(self):
        self.scraper.driver.quit()
        del self.scraper

if __name__ == '__main__':
    unittest.main()