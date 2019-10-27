import random
import re
import json
import datetime


class tParamAlternative:
  def __init__(self):
    pass

def fixKey(key):
  new_key = key.lower().replace('-','_').replace(' ', '_').replace(',', '_')
  return new_key

def getKeys(text, strip=True):
  if text is None:
    return []

  matches = re.findall(r"\{[^\{\}]*\}", text)

  result = [(m[1:-1] if strip else m) for m in matches]
  return result

class tEntry:
  def __init__(self, text):
    # if isinstance(text, str):
    self.template = self.fixKeys(text)
    # else:
      # self.template = text

  def format(self, context):
    try:
      return self.template.format(**context)
    except Exception as e:
      return ""

  def keys(self):
    return getKeys(self.template)

  def fixKeys(self, text):
    new_text = text[:]  # cl = Client(doc, context)
  # print(cl.get())  # cl = Client(doc, context)
  # print(cl.get())
    for old_key in getKeys(text, False):
      # print(old_key, fixKey(old_key))
      # new_text.replace(old_key, old_key)
      new_text = new_text.replace(old_key, fixKey(old_key))

    # print(new_text)
    return new_text

class tSet:
  def __init__(self, items):
    self.items = items

  def format(self, context):
    return random.choice(self.items).format(context)

  def keys(self):
    keys = []

    for item in self.items:
      keys.extend(item.keys())

    return keys

class tDocument:
  def __init__(self, sets):
    self.items = sets

  def keys(self):
    keys = []

    for item in self.items:
      keys.extend(item.keys())

    return set(keys)

  def format(self, context):
    text = [item.format(context) for item in self.items]

    return " ".join(text)

class Client:
  def __init__(self, document, context):
    self.document = document
    self.context = context

  def get(self):
    return self.document.format(self.context).replace("<br>", "\n   ")

def removeSeqDup(items):
  result = [items[0]]
  for item in items[1:]:
    if item != result[-1]:
      result.append(item)

  return result

def splitAt(items, delimiter):
  result = []
  chunk = []
  for item in items:
    if item == delimiter:
      result.append(chunk)
      chunk = []
    else:
      chunk.append(item)

  if chunk != []:
    result.append(chunk)

  return result

def buildDocumentTemplate(fname):
  lines = []
  with open(fname) as f:
    for line in f:
      if line.startswith("*"):
        line = ''
        lines.append("<br>")
      else:
        lines.append(line.strip())

  lines = removeSeqDup(lines)
  # print(lines)

  chunks = splitAt(lines, '')
  # print(chunks)

  doc = tDocument([])
  for chunk in chunks:
    if chunk != []:
      entries = [tEntry(item) for item in chunk]
      tset = tSet(entries)
      doc.items.append(tset)

  return doc

def loadSrc(fname):
  with open(fname, "r") as read_file:
    return read_file.read()

def bind(foo, dst, dst_k):
  try:
    dst[dst_k] = foo()
  except Exception as e:
    # print("err")
    pass

def startYear(src):
  years = sorted(list(map(int, re.findall(r"\d{4}", src))))
  return str(years[0])

def endYear(src):
  years = sorted(list(map(int, re.findall(r"\d{4}", src))))
  return str(years[-1])

def yearSuffix(val):
  if val == 0:
    return "a few months"
  elif val == 1:
    return " a year"
  else:
    return str(val) + " years"

def yearsRange(src):
  years = sorted(list(map(int, re.findall(r"\d{4}", src))))
  # print(years)
  val = years[-1] - years[0]

  return yearSuffix(val)

def startYears(src):
  year = sorted(list(map(int, re.findall(r"\d{4}", src))))[0]
  return yearSuffix(datetime.datetime.now().year - year)

def endYears(src):
  year = sorted(list(map(int, re.findall(r"\d{4}", src))))[-1]

  val = year - datetime.datetime.now().year
  return yearSuffix(val)

def getSubjects(skills, num):
  subjects = [x["name"] for x in random.sample(skills, k=num)]
  return ", ".join(subjects)

def getLanguage(skills, jobs):
  langs = ["C#", "Java", "C++", "HTML", "CSS", "JavaScript", "Python", "Haskell", "Bash", "SQL", "F#", "TypeScript", "Cotlin", "Racket", "R", "Julia", "Scheme", "Lisp", "Prolog"]
  subjects = set([x["name"] for x in skills])
  job_subj = []
  for job in jobs:
    job_subj.extend(x["keyPhrases"])

  subjs = subjects | job_subj
  lang = langs & subjs

  return str(random.choice(lang))
  # return str(random.choice(subjects))

def getSoftSkill(skills):
  sskills = ["project management", "interpersonal skills", "project lead"]
  return str(random.choice(sskills))

def getSubject(skills, order = None):
  if order is None:
    return str(random.choice(skills)["name"])
  else:
    return str(skills[order]["name"])

def getTask(jobs):
  return str(random.choice(jobs[0]["keyPhrases"]))

def qualification(jobs, num):
  return str(random.choice(jobs[-num]["keyPhrases"]))

def jobSkill(jobs, i, seq):
  return jobs[i]["keyPhrases"][-seq]

def fuseKeys(src, dst, text):
  general = src['general']
  jobs = src['jobs']
  skills = src['skills'][0]
  # print(random.choice(skills)["name"])
  schools = src['schools']
  # print(endYears(schools[0]["dateRange"]))

  # bind = lambda src_k, dst_k: tryFill(general, jobs, skills, schools, src_k, dst_k, dst)

  # bind(general, "", dst, "")
  # bind(general, "", dst, 'achievement_1')
  bind(lambda: getSubject(skills, 0), dst, 'achievement_1')
  bind(lambda: schools[-1]["degree"], dst, 'edu1_qualification')
  bind(lambda: schools[-1]["degreeSpec"], dst, 'edu1_subject')
  bind(lambda: schools[-1]["degreeSpec"], dst, 'edu1_subject_1')
  bind(lambda: yearsRange(schools[-1]["dateRange"]), dst, 'edu1_years')
  bind(lambda: getSubject(skills, 0), dst, 'edu2_subject')
  bind(lambda: getSubject(skills, 1), dst, 'edu2_subject_1')
  bind(lambda: getSubject(skills, 2), dst, 'edu2_subject_2')
  bind(lambda: getSubject(skills, 3), dst, 'edu2_subject_3')
  bind(lambda: schools[-3]["degree"], dst, 'edu3_qualification')
  bind(lambda: getSubjects(skills, 3), dst, 'edu3_subject_1_2_3')
  bind(lambda: startYear(schools[-3]["dateRange"]), dst, 'edu3_year')
  bind(lambda: schools[-1]["schoolName"], dst, 'edu_organisation_1')
  bind(lambda: yearsRange(schools[-1]["dateRange"]), dst, 'edu_organisation_1_years')
  bind(lambda: schools[-2]["schoolName"], dst, 'edu_organisation_2')
  bind(lambda: schools[-3]["schoolName"], dst, 'edu_organisation_3')
  bind(lambda: schools[0]["schoolName"], dst, 'edu_organisation_c')
  bind(lambda: endYear(schools[0]["dateRange"]), dst, 'educ_end_year')
  bind(lambda: getSubjects(skills, 3), dst, 'educ_subject_1_2_3')
  bind(lambda: endYear(schools[0]["dateRange"]), dst, 'end_year_c')
  bind(lambda: endYears(schools[0]["dateRange"]), dst, 'end_years_c')
  bind(lambda: getLanguage(skills), dst, 'language_1')
  bind(lambda: getLanguage(skills), dst, 'language_2')
  bind(lambda: getLanguage(skills), dst, 'language_3')
  bind(lambda: schools[-1]["degree"], dst, 'qualification_1')
  bind(lambda: schools[-3]["degree"], dst, 'qualification_3')
  bind(lambda: getSubject(skills, 0), dst, 'skill_1')
  bind(lambda: getSubject(skills, 1), dst, 'skill_2')
  bind(lambda: getSubject(skills, 2), dst, 'skill_3')
  bind(lambda: getSubject(skills, 3), dst, 'skill_4')
  bind(lambda: getSoftSkill(skills), dst, 'soft_skill_1')
  bind(lambda: getSoftSkill(skills), dst, 'soft_skill_2')
  bind(lambda: getSoftSkill(skills), dst, 'soft_skill_3')
  bind(lambda: schools[-1]["degree"], dst, 'start_achievement')
  bind(lambda: yearsRange(text), dst, 'start_few')
  bind(lambda: schools[-1]["degreeSpec"], dst, 'start_subject')
  bind(lambda: getTask(jobs), dst, 'start_task_1')
  bind(lambda: getTask(jobs), dst, 'start_task_2')
  bind(lambda: getTask(jobs), dst, 'start_task_3')
  bind(lambda: jobs[-1]["jobTitle"], dst, 'start_title')
  bind(lambda: jobs[-1]["companyName"], dst, 'start_work_place')
  bind(lambda: startYear(text), dst, 'start_year')
  bind(lambda: startYears(text), dst, 'start_years')
  bind(lambda: getSubject(skills, 0), dst, 'subject_1')
  bind(lambda: getSubjects(skills, 3), dst, 'subject_1_2_3')
  bind(lambda: getSubject(skills, 1), dst, 'subject_2')
  bind(lambda: getSubject(skills, 2), dst, 'subject_3')
  bind(lambda: getTask(jobs), dst, 'task_1')
  bind(lambda: getTask(jobs), dst, 'task_2')
  bind(lambda: getTask(jobs), dst, 'task_3')
  bind(lambda: jobs[-1]["jobTitle"], dst, 'title_1')
  bind(lambda: jobs[-2]["jobTitle"], dst, 'title_2')
  bind(lambda: jobs[0]["jobTitle"], dst, 'title_c')
  bind(lambda: startYear(jobs[-1]["dateRange"]), dst, 'work1_start_year')
  bind(lambda: jobSkill(jobs, 0, 0), dst, 'work1_subject')
  bind(lambda: jobSkill(jobs, 1, 0), dst, 'work2_skill_1')
  bind(lambda: jobSkill(jobs, 1, 1), dst, 'work2_skill_2')
  bind(lambda: jobSkill(jobs, 1, 2), dst, 'work2_skill_3')
  bind(lambda: startYear(jobs[-2]["dateRange"]), dst, 'work2_year')
  bind(lambda: yearsRange(jobs[-2]["dateRange"]), dst, 'work2_years')
  bind(lambda: yearsRange(jobs[-1]["dateRange"]), dst, 'work_place1_years')
  bind(lambda: jobs[-1]["companyName"], dst, 'work_place_1')
  bind(lambda: jobs[-2]["companyName"], dst, 'work_place_2')
  bind(lambda: jobs[0]["companyName"], dst, 'work_place_c')
  bind(lambda: getSubject(skills), dst, 'work_subject_1')
  bind(lambda: startYear(jobs[-1]["dateRange"]), dst, 'work_year_1')
  bind(lambda: startYears(jobs[0]["dateRange"]), dst, 'work_years_c')

  # print(schools)

def chooseTemplate(context):
  templates = ["education1.txt", "education2.txt", "blended1.txt", "carreer1.txt", "carreer2.txt"]
  return random.choice(templates)


def magicFoo(json_context):
  src = json.loads(json_context)
  context = dict()
  fuseKeys(src, context, json_context)

  doc = buildDocumentTemplate(chooseTemplate(context))

  cl = Client(doc, context)
  return cl.get()

def main():
  request = loadSrc("src.json")
  print(magicFoo(request))

if __name__ == '__main__':
  main()