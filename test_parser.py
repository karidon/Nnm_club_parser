# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'karidon'
__email__ = 'Genek_x@mail.ru'
__date__ = '2016-05-05'

import requests
from bs4 import BeautifulSoup

s = requests.Session()
BASE_URL = 'http://nnmclub.to/forum'


def get_html(session, url):
	request = session.get(url)
	return request.text

def read_file(filename):
	with open(filename, 'r') as input_file:
		text = input_file.read()
	return text


def parser_link(filename):
	text = read_file(filename)

	soup = BeautifulSoup(text, 'html.parser')
	table = soup.find('table', {'class':'forumline tablesorter'})

	tr = table.find_all('tr', {'class': ['prow1', 'prow2']})

	result = []
	for item in tr:
		link = BASE_URL + item.find('td', {'class': 'genmed'}).find('a').get('href')

		result.append(link)

	return result

# TODO 1: пройтись по каждой ссылке, и сохранить в файл
# TODO 2: распарсить

def parser_container_films(text):
	# Засчитываем по ссылке

	# test read file
	text = read_file(text)
	#
	#
	soup = BeautifulSoup(text, 'html.parser')

	span = soup.find('span', {'class': 'postbody'})

	for item in span:
		print(item)




if __name__ == '__main__':
	# url = 'http://nnmclub.to/forum/viewtopic.php?t=1013847'
	#url = 'http://nnmclub.to/forum/tracker.php?f=218'

	url = 'http://nnmclub.to/forum/viewtopic.php?t=1014442'
	data = get_html(s, url)

	with open('proba.html', 'w') as f:
		f.write(data)

	#parser_link('proba.html')

	parser_container_films('proba.html')

