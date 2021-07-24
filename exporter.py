import csv 

def save_to_csv(jobs, file_name):
  if len(jobs)>0:
    file = open(f"{file_name}.csv", mode="w")
    writer = csv.writer(file)

    writer.writerow(["title", "company", "link"])
      
    for job in jobs:
      del job['type']
      writer.writerow(list(job.values()))