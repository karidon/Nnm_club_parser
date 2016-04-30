# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'karidon'
__email__ = 'Genek_x@mail.ru'
__date__ = '2016-04-30'

import requests

from bs4 import BeautifulSoup

BASE_URL = 'http://www.ip-adress.com/proxy_list/'

def get_html(url):
	'''
	Возвращает html страницу
	:param url: str url
	:return:
	'''
	r = requests.get(BASE_URL)
	return r.content

def parse(html):
	'''
	Возвращает список ip proxy
	:param html: str
	:return: list
	'''
	soup = BeautifulSoup(html, 'html.parser')
	table = soup.find('table', class_='proxylist')

	proxy_list = []
	for row in table.find_all('tr', class_='odd'):
		cols = row.find_all('td')
		proxy_list.append(cols[0].text)
	for row in table.find_all('tr', class_='even'):
		cols = row.find_all('td')
		proxy_list.append(cols[0].text)

	return proxy_list

def get_proxy(proxy_list):
	'''
	Проверяет proxy
	:param proxy_list: list
	:return: url
	'''
	for proxy in proxy_list:
		url = 'http://' + proxy
		try:
			r = requests.get('https://www.ya.ru/', proxies={'http': url})
			if r.status_code == 200:
				return url
		except requests.exceptions.ConnectionError:
			continue

if __name__ == '__main__':
	proxy = get_proxy(parse(get_html(BASE_URL)))
	print(proxy)
	r = requests.get('http://speed-tester.info/check_ip.php', proxies={'http': proxy})
	print(r.content)