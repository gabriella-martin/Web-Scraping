import unittest

import sys 

sys.path.insert(1, '/Users/gabriellamartin/Web Scraping' )
from DataAnalysis import DataAnalysis
class TestDataAnalysis(unittest.TestCase):

    def setUp(self):
        self.analysis = DataAnalysis(test=1)

    def test_get_list_of_descriptions_only(self):
        expected = ['Python and AWS is required','aws and PANDAS','PYTHON PYTHON']
        actual = self.analysis.get_list_of_descriptions_only()
        self.assertEqual(actual, expected)

    def test_find_prominance_of_skill(self):
        skill_queries = []
        skill_query = 'python'
        list_of_descriptions = ['Python and AWS is required','aws and PANDAS','PYTHON PYTHON']
        expected = (['python'], [33])
        actual = self.analysis.find_prominance_of_skill(list_of_descriptions, skill_query)
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()