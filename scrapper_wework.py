import requests
from bs4 import BeautifulSoup

wework_base_url = "https://weworkremotely.com"
wework_url = "https://weworkremotely.com/remote-jobs"

def get_wework_jobs(word):

  print("##START WEWORK SCRAPPING..")
  jobs = []

  url = f"{wework_url}/search?term={word}"
  req = requests.get(url)
  soup = BeautifulSoup(req.text, "html.parser")

  job_lists_t= soup.find_all("section", class_="jobs")


  for job_list_t in job_lists_t:
   
    jobs_t = job_list_t.find_all("li")[:-1]
    
    for job_t in jobs_t:

      link = job_t.contents[2].get("href")
  
      link = f"{wework_base_url}{link}"
      
      
      title= job_t.find("span", class_="title").text
      company = job_t.find("span", class_="company").text

      job = {"title":title, "company":company, "link":link, "type":2}
      jobs.append(job)
  print("##END WEWORK SCRAPPING..")
  return jobs

