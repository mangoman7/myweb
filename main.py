import urllib.parse
import requests
import json
import re
from bs4 import BeautifulSoup as bs
import urllib
from concurrent.futures import ThreadPoolExecutor
from patterns import patterns
patterns = patterns()
def bing_serach(query,ifextract=False):
    query = urllib.parse.quote_plus(query)
    url= 'https://www.bing.com/search?q=' + query
    print(url)
    bingr = requests.get(url,headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
    # print(bingr.text)
    def rm_escape(string):
        return string.replace('\n','')
    soup = bs(bingr.text,'html.parser')
    linkscont = soup.find_all(id="b_results")
    results = []
    ino = 0
    for linkcont in linkscont:
        listcont = linkcont.find_all(class_='b_algo')
        # print(listcont)
        for cont in listcont:
            ino+=1
            try:
                icon = 'https:'+cont.find_all(class_='rms_iac')[0].get('data-src')
            except:
                icon ='could not retrieve'
            try:
                URL = cont.find_all(class_='tilk')[0].get('href')
            except:
                print('INDEX: ', ino ,'could not extract')
                continue
            try:
                Title = cont.find_all('h2')[0].get_text()
            except:
                Title = 'Could Not Retrieve'
            try:
                Abstract = cont.find_all(class_='b_caption')[0].get_text()
                if(Abstract == ''):
                    Abstract = cont.find_all(class_='b_algoSlug')[0].get_text()
                else:
                    print('Abstract From First Logic for',URL,'\n',Abstract)
                    pass
            except:
                try:
                    Abstract = cont.find_all(class_='b_algoSlug')[0].get_text()
                except:
                    Abstract = 'Could Not Retrieve'
            try:
                # class_='b_rc_gb_sub_column'['itrate']>tag='div'>[Title{class_='b_rc_gb_sub_title'}.get_text(),Description{clss_='b_rc_gb_text_wrapper '.get_text()}]
                other = []
                for columns in cont.find_all(class_='b_rc_gb_sub_column'):
                    for column in columns.find_all('div'):
                        try:
                            thistitle = column.find_all(class_='b_rc_gb_sub_title')[0].get_text()
                        except:
                            thistitle = 'Could Not Retrieve'
                        try:
                            thisdescription = column.find_all(class_='b_rc_gb_text_wrapper')[0].get_text()
                            other.append({'Title':thistitle,'Description':thisdescription})
                        except:
                            pass
            except:
                other = 'None'            
            results.append({
                'no':ino-1,
                'icon': icon,
                'URL': URL,
                'Title': Title,
                'Abstract': Abstract,
                'other':other

            })
        rquestions = linkcont.find_all(id='relatedQnAListDisplay')
        for rq in rquestions:
            conts = rq.find_all(attrs={'role':'listitem'})
            for cont in conts:
                try:
                    Title = cont.find_all(class_='df_qn_syd')[0].get_text()
                except:
                    Title = 'Could Not Extract Title'
                try:
                    Abstract = cont.find_all(class_='df_alsocon_link')[0].get_text()
                except:
                    Abstract = 'Could Not Extract Title'
                try:
                    URL = cont.find_all(class_='df_alsocon_link')[0].get('href')
                except:
                    continue
                try:
                    icon = 'https:'+cont.find_all(class_='rms_iac')[0].get('data-src')
                except:
                    Title = 'Could Not Extract Title'
                results.append({
                'icon': icon,
                'URL': URL,
                'Title': Title,
                'Abstract': Abstract,

                })
    if(ifextract):
        with ThreadPoolExecutor() as web_extract_executor:
            for result in results:
                result['webpage'] = web_extract_executor.submit(extract_web,result)

        for result in results:
            result['webpage']=result['webpage'].result()
        return results
    else:
        return results



def extract_web(result):
    content = requests.get(result['URL'],verify=False)
    print(content.status_code)
    for pattern in patterns:
        if(re.match(pattern['recode'],result['URL'])):
            return pattern['function'](content)
                # return ('There is some error with This Pattern\n','Pattern Name',pattern['Title'],'\nPattern Id',pattern['id'])
    
    