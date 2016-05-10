# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'karidon'
__email__ = 'Genek_x@mail.ru'
__date__ = '2016-05-10'


def save_html(projects, path, mode='w'):
	'''
	Сохраняет нащ список в файл HML.
	:category: str (category films)
	:param projects: list
	:param path: str
	:mode: str (режим записи)
	:return: file
	'''

	# TODO: добавить оглавнение

	html_template_head = """
		<!DOCTYPE HTML>
		<html>
			<head>
				<meta charset="utf-8">
				<title>New Films</title>
			</head>
		<body>
			<h1 align='center'>{category}</h1>
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
	my_file = open(path, mode, encoding='utf-8')

	my_file.write(html_template_head.format(category=projects[0]['category']))

	for num, project in enumerate(projects, 1):
		my_file.write(html_template_table.format(number=num, topic=project['topic'], link=project['link'],
		                                         size=project['size'], seeders=project['seeders'],
		                                         img=project['img']))
	my_file.write(html_template_footer)

	my_file.close()


if __name__ == '__main__':
	projects = [{'category': 'Зарубежный фильм', 'topic': 'Детпул', 'link': 'https://yandex.ru/', 'size': '2.34 GB',
	             'seeders': '2345',
	             'img': 'http://assets.nnm-club.ws/forum/image.php?link=http://s017.radikal.ru/i420/1601/56/affa088a60aa.jpg'},
	            {'category': 'Зарубежный фильм', 'topic': 'Детпул', 'link': 'https://yandex.ru/', 'size': '2.34 GB',
	             'seeders': '2345',
	             'img': 'http://assets.nnm-club.ws/forum/image.php?link=http://s017.radikal.ru/i420/1601/56/affa088a60aa.jpg'}
	            ]
	save_html(projects, 'test.html')

	projects = [{'category': 'Наши фильмы', 'topic': 'Детпул', 'link': 'https://yandex.ru/', 'size': '2.34 GB',
	             'seeders': '2345',
	             'img': 'http://assets.nnm-club.ws/forum/image.php?link=http://s017.radikal.ru/i420/1601/56/affa088a60aa.jpg'},
	            {'category': 'Наши фильмыы', 'topic': 'Детпул', 'link': 'https://yandex.ru/', 'size': '2.34 GB',
	             'seeders': '2345',
	             'img': 'http://assets.nnm-club.ws/forum/image.php?link=http://s017.radikal.ru/i420/1601/56/affa088a60aa.jpg'}
	            ]
	save_html(projects, 'test.html', 'a')
