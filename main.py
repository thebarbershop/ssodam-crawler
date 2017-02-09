# ssodam statistics
# written in python 2.7.13

import sys
import time
import requests
from lxml import html
from bs4 import BeautifulSoup

main_url = r"http://www.ssodam.com/"
login_url = r"http://www.ssodam.com/auth"
bbs_url_base = r"http://www.ssodam.com/board/5/"

def call_requests(id, password):
    session = requests.session()

    # login
    csrftoken = session.get(main_url).cookies['csrftoken']
    payload = {
        "id": id,
        "password": password,
        "auto": "false",
        "csrfmiddlewaretoken": csrftoken
    }
    result = session.post(login_url, data=payload, headers={'Referer':main_url})
    if result.status_code != 200:
        return "Login Failure"
    result = session.get(bbs_url_base+"1")
    soup = BeautifulSoup(result.text, "lxml")
    max_page=int(soup.text[soup.text.find("max_page"):].split('\n')[0][0:-1].split(" ")[1])

    # open board
    start_time=time.time()
    print(soup.find_all(name="label label-info"))
'''
    for page in range(1,max_page+1):
        bbs_url = bbs_url_base+str(page)
        result = session.get(bbs_url)
        print("Reading page %d of %d (%.2f%%, %d ms)"%(page, max_page, 100.0*page/max_page, time.time()-start_time))
'''
#    return "Successful termination"

def main():
    id, password = raw_input("id: "), raw_input("password: ")
    print(call_requests(id, password))

if __name__ == "__main__":
    main()