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
