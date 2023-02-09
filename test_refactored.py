import unittest 
import refactored

class TestScraper(unittest.TestCase):
    def test_get_job_info(self):
        actual = self.test_get_job_info()
        expected = []
        self.assertEqual(actual, expected)

a = TestScraper()

a.test_get_job_info()