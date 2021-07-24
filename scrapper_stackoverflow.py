import requests
import math
from bs4 import BeautifulSoup
stackoverflow_base_url="https://stackoverflow.com"
stackoverflow_url = "https://stackoverflow.com/jobs"

def get_page_num(word):
  url = f"{stackoverflow_url}?q={word}"

  req = requests.get(url)
  soup = BeautifulSoup(req.text, "html.parser")

  jobs_num = soup.find("span", class_="description").text
  jobs_num = jobs_num.replace("jobs", "").replace(",","").strip()
  page_num = int(jobs_num)
  page_num /=25
  page_num = math.ceil(page_num)
  
  return page_num


def get_jobs(url):
  jobs = []
  req=requests.get(url)
  soup = BeautifulSoup(req.text, "html.parser")
  jobs_t = soup.find_all("div", class_="-job")
  
  for job_t in jobs_t:
    anker = job_t.find("a", class_="s-link")
    title = anker.get("title")
    link = anker.get("href")
    link = f"{stackoverflow_base_url}{link}"

    company = job_t.find("h3", class_="fc-black-700").find("span").text.strip()

    job = {"title" : title, "company":company, "link":link, "type":1}
    jobs.append(job)
  
  return jobs


def get_stackoverflow_jobs(word):
  print("##START STACKOVERFLOW SCRAPPING..")
  jobs = []
  
  page_num = get_page_num(word)

  for i in range(1, page_num+1):
    print(f"[{i}/{page_num}] page scrapping..")
    url = f"{stackoverflow_url}?q={word}&pg={i}"
    temp_jobs= get_jobs(url)
    jobs.extend(temp_jobs)

  print("##END STACKOVERFLOW SCRAPPING..")
  return jobs