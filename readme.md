<h2 align="center">Web-Scraping Google Jobs</h2>


<h4 align="center">Languages and Technologies</h4>

<div align="center">
	  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/selenium/selenium-original.svg" height="40" width="52"   />
	  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original-wordmark.svg" height="40" width="52"   />
	    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg" height="40" width="52"  />
	<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original-wordmark.svg" alt="html5" width="40" height="40"/>
	<img src="https://github.com/sempostma/office365-icons/blob/master/png/64/excel.png?raw=true" alt="html5" width="40" height="40"/>

<h3 align="center">Introduction</h3>

---

<div align="left">

 Job searching is a notoriously time-consuming process and searching for jobs in tech confounds this issue. With each job requesting a unique tech stack, it can be difficult to manually parse through this data to find the best suited jobs for you to apply to. This program tries to alleviate some of these issues by scraping job postings from Google Jobs for a specified search query, processes the data, analyses the data and stores it in a  Excel spreadsheet. I chose Google Jobs over other viable options as I find it has the best job search capabilities; it only returns job postings for exactly what you search 

<h3 align="center"> 🔍 Google Jobs Website</h3>

---

<p align="center">
  <img src="images/googlejobs.png" />
</p>

The Google Jobs website is a highly dynamic and pageless (infinite scroll) website that does not respond well with a regular web scraping method like requests. In order to properly scrape the data, rather than attempt to call the backend server for information, we must simulate a front-end user with Selenium and Chrome-Driver

In order to make my code versatile I began the scraper by asking the user for a job search query, including what job, what location and what radius to search in. This allows me to collect data from different search queries easily without altering any code

<h3 align="center">🕸️ Scraping the Data </h3>

---

My first class, the **Scraper** class, does the following:

- Initialises the scraper by setting up the ChromeDriver and asking the user for their search query
- Accept the cookies button for us (if one pops up)
- Click on the user's inputted location and radius
- Scrolls down the page into all the postings have been loaded
- Scrapes all relevant information from each job posting
- Pickles this as a list for use in the next step

🫙 Pickling between steps (saving in local storage) ensures I was able to process the data without recalling the entire scraper class which helps us avoid getting our IP banned for behaving strangly and saves time as the process of scraping takes a few minutes 

<h3 align="center">🚧 Processing the Data </h3>

---

The **Data Processing** class cleans and processes the data and adds it a an Excel spreadsheet. Here in excel I can customisably track each job for example I can delete those that I am not interested in, track application status and add any relevant follow on details

Here is an example of a search I did for a friend who was looking at data science jobs in London; this process happens automatically when the script is ran

<p align="center">
  <img src="images/excel.png" />
</p>

<h3 align="center"> 📉 Analysing the Data</h3>

---

In my final class **Data Analysis** I wanted to analyse the job requirements for specific roles at the aggregate level, so I could get market wide information. Scraping Google Jobs over say Indeed or Linkedin was important for achieving a solid analysis as unlike the other options, Google Jobs returns only specifically what you search for, if you ask for only internships thats all they will provide you with. The job of this class is to analyse the tech stacks for certain job roles and have a guideline for what technology is most in demand for employers in each specific role. For data science, I can ask about the prominance of each skill and my script will return an ordered list of percentage prominance for each skill. The prominance calculate by what percent of all the scraped job postings include the term in their description 

<p align="center">
  <img src="images/percentages.png" />
</p>

UNIT TESTING 