# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'karidon'
__email__ = 'Genek_x@mail.ru'
__date__ = '2016-05-10'

import parser_script
import template


def main(url, mode='w'):
	'''
	Return html file
	:param url: str
	:param mode: режим записи (чтения) str
	:return: file
	'''
	data = parser_script.load_user_data(parser_script.s, url)
	if parser_script.contain_movies_data(data):
		with open('tmp.html', 'w') as output_file:
			output_file.write(data)

	text_list = parser_script.parse_user_datafile_bs('test.html')

	template.save_html(text_list, 'index.html', mode)
	print('Результатов поиска: %d (max: 50)' % len(text_list))


if __name__ == '__main__':
	foreign_films = 'http://nnmclub.to/forum/tracker.php?f=218'
	main(foreign_films)

	our_films = 'http://nnmclub.to/forum/tracker.php?f=270'
	main(our_films, mode='a')
