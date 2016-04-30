# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
Скрипт разбирает сайт Nnm-club выбмрая 50 зарубежные и наши фильмы.
Выводит в html и excel фаил.
"""
# TODO 1: Переделать по возможность в ООП
# TODO 2: Сделать status bar

__author__ = 'karidon'
__email__ = 'Genek_x@mail.ru'
__date__ = '2016-04-29'

import urllib.request
from bs4 import BeautifulSoup
from xlwt import Workbook, easyxf

FOREIGN_URL = 'http://nnmclub.to/forum/tracker.php?f=218'
OUR_URL = 'http://nnmclub.to/forum/tracker.php?f=270'

BASE_URL = 'http://nnmclub.to/forum/'


def get_html(url):
	'''
	Возращает содержимое сайта
	:param str
	:return: http.client.HTTPResponse
	'''
	response = urllib.request.urlopen(url)
	return response.read()


def parse_img(html):
	soup = BeautifulSoup(html, 'html.parser')
	img = soup.find('var', class_='postImg postImgAligned img-right')

	return img['title']


def parse(html):
	'''
	Возварщает список всех проектов на одной странице
	:param html: str
	:return: list
	'''
	soup = BeautifulSoup(html, 'html.parser')
	table = soup.find('table', class_='forumline tablesorter')

	project = []

	for row in table.find_all('tr', class_='prow1'):
		cols = row.find_all('td')
		project.append({'topic': cols[2].a.text,
						'link': BASE_URL + cols[2].a.get('href'),
						'size': ' '.join(cols[5].text.split()[1:]),  # собирает 2.18 GB
						'seeders': int(cols[6].text),
						'img': parse_img(get_html(BASE_URL + cols[2].a.get('href')))
						})

	for row in table.find_all('tr', class_='prow2'):
		cols = row.find_all('td')
		project.append({'topic': cols[2].a.text,
						'link': BASE_URL + cols[2].a.get('href'),
						'size': ' '.join(cols[5].text.split()[1:]),  # собирает 2.18 GB
						'seeders': int(cols[6].text),
						'img': parse_img(get_html(BASE_URL + cols[2].a.get('href')))
						})

	return project


def save_excel(projects, path):
	'''
	Сохраняет нащ список в файл xls
	:param projects: list
	:param path: str
	:return: file
	'''
	wb = Workbook()
	ws = wb.add_sheet('Sheet 1')

	style1 = easyxf('pattern: pattern solid, fore_colour yellow;' + 'font: bold True, height 250')
	ws.col(0).width = 20000
	ws.col(1).width = 11000
	ws.col(2).width = 3000
	ws.col(3).width = 4000
	ws.col(4).width = 4000

	headers = ('Название', 'Ссыдка', 'Размер', 'Раздатчики', 'Картинка')

	for j, header in enumerate(headers):
		ws.write(0, j, header, style1)

	for i, project in enumerate(projects, 1):
		ws.row(i).write(0, project['topic'])
		ws.row(i).write(1, project['link'])
		ws.row(i).write(2, project['size'])
		ws.row(i).write(3, project['seeders'])
		ws.row(i).write(4, project['img'])

	wb.save(path)


def save_html(category, projects, path, mode='w'):
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
            <h1 align='center'>{name}</h1>
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


def main():
	foreign_films = 'Зарубежные фильмы'
	topic_count = parse(get_html(FOREIGN_URL))
	print('Результатов поиска: %d (max: 50)' % len(topic_count))

	save_html(foreign_films, topic_count, 'project.html')

	our_films = 'Наши фильмы'
	topic_count = parse(get_html(OUR_URL))
	print('Результатов поиска: %d (max: 50)' % len(topic_count))

	save_html(our_films, topic_count, 'project.html', mode='a')  # до писали фаил


if __name__ == '__main__':
	try:
		main()
	except urllib.error.URLError:
		print('Sorry 502')
