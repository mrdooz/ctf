import requests
import getpass
import hashlib
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup

payload = {
    'username': 'mrdooz',
    'password': getpass.getpass()
}

from pwn import *


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def get_message(html):
    ss = '----- BEGIN MESSAGE -----'
    ee = '----- END MESSAGE -----'
    s = html.index(ss) + len(ss)
    e = html.index(ee)
    return html[s:e].strip()


def challenge_13():
    with requests.Session() as s:
        p = s.post('http://ringzer0team.com/login', data=payload)
        r = s.get('http://ringzer0team.com/challenges/13')
        msg = get_message(strip_tags(r.text))
        sha = hashlib.sha512()
        sha.update(msg)
        digest = sha.hexdigest()

        url = 'http://ringzer0team.com/challenges/13/%s' % digest
        p = s.get(url)
        soup = BeautifulSoup(p.text, 'html.parser')
        print soup.find_all(class_='challenge-wrapper')


def challenge_14():
    with requests.Session() as s:
        p = s.post('http://ringzer0team.com/login', data=payload)
        r = s.get('http://ringzer0team.com/challenges/14')
        msg = get_message(strip_tags(r.text))
        sha = hashlib.sha512()
        sha.update(msg)
        digest = sha.hexdigest()

        url = 'http://ringzer0team.com/challenges/14/%s' % digest
        p = s.get(url)
        soup = BeautifulSoup(p.text, 'html.parser')
        print soup.find_all(class_='challenge-wrapper')


challenge_14()