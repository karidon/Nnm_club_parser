# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'karidon'
__email__ = 'Genek_x@mail.ru'
__date__ = '2016-04-30'

import main_new

import proxy

	# TODO 3: Test


def main(url, mode='w'):
	data = main_new.load_user_data(main_new.s, url)
	if main_new.contain_movies_data(data):
		with open('test.html', 'w') as output_file:
			output_file.write(data)

	text_list = main_new.parse_user_datafile_bs('test.html')
	main_new.save_html(text_list, 'index.html', mode)
	print('Результатов поиска: %d (max: 50)' % len(text_list))

if __name__ == '__main__':
	foreign_films = 'http://nnmclub.to/forum/tracker.php?f=218'
	main(foreign_films)

	our_films = 'http://nnmclub.to/forum/tracker.php?f=270'
	main(our_films, mode='a')
