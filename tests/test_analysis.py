import sys
import unittest
sys.path.insert(1, '/Users/gabriellamartin/Web Scraping' )
from project.data_analysis import DataAnalysis

class TestDataAnalysis(unittest.TestCase):

    def setUp(self):
        self.analysis = DataAnalysis(test=1)

    '''
        mock_lists = [['','','','', 'Python and AWS is required'], ['','','','', 'aws and PANDAS'],
                           ['','','','', 'PYTHON PYTHON'], ['','','','', 'pandas python']]
        The mock list are designed to ensure that the following conditions are met in the data analysis:
        python , Python and PYTHON all respond the same way
        the last descriptions "PYTHON PYTHON" ensures that if we test skill python, it will only be counted 
        once so no false over-estimated
         
        So with this in mind this is what we expect for this process:
         - Prominance of Python: 75%
         - Prominance of AWS: 50%
         - Prominance of Pandas: 50% '''

    def test_get_list_of_descriptions_only(self):
        expected = ['Python and AWS is required','aws and PANDAS','PYTHON PYTHON','pandas python']
        actual = self.analysis.get_list_of_descriptions_only()
        self.assertEqual(actual, expected)

    def test_find_prominance_of_skill(self):

        list_of_descriptions = self.analysis.get_list_of_descriptions_only()
        skill_queries = ['aws', 'python', 'pandas']
        expected = (['aws', 'python', 'pandas'], [50,75, 50])
        actual = self.analysis.find_prominance_of_skill(list_of_descriptions)
        self.assertEqual(actual, expected)

    def test_make_skill_dictionary(self):
     
        skills_and_percentages = (['aws', 'python', 'pandas'], [50,75, 50])
        expected = {'aws':50, 'python':75, 'pandas':50}
        actual = self.analysis.make_skill_dictionary(skills_and_percentages)
        self.assertEqual(actual, expected)
        
    def order_dictionary(self):

        dictionary_of_skills_and_percentages = {'aws':50, 'python':75, 'pandas':50}
        actual = self.analysis.order_dictionary(dictionary_of_skills_and_percentages)
        expected = {'python':75,'aws':50,'pandas':50}
        self.assertEqual(actual, expected)

    def tearDown(self):
        del self.analysis
        
if __name__ == '__main__':
    unittest.main()