import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

remoteok_url = "https://remoteok.io"

def get_remoteok_jobs(language):
  print("##START REMOTEOK SCRAPPING..")
  jobs = []
  
  req = requests.get(f"{remoteok_url}/remote-{language}-jobs", headers=headers)

  soup = BeautifulSoup(req.text, "html.parser")
  
  job_list = soup.find_all("tr", class_="job")
  
  for job in job_list:
    
    company = job.find("td", class_="company")
    title = company.find("h2", itemprop="title").text
    company_name= company.find("h3", itemprop="name").text  
    link = company.find("a", itemprop="url").get('href')
    link = f"{remoteok_url}{link}"
    
    #print(title, company_name, link)
    
    job_dict = {"title" : title , "company" : company_name, "link":link, "type":0}

    jobs.append(job_dict)

  print("##END REMOTEOK SCRAPPING..")
  return jobs