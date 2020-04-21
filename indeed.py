import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?as_and=python&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&as_src=&radius=25&l=&fromage=any&limit={LIMIT}&sort=&psf=advsrch&from=advancedsearch"

def get_last_page():
  #only use python, get load url? => possible
  #but you use package, it is very comfortable
  result = requests.get(URL)

  ##take all html 
  #print(indeed_result.text)
  ##beatifulsoup is very useful library to extract information

  ## it is alert that i wll use html.parser
  soup = BeautifulSoup(result.text, "html.parser")

  ##i want to use pargination div tag
  pagination = soup.find("div", {"class":"pagination"})

  ##on pagination, find a tag
  links = pagination.find_all('a')

  ##in links, find span tag
  pages = []
  ## after find span, input pages array
  for link in links[:-1]:
    link.find("span")
    ##we take only text(string)
    pages.append(int(link.string))
  ##pages[-1] gave last item
  ##pages[:-1] gave except last item 
  ##we take last number(the biggest number)
  max_page = pages[-1]
  return max_page

def extract_job(html):
  title = html.find("h2", {"class":"title"}).find("a")["title"]
  company = html.find("span", {"class":"company"})
  company_anchor =  company.find("a")
  if company_anchor is not None:
    company= str(company_anchor.string)
  else :
    company = str(company.string)
  company = company.strip( )
  location = html.find("div", {"class":"recJobLoc"})["data-rc-loc"]
  job_id = html["data-jk"]

  return {'title': title, 'company': company, 'location': location, "link": f"https://kr.indeed.com/%EC%B1%84%EC%9A%A9%EB%B3%B4%EA%B8%B0?jk={job_id}"}

def extract_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping indeed : page: {page}")
    result = requests.get(f"{URL}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs

def get_jobs():
  last_page = get_last_page()
  jobs = extract_jobs(last_page)
  return jobs