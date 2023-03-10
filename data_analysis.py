import pickle

class DataAnalysis():

    '''This class enables data analysis to be done on the job descriptions and gain insight in to the job
    market as a whole'''

    def __init__(self, test=None):

        '''Opens the full formatted job list, the test argument is used for testing purposes'''
        self.test = test

        if self.test == None:
           with open('full_info_list', 'rb') as fil:
                self.job_info_formatted = pickle.load(fil)

        else:
            with open('tests/mock_lists/mock_info_list', 'rb') as fil:
                self.job_info_formatted = pickle.load(fil)            

    def get_list_of_descriptions_only(self):

        '''This function retrieves only the job descriptions into a new list as we want to analyse only
        the descriptions'''

        list_of_descriptions = []
        for info in self.job_info_formatted:
            list_of_descriptions.append(info[4])
        return(list_of_descriptions)

    def find_prominance_of_skill(self,list_of_descriptions):

        '''This function repeatedly asks the user for a particular skill, like 'AWS', it then searches each 
        description and if the skill is found in the description a count is increased, once done this count
        is then turned into a percentage of prominance of skill by taking the number of descriptions that the
        skill appeared in and dividing by the total of the descriptions
        
        By specifying that the count must be >1 we remove any arbitrary skill searches from our final list.
        Each sucessful search query and corresponding percentage of prominance is added to a list'''

        skill_query = []
        percentages_of_skills = []

        while True:
            skill_query = str(input('What skill would you like to search for? If you are done type quit ')).lower()
            if skill_query == 'quit':
                break
            else:
                count = 0
                for desc in list_of_descriptions:
                    desc = desc.lower()
                    if skill_query in desc:
                        count += 1
                if count > 1:
                    percentage_of_skill = round((count/len(list_of_descriptions))*100)
                    skill_query.append(skill_query)
                    percentages_of_skills.append(percentage_of_skill)

        return(skill_query, percentages_of_skills)

    def make_skill_dictionary(self, skills_and_percentages):

        '''This function takes both the skill queried list and percentages and creates a dictionary'''
        skill_query = skills_and_percentages[0]
        percentages_of_skills = skills_and_percentages[1]
        dictionary_of_skills_and_percentages = {skill_query[i]: percentages_of_skills[i] for i in range(len(skill_query))}

        return(dictionary_of_skills_and_percentages)

    def order_dictionary(self, dictionary_of_skills_and_percentages):

        '''This function takes the dictionary and orders in in descending order - so most important technologies
        are seen first'''
        sorted_dictionary_of_skills = {}

        ordered_values = sorted(dictionary_of_skills_and_percentages.values())
        ordered_values.reverse()
        for i in ordered_values:
            for k in dictionary_of_skills_and_percentages.keys():
                if dictionary_of_skills_and_percentages[k] == i:
                    sorted_dictionary_of_skills[k] = dictionary_of_skills_and_percentages[k]
        print(sorted_dictionary_of_skills)

    def analyse_data(self):

        '''This function compiles the entire data analysis process'''

        list_of_descriptions = self.get_list_of_descriptions_only()
        skills_and_percentages = self.find_prominance_of_skill(list_of_descriptions)
        dictionary_of_skills_and_percentages = self.make_skill_dictionary(skills_and_percentages)
        self.order_dictionary(dictionary_of_skills_and_percentages)

if __name__ == '__main__':
    da = DataAnalysis()
    da.analyse_data()