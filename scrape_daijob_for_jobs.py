import twill
from twill.commands import go, showforms, formclear, fv, submit
from twill.commands import url as turl
import urllib.parse
from twill.commands import find as tfind, browser
from bs4 import BeautifulSoup as bs

config = {
    'userid': 'user_id',
    'preferred_resume_id': 'resume_id_here',
    'username': 'email_here',
    'password': 'password_here'
}

def generate_page_url(page):
    url = 'https://www.daijob.com/en/jobs/search_result?sort_order=7&job_types[]=1301&job_types[]=1302&job_types[]=1303&job_types[]=1304&job_types[]=1305&job_types[]=1306&job_types[]=1307&job_types[]=1300&jt[]=1300&working_a_locations[]=230&working_a_locations[]=102&job_post_language=1&job_search_form_hidden=1'
    url += f"&page={page}"
    return url


#Login to daijob
go('https://www.daijob.com/en/member/reg_login?destination=members%2Fmypage&org_method_name=login')
formclear('1')
fv('1', 'user_name', config['username'])
fv('1', 'password', config['password'])
submit('0')

#Navigate first two pages
pages = [1, 2]

for pg in pages:
    u = generate_page_url(pg)
    go(u)
    if(not(urllib.parse.unquote(browser.url) == u)):
        print('Could not open {u}')
        continue
    soup = bs(browser.html)
    s = soup.find_all('a', id="_job")
    for job in s:
        try:
            job_id = job['href'].split('/')[-1]
            apply_url = f'https://www.daijob.com/en/{config["userid"]}/members/application/apply/{job_id}'
            go(apply_url)
            if len(browser.forms) == 0:
                print('Maybe already applied to job ' +job_id)
                continue

            formclear('1')
            fv('1','application[member_resume_en_id]', config["preferred_resume_id"])
            submit('submit','1')
            
            ## do I need to insert wait here?
            
            ## check if url stays the same, if so, means there was some error
            if(urllib.parse.unquote(browser.url) == apply_url):
                print('Application failed to '+job_id)
                continue
            ## else click on submit
            submit('submit','1')
            
            if(urllib.parse.unquote(browser.url) == f'https://www.daijob.com/en/{config["userid"]}/members/application/save'):
                print('Application submitted to '+job_id)
            else:
                print('Application failed to '+job_id)
        except Exception:
            continue