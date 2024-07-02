from bs4 import BeautifulSoup as bs
import re
def extract_1(content):
    finalcontent = ''
    toremove = ['link','script','style','iframe','object','noscript','param','embed','meta','base','canvas','svg']
    content_soup = bs(content.text, 'html.parser')
    for soup_body in content_soup.find_all('body'):
        for remove_tag in toremove:
            for trash_tag in soup_body.find_all(remove_tag):
                trash_tag.decompose()
        thisbody = soup_body.get_text()
        thisbody = thisbody.replace("\t",'')
        thisbody = re.sub(r"\n\w\n",'\n',thisbody)
        while True:
            old_body = thisbody
            thisbody = thisbody.replace('  ', ' ')
            if old_body == thisbody:
                break

        while True:
            old_body = thisbody
            thisbody = thisbody.replace('\n\n', '\n')
            if old_body == thisbody:
                break

        finalcontent = finalcontent + thisbody
    print('content Extracted')
    return finalcontent