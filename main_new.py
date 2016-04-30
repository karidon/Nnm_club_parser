# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'karidon'
__email__ = 'Genek_x@mail.ru'
__date__ = '2016-04-30'

import requests
from bs4 import BeautifulSoup

s = requests.Session()

BASE_URL = 'http://nnmclub.to/forum/'


def load_user_data(session, url):
	'''
	Считаем url. Возращает text.
	:param session: текущая сессия
	:return: str
	'''
	#	url = 'http://nnmclub.to/forum/tracker.php?f=218'
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
	soup = BeautifulSoup(text, 'html.parser')
	img = soup.find('var', {'class': 'postImg postImgAligned img-right'})

	return img['title']


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
	result = []
	text = read_file(filename)

	soup = BeautifulSoup(text, 'html.parser')
	film_list = soup.find('table', {'class': 'forumline tablesorter'})

	items = film_list.find_all('tr', ['prow1', 'prow2'])
	# print(len(items), items)

	for item in items:
		# название фильма
		topic = item.find('td', {'class': 'genmed'}).find('a').text
		# ссылка
		link = BASE_URL + item.find('td', {'class': 'genmed'}).find('a').get('href')
		# размер
		size = ' '.join(item.find('td', {'class': 'gensmall'}).text.split()[1:])
		# скаяано
		seeders = item.find('td', {'class': 'seedmed'}).text
		# обложка
		img = contain_img_data(load_user_data(s,
											  BASE_URL + item.find('td', {'class': 'genmed'}).find('a').get('href')))

		result.append({'topic': topic,
					   'link': link,
					   'size': size,
					   'seeders': seeders,
					   'img': img
					   })

	return result


def save_html(projects, path, mode='w', category=None):
	'''
	Сохраняет нащ список в файл HML.
	:category: str
	:param projects: list
	:param path: str
	:mode: str (режим записи)
	:return: file
	'''
	html_template_head = """
        <!DOCTYPE HTML>
        <html>
            <head>
                <meta charset="utf-8">
                <title>New Films</title>
            </head>
        <body>
            <h1 name={name} align='center'>{name}</h1>
            <table border='1' align='center'>
            <tr>
                <th>№</td>
                <th>Название</td>
                <th>Размер</td>
                <th>Раздатчики</td>
                <th>Обложка</td>
            </tr>
    """

	html_template_table = """
    <tr>
        <td align='center'>{number}</td>
        <td align='center'><a href={link}>{topic}</a></td>
        <td align='center'>{size}</td>
        <td align='center'>{seeders}</td>
        <td align='center'><img src={img} width="189" height="255"></td>
    </tr>
    """

	html_template_footer = """
            </table>
        </body>
        </html>
    """
	# with open(path, 'w', encoding='utf-8') as my_file:
	my_file = open(path, mode, encoding='utf-8')

	my_file.write(html_template_head.format(name=category))

	for num, project in enumerate(projects, 1):
		my_file.write(html_template_table.format(number=num, topic=project['topic'], link=project['link'],
												 size=project['size'], seeders=project['seeders'],
												 img=project['img']))
	my_file.write(html_template_footer)

	my_file.close()


if __name__ == '__main__':
	url = 'http://nnmclub.to/forum/tracker.php?f=218'
	data = load_user_data(s, url)
	if contain_movies_data(data):
		with open('test.html', 'w') as output_file:
			output_file.write(data)

	text_list = parse_user_datafile_bs('test.html')
	save_html(text_list, 'index.html')

	# contain_img_data(load_user_data(s, 'http://nnmclub.to/forum/viewtopic.php?t=1012261'))
