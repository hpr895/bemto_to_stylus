import sublime
import sublime_plugin

import ctypes
import re
from collections import Counter

# from pprint import pprint


class bemto_to_stylusCommand(sublime_plugin.TextCommand):
	def run(self, edit):


		# Часть 1

		# Берём текст из буфера обмера
		def getClipboardText():
			CF_UNICODETEXT = 13
			d = ctypes.windll
			d.user32.OpenClipboard(0)
			handle = d.user32.GetClipboardData(CF_UNICODETEXT)
			data = ctypes.c_wchar_p(handle).value
			d.user32.CloseClipboard()
			return data


		# Удаляем строки без bemto
		def cleanBemTo(array):
			new_array = []
			pattern = re.compile(r'\t*\+b.|\+b.|\t*\+e.|\+e.')
			for i in range(len(array)):
				if re.match(pattern, array[i]):
					new_array.append(array[i])
			return new_array


		# Удаляем всё между скобок
		def removeBrackets(array):
			new_array = []
			pattern = re.compile(r"\((.*)\)")
			for i in range(len(array)):
				s = re.sub(pattern, '', array[i])
				new_array.append(s)
			return new_array


		# Удаляем всё после пробела, "=", "& ", "# "
		def removeJadeContent(array):
			new_array = []
			pattern = re.compile(r" \S*|= \S*|&\S*|#\S*")
			for i in range(len(array)):
				s = re.sub(pattern, '', array[i])
				new_array.append(s)
			return new_array


		# Очищаем классы от тегов
		def cleanClassedTags(array):
			new_array = []
			pattern = re.compile(r"([A-Z0-9]+\.)*")
			for i in range(len(array)):
				s = re.sub(pattern, '', array[i])
				new_array.append(s)
			return new_array


		# Если в какой-то строке нет символа '\r', добавляем его
		def typeReturnToLastArrayItem(array):
			new_array = []
			for i in range(len(array)):
				if '\r' in array[i]:
					s = array[i]
					new_array.append(s)
				else:
					s = array[i] + '\r'
					new_array.append(s)
			return new_array






		# Часть 2

		# Посчитать количество +b. в массиве
		# И пересортировать массив:
		# Поднять элементы к своим блокам
		def sortingElemToBlock(array):
			b_count = 0
			for line in range(len(array)):
				if '+b.' in array[line]:
					b_count += 1
			if b_count > 0:
				new_array = []
				e_cycle = 1
				while e_cycle <= b_count:
					iter_block_count = 0
					left_edge = 0
					right_edge = 9999999
					has_block = 0
					for line in range(len(array)):
						this_line_tabs_count = array[line].count('\t')
						# Если находит БЛОК
						b_pattern = re.compile(r'\t*\+b.|\+b.')
						if re.match(b_pattern, array[line]):
							iter_block_count += 1
							if iter_block_count == e_cycle:
								new_array.append(array[line])
								left_edge = this_line_tabs_count
								has_block = 1
							if iter_block_count != e_cycle:
								if has_block == 1:
									if this_line_tabs_count < right_edge:
										right_edge = this_line_tabs_count
								if this_line_tabs_count <= left_edge:
									has_block = 0
						# Если находит ЭЛЕМЕНТ
						e_pattern = re.compile(r'\t*\+e.|\+e.')
						if re.match(e_pattern, array[line]):
							if has_block == 1:
								if this_line_tabs_count <= left_edge:
									break
								if this_line_tabs_count > left_edge and this_line_tabs_count <= right_edge:
									new_array.append(array[line])
									right_edge = 9999999
					e_cycle += 1
				return new_array






		# Часть 3

		# Выравнивает все табы и ставит пустые строки между массивами.
		def alignJadeLines(array):
			new_array = []
			pattern_b = re.compile(r"\t*\+b\.")
			pattern_e = re.compile(r"\t*\+e\.")
			block_count = 0
			for line in range(len(array)):
				if re.match(pattern_b, array[line]):
					s = re.sub(pattern_b, '+b.', array[line])
					new_array.append(s)
					block_count = 1
				if re.match(pattern_e, array[line]):
					s = re.sub(pattern_e, '\t+e.', array[line])
					new_array.append(s)
			return new_array


		# Удалить всё после точки
		def removeAllAfterDot(array):
			new_array = []
			pattern_after_dot = re.compile(r"\..*")
			for line in range(len(array)):
				if '+b.' in array[line]:
					str_new = re.sub('\+b\.', '+b=', array[line])
					if re.search(pattern_after_dot, array[line]):
						str_new = re.sub(pattern_after_dot, '\r', str_new)
						str_new = re.sub('\+b\=', '+b.', str_new)
				if '+e.' in array[line]:
					str_new = re.sub('\+e\.', '+e=', array[line])
					if re.search(pattern_after_dot, array[line]):
						str_new = re.sub(pattern_after_dot, '\r', str_new)
						str_new = re.sub('\+e\=', '+e.', str_new)
				new_array.append(str_new)
			return new_array


		# Подогнать одинаковые блоки
		def joinSameBlocks(array):
			b_count = 0
			for line in range(len(array)):
				if '+b.' in array[line]:
					b_count += 1
			if b_count > 0:
				new_array = []
				join_cycle = 1
				regex_block_name = ''
				while join_cycle <= b_count:
					iter_block_count = 0
					join_active = 0
					search_is_work = 0
					# Находит блок, равный итерации
					for line in range(len(array)):
						if '+b.' in array[line]:
							iter_block_count += 1
							join_active = 0
							if iter_block_count == join_cycle:
								new_array.append('\r')
								# Записывает имя первого блока в поиск
								regex_block_name = array[line]
								regex_block_mod = re.sub('\r', '_', regex_block_name)
								if '_' in array[line]:
									block_without_mod = re.sub('_.*', '', array[line])
									new_array.append(block_without_mod)
								new_array.append(array[line])
								search_is_work = 1
								join_active = 1
							if iter_block_count != join_cycle:
								if search_is_work == 1:
									if regex_block_name in array[line] or regex_block_mod in array[line]:
										new_array.append(array[line])
										join_active = 1
										array[line] = 'space'
						# Присваиваем элементы к блоку
						if '+e.' in array[line]:
							if join_active == 1:
								new_array.append(array[line])
								array[line] = 'space'
					join_cycle += 1
				new_array.append('\r')
				return new_array


		# Подогнать модификаторы
		def joinMods(array):
			b_count = 0
			new_array = []
			for line in range(len(array)):
				if '+b.' in array[line]:
					b_count += 1
			if b_count > 0:
				join_cycle = 1
				regex_block_name = ''
				while join_cycle <= b_count:
					iter_block_count = 0
					join_active = 0
					elements_array = []
					elem_count = 0
					# Находит блок, равный итерации
					for line in range(len(array)):
						if '+b.' in array[line]:
							iter_block_count += 1
							if iter_block_count == join_cycle:
								new_array.append('\r')
								new_array.append(array[line])
								join_active = 1
								active_line = line
						if '+b.' in array[line]:
							if iter_block_count != join_cycle:
								if join_active == 1:
									new_array.append(array[line])
									array[line] = 'space_block'
						if '+e.' in array[line]:
							if join_active == 1:
								elem_count += 1
								elements_array.append(array[line])
								array[line] = 'space_element'
						if re.match('\r', array[line]):
							if join_active == 1:
								join_active = 0
								if elem_count > 0:
									element_join_cycle = 1
									regex_elem_name = ''
									while element_join_cycle <= elem_count:
										iter_element_count = 0
										for line in range(len(elements_array)):
											if '+e.' in elements_array[line]:
												iter_element_count += 1
												if iter_element_count == element_join_cycle:
													elements_join_active = 1
													element_active_line = line
													regex_elem_name = elements_array[line]
													regex_elem_mod = re.sub('\r', '_', regex_elem_name)
													if '_' in elements_array[line]:
														element_without_mod = re.sub('_.*', '', elements_array[line])
														new_array.append(element_without_mod)
													new_array.append(elements_array[line])
											if '+e.' in elements_array[line]:
												if iter_element_count != element_join_cycle:
													if elements_join_active == 1:
														if regex_elem_mod in elements_array[line]:
															new_array.append(elements_array[line])
															elements_array[line] = 'elem_space'
										element_join_cycle += 1
								break
					join_cycle += 1
			return new_array


		# Оставляем только уникальные строки.
		def remainUnique(array):
			seen = []
			new_array = []
			for line in array:
				if re.match('\r', line):
					new_array.append(line)
					seen = []
				else:
					if line in seen:
						continue
					seen.append(line)
					new_array.append(line)
			return new_array






		# Часть 4

		# Временно подготавливаем модификаторы
		def convertMods(array):
			new_array = []
			pattern_before_mod = re.compile(r".*_")
			for line in range(len(array)):
				str_new = array[line]
				if '+b.' in array[line]:
					if re.search(pattern_before_mod, array[line]):
						str_new = re.sub(pattern_before_mod, '\t+bm.', array[line])
				if '+e.' in array[line]:
					if re.search(pattern_before_mod, array[line]):
						str_new = re.sub(pattern_before_mod, '\t\t+em.', array[line])
				new_array.append(str_new)
			return new_array


		# Конвертируем теги
		def convertTags(array):
			new_array = []
			pattern_tag = re.compile(r".*\.[A-Z]")
			for line in range(len(array)):
				str_new = array[line]
				if re.match(pattern_tag, array[line]):
					if '+b.' in array[line]:
						str_new = re.sub('\+b.', '', array[line])
						str_new = str_new.lower()
					if '+e.' in array[line]:
						str_new = re.sub('\+e.', '& ', array[line])
						str_new = str_new.lower()
				new_array.append(str_new)
			return new_array


		# Конвертируем всё в Stylus разметку
		def convertToStylus(array):
			new_array = []
			for line in array:
				str_new = line
				if '+b.' in line:
					str_new = re.sub('\+b.', '.', line)
					new_array.append(str_new)
					new_array.append('\t//')
				if '+e.' in line:
					str_new = re.sub('\+e.', '&__', line)
					new_array.append(str_new)
					new_array.append('\t\t//')
				if '+bm.' in line:
					str_new = re.sub('\+bm.', '&_', line)
					new_array.append(str_new)
					new_array.append('\t\t//')
				if '+em.' in line:
					str_new = re.sub('\+em.', '&_', line)
					new_array.append(str_new)
					new_array.append('\t\t\t//')
				if re.match('\r', line):
					new_array.append('\r')
			return new_array


		# Автоматически добавляем стили (работает только для элементов на 2 табах)
		def autoInsert(array):
			dictArray = {
				'link' :  {'value': '+link()\n\t\t\t\n\t\t&:hover\n\t\t\t'},
				'left' :  {'value': 'dib(50%)\n\t\t'},
				'right' : {'value': 'dib(50%, 1)\n\t\t'},
				'title' : {'value': 'margin 0\n\t\tfont-size 20px\n\t\tfont-weight normal'},
				'row' :   {'value': 'cf()'},
				'photo' : {'value': 'fit(200px)'},
				'mask' : {'value': 'link-mask()'},
			}
			new_array = []
			for line in array:
				new_array.append(line)
				# Достаём слово
				reg_word = re.compile(r".+&__|\.|\r")
				word = re.sub(reg_word, '', line)
				# Добавляем миксин, если слово есть в словаре
				if re.match('\w', word):
					if word in dictArray:
						mixin_line = '\t\t' + dictArray[word]['value']
						new_array.append(mixin_line)
			return new_array


		# Скрываем символ возврата каретки, и удаляем лишнюю первую строку
		def hideCaretReturn(array):
			new_array = []
			first_is_removed = 0
			if re.match('\r', array[0]):
				del array[0]
			for line in array:
				str_new = line
				str_new = re.sub('\r', '', line)
				new_array.append(str_new)
			return new_array


		# Заключение

		# Вставляем в Sublime Text результат
		def SublimeInsertText(array):
			for line in array:
				pos = self.view.sel()[0].begin()
				self.view.insert(edit, pos, line + '\n')
				# pprint(line)


		# Финальное объединение всего плагина
		def makeFinal():
			fin = getClipboardText()
			fin = fin.split('\n')
			fin = cleanBemTo(fin)
			if fin:
				fin = removeBrackets(fin)
				fin = removeJadeContent(fin)
				fin = cleanClassedTags(fin)
				fin = typeReturnToLastArrayItem(fin)
				fin = sortingElemToBlock(fin)
				fin = alignJadeLines(fin)
				fin = removeAllAfterDot(fin)
				fin = joinSameBlocks(fin)
				fin = joinMods(fin)
				fin = remainUnique(fin)
				fin = convertMods(fin)
				fin = convertTags(fin)

				fin = convertToStylus(fin)

				fin = autoInsert(fin)

				fin = hideCaretReturn(fin)
				sublime.status_message('Bemto to Jade: Conversion was successful')
			else:
				sublime.status_message('Bemto to Jade: Error - array has no length')
			SublimeInsertText(fin)
		makeFinal()


