from setuptools import setup
from setuptools import find_packages

setup(
    name= 'google_jobs_scraping',
    version= '0.0.1',
    description= 'Scrapes google jobs for any search query, processes the data and crates a spreadsheet. Also analyses the description to find repeatable skills',
    url= 'https://github.com/gabriella-martin/Web-Scraping',

    author= 'Gabriella Martin',
    license = 'MIT',
    packages= find_packages(),
    install_requires = ['selenium', 'openpyxl', 'webdriver-manager']
)

