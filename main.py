
import random
import threading
import time
from flask import Flask, render_template, request, redirect, send_file
from scrapper_remoteok import get_remoteok_jobs
from scrapper_stackoverflow import get_stackoverflow_jobs
from scrapper_wework import get_wework_jobs
from exporter import save_to_csv

STR_REMOTEOK = "remoteok"
STR_STACKOVERFLOW = "stackoverflow"
STR_WEWORK = "wework"

scrapper_type = (STR_REMOTEOK, STR_STACKOVERFLOW, STR_WEWORK)

db = {
  STR_REMOTEOK:{},
  STR_STACKOVERFLOW:{},
  STR_WEWORK:{}
}


class ExportingThread(threading.Thread):
    def __init__(self):
        self.progress = 0
        super().__init__()

    def run(self):
        # Your exporting stuff goes here ...
        for _ in range(10):
            time.sleep(1)
            self.progress += 10


exporting_threads = {}

app = Flask("GraduationAssignment")
app.debug = True


@app.route("/")
def index():
  
  return render_template("index.html")

@app.route('/search')
def search():
  
  language = request.args.get('language')
  
  jobs = []
  remoteok_jobs = []
  stackoverflow_jobs = []
  wework_jobs = []

  from_db = db[STR_REMOTEOK].get(language)
  
  if from_db:
    remoteok_jobs = from_db
    jobs.extend(remoteok_jobs)
  else:
    remoteok_jobs = get_remoteok_jobs(language)
    if len(remoteok_jobs)>0:
      jobs.extend(remoteok_jobs)
      db[STR_REMOTEOK][language] = remoteok_jobs


  from_db = db[STR_STACKOVERFLOW].get(language)

  if from_db:
    stackoverflow_jobs = from_db
    jobs.extend(stackoverflow_jobs)
  else:
    stackoverflow_jobs = get_stackoverflow_jobs(language)
    if len(stackoverflow_jobs)>0:
      jobs.extend(stackoverflow_jobs)
      db[STR_STACKOVERFLOW][language] = stackoverflow_jobs    


  from_db = db[STR_WEWORK].get(language)

  if from_db:
    wework_jobs = from_db
    jobs.extend(wework_jobs)
  else:
    wework_jobs = get_wework_jobs(language)
    
    if len(wework_jobs)>0:
      jobs.extend(wework_jobs)
      db[STR_WEWORK][language] = wework_jobs    


  return render_template("search.html", jobs=jobs, jobs_count = len(jobs),word=language, scrapper_type=scrapper_type)

@app.route("/export")
def export():
  try:
    word = request.args.get('word')
    if not word :
      print("word doesn't exist")
      raise Exception()

    word=word.lower()
    jobs = [] 
    
    r_jobs = db[STR_REMOTEOK].get(word)
    s_jobs = db[STR_STACKOVERFLOW].get(word)
    w_jobs = db[STR_WEWORK].get(word)

    if r_jobs:
      jobs.extend(r_jobs)
    if s_jobs:
      jobs.extend(s_jobs)
    if w_jobs:
      jobs.extend(w_jobs)

    if len(jobs)>0:
      save_to_csv(jobs, word)

    return send_file(f"{word}.csv", attachment_filename =f'{word}.csv', as_attachment=True)

  except:
    print("Exception")
    return redirect("/")


app.run(host="0.0.0.0")