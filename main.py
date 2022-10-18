# getting first page
from serpapi import GoogleSearch

params = {
  "device": "desktop",
  "engine": "google_jobs",
  "google_domain": "google.co.uk",
  "q": "junior python",
  "hl": "en",
  "gl": "uk",
  "location": "Greater London, England, United Kingdom",
  "api_key": "711701a99280f41babc89caa35a4479b34657d3fe85a3bd97aeff6ee82f9c32e"
}

search = GoogleSearch(params)
results = search.get_dict()

job_list = (results['jobs_results'])

for job in job_list:
    print(job['description'])