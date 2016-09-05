from bs4 import BeautifulSoup
import requests
from spacy.en import English
from tqdm import tqdm_notebook

def StringToFunction(func_name):
    possibles = globals().copy()
    possibles.update(locals())
    func = possibles.get(func_name)
    if not func:
        raise NotImplementedError("Function %s not implemented" % func_name)
    return func

class JobScraper(object):
    def __init__(self, spider, parmdata):
        self.spider = StringToFunction(spider)
        self.parmdata = parmdata

    def Spider(self,*argv):
        jobs = []
        nlp = English()
        self.data = list()
        for joburl in self.spider(self,*argv):
            self.data.append(dict())
            r = requests.get(joburl, cookies=self.cookies)
            soup = BeautifulSoup(r.text,"lxml")
            content = soup.body.find('div', attrs={'id':'ctl00_MainContent_PrimaryContent'})
            jobs.append(dict())
            for span in content.span.find_all('span',recursive=True):
                  if span.has_attr('aria-labelledby'):
                        #print span['id'] + " : " + span.text
                        self.data[-1][span['id']] = span.getText(separator=u' ')
                        #doc = nlp(span.text)
                        #for np in doc.noun_chunks:
                        #    np.text

def NullSpider(url):
    yield url

def DullSpider(url):
    yield url + 'dull'

def BrassRingSpider(self):
    # we need to get the cookies from this "base url" to make subsequent queries
    self.parmdata['baseurl'] = "%s/searchopenings.aspx?partnerid=%s&siteid=%s"%(self.parmdata['site'],self.parmdata['partnerid'],self.parmdata['siteid'])
    baser = requests.get(self.parmdata['baseurl'])
    self.cookies = baser.cookies

    # identify the url for performing search queries
    searchpage = dict()
    soup = BeautifulSoup(baser.text,"lxml")
    search = soup.find_all('form',attrs={'id' : 'aspnetForm'})

    # loop over search result pages; each page contains 50 listings by default
    startrecord = 1
    while True:
        searchpage['url'] = "%s/%s"%(self.parmdata['site'],search[0]['action'])
        headers = {'recordstart':startrecord}
        searchpage['data'] = requests.post(searchpage['url'],cookies=baser.cookies,data=headers)
        searchpage['soup'] = BeautifulSoup(unicode(searchpage['data'].text),"lxml")
        for maincontent in searchpage['soup'].find_all('input',attrs={'id':'ctl00_MainContent_GridFormatter_json_tabledata'}):
            if maincontent.has_attr('id'):
                subsoup = BeautifulSoup(maincontent['value'],"lxml")
                for job in subsoup.find_all('input',attrs={'name':'chkJobClientIds'}):
                    jobid = job['id']
                    joburl = "%s/jobdetails.aspx?jobId=%s&JobSiteId=%s"%(self.parmdata['site'],jobid,self.parmdata['siteid'])
                    yield joburl

        numjobs = int(searchpage['soup'].find('input',{'name':'totalrecords'})['value'])
        if startrecord == 1:
            bar = tqdm_notebook(total=numjobs)
        bar.update(50)
        if startrecord + 50 >= numjobs:
            break
        else:
            startrecord = startrecord + 50

def NullSpider(url):
    yield url

def DullSpider(url):
    yield url + 'dull'

def BrassRingSpider(self):
    # we need to get the cookies from this "base url" to make subsequent queries
    self.parmdata['baseurl'] = "%s/searchopenings.aspx?partnerid=%s&siteid=%s"%(self.parmdata['site'],self.parmdata['partnerid'],self.parmdata['siteid'])
    baser = requests.get(self.parmdata['baseurl'])
    self.cookies = baser.cookies

    # identify the url for performing search queries
    searchpage = dict()
    soup = BeautifulSoup(baser.text,"lxml")
    search = soup.find_all('form',attrs={'id' : 'aspnetForm'})

    # loop over search result pages; each page contains 50 listings by default
    startrecord = 1
    while True:
        searchpage['url'] = "%s/%s"%(self.parmdata['site'],search[0]['action'])
        headers = {'recordstart':startrecord}
        searchpage['data'] = requests.post(searchpage['url'],cookies=baser.cookies,data=headers)
        searchpage['soup'] = BeautifulSoup(unicode(searchpage['data'].text),"lxml")
        for maincontent in searchpage['soup'].find_all('input',attrs={'id':'ctl00_MainContent_GridFormatter_json_tabledata'}):
            if maincontent.has_attr('id'):
                subsoup = BeautifulSoup(maincontent['value'],"lxml")
                for job in subsoup.find_all('input',attrs={'name':'chkJobClientIds'}):
                    jobid = job['id']
                    joburl = "%s/jobdetails.aspx?jobId=%s&JobSiteId=%s"%(self.parmdata['site'],jobid,self.parmdata['siteid'])
                    yield joburl

        numjobs = int(searchpage['soup'].find('input',{'name':'totalrecords'})['value'])
        if startrecord == 1:
            bar = tqdm_notebook(total=numjobs)
        bar.update(50)
        if startrecord + 50 >= numjobs:
            break
        else:
            startrecord = startrecord + 50
