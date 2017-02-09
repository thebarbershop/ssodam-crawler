# ssodam statistics
# written in python 2.7.12

import sys
import mechanize
import requests
from lxml import html
from bs4 import BeautifulSoup

main_url = r"http://www.ssodam.com/"
login_url = r"http://www.ssodam.com/auth"
bbs_url = r"http://www.ssodam.com/board/5/1"

headers={'Referer':main_url}

def call_requests(id, password):
    session = requests.session()
    csrftoken = session.get(main_url).cookies['csrftoken']

    payload = {
        "id": id,
        "password": password,
        "auto": "false",
        "csrfmiddlewaretoken": csrftoken
    }

    session.post(login_url, data=payload, headers=headers)
    result = session.get(bbs_url)
    soup = BeautifulSoup(result.text, "lxml")
    print(soup.text)

def call_mechanize(id, password):
    b = mechanize.Browser()
    b.open(main_url)
    b.set_handle_robots(False)
    b.addheaders=[('Referer',main_url)]
    b.select_form(nr=0)
    b['id']=id
    b['password']=password
    try:
        print b.submit().read
    except 401:
        print "401 error"

def main():
    id, password = input("id: "),input("password: ")
    call_requests(id, password)

if __name__ == "__main__":
    main()