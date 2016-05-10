# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'karidon'
__email__ = 'Genek_x@mail.ru'
__date__ = '2016-05-10'

import requests

from bs4 import BeautifulSoup
from time import process_time, sleep

import template

s = requests.Session()

BASE_URL = 'http://nnmclub.to/forum/'


def load_user_data(session, url):
	'''
	Считаем url. Возращает text.
	:param session: текущая сессия
	:return: str
	'''
	request = session.get(url)
	return request.text


def contain_movies_data(text):
	'''
	Обрабатывает text - разбирая на html код
	:param text: str
	:return: str
	'''
	soup = BeautifulSoup(text, 'html.parser')
	film_list = soup.find('table', {'class': 'forumline tablesorter'})
	return film_list is not None


def contain_img_data(text):
	'''
	Parsing html file and return url img
	:param text:
	:return: str
	'''
	soup = BeautifulSoup(text, 'html.parser')
	img = soup.find('var', {'class': 'postImg postImgAligned img-right'})
	try:
		return img['title']
	except TypeError:
		pass


def read_file(filename):
	'''
	Засчитываем фаил и возращаем ext
	:param filename: str
	:return: str
	'''
	with open(filename, 'r') as input_file:
		text = input_file.read()
	return text


def parse_user_datafile_bs(filename):
	'''
	Возвращает парсер файла в виде листа
	:param filename: str
	:return: list
	'''
	start = process_time()  # начальное время работы функции

	result = []
	text = read_file(filename)

	soup = BeautifulSoup(text, 'html.parser')
	film_list = soup.find('table', {'class': 'forumline tablesorter'})

	items = film_list.find_all('tr', ['prow1', 'prow2'])

	for item in items:
		# название категории
		category = item.find('a', {'class': 'gen'}).text
		# название фильма
		topic = item.find('td', {'class': 'genmed'}).find('a').text
		# ссылка
		link = BASE_URL + item.find('td', {'class': 'genmed'}).find('a').get('href')
		# размер
		size = ' '.join(item.find('td', {'class': 'gensmall'}).text.split()[1:])
		# скачано
		seeders = item.find('td', {'class': 'seedmed'}).text
		# обложка
		img = contain_img_data(load_user_data(s,
		                                      BASE_URL + item.find('td', {'class': 'genmed'}).find('a').get('href')))

		result.append({'category': category,
		               'topic': topic,
		               'link': link,
		               'size': size,
		               'seeders': seeders,
		               'img': img
		               })

		sleep(2.0)  # задержка на 1 сек

		# Проверка по времени
		finish = process_time()
		print(finish - start)

	return result


if __name__ == '__main__':
	url = 'http://nnmclub.to/forum/tracker.php?f=218'
	data = load_user_data(s, url)
	if contain_movies_data(data):
		with open('test.html', 'w') as output_file:
			output_file.write(data)

	text_list = parse_user_datafile_bs('test.html')
	template.save_html(text_list, 'index.html')

# contain_img_data(load_user_data(s, 'http://nnmclub.to/forum/viewtopic.php?t=1012261'))
