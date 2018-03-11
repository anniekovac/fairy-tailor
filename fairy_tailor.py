from pprint import pprint as pp
from fairy_parser import parser
import random


class Word(object):
	def __init__(self, word):
		self.word = word
		self.next_word_list = []
		self.frequency = None


def separate_words(text):
	"""
	Function that receives text as raw and removes special characters
	etc from it.
	:param text: str 
	:return: list of strings [str, str, str ...]
	"""
	# splitting fairy tale into words
	fairy_list = text.split(" ")

	# removing ",", ";", ".", "\n" from words
	new_fairy_list = []
	for word in fairy_list:
		if "\n" in word:
			new_fairy_list.extend(["".join(letter for letter in item if letter.isalnum()) for item in word.split("\n")])
		else:
			new_fairy_list.append("".join(letter for letter in word if letter.isalnum()))

	# removing empty strings
	new_fairy_list = [item for item in new_fairy_list if item]
	return new_fairy_list


def print_words(word_list):
	"""
	Printing words and their next words, and frequencies.
	:param word_list: list of Word object instances - [Word(), Word(), ...]
	:return: None
	"""
	for word in word_list:
		print(word.word)
		for next_word in word.next_word_list:
			print("    ", next_word.word, next_word.frequency)


def save_words_to_txt(word_list, filename="word_list_output.txt"):
	with open(filename, "w") as file:
		for word in word_list:
			file.write("\n{}".format(word.word))
			for next_word in word.next_word_list:
				file.write("\n    {}, {}".format(next_word.word, next_word.frequency))


def generate_text(word_list):
	"""
	Function for generating text from word_list.
	:param word_list: list of Word object instances - [Word(), Word(), ...]
	:return: 
	"""
	text = ""
	random_word = random.choice(word_list)  # choose one random word (for start)
	text = text.join(random_word.word + " ")  # append this random word to text
	while len(text) < 100:  # while text has smaller length than 100
		random_word = random_word.next_word_list[0]  # another word is always first from the next_word_list
		#print(random_word.word)
		append_word = random_word.word + " "
		text = text + append_word
		print(text)

	return text


def connect_next_words(word_list):
	"""
	Connecting word from next_lists to their next_word lists.
	:param word_list:  list of Word object instances - [Word(), Word(), ...]
	:return: dict
	"""
	next_words_dict = dict()
	for word in word_list:
		next_words_dict[word.word] = word.next_word_list
	for word in word_list:
		for next_word in word.next_word_list:
			try:
				next_word.next_word_list = next_words_dict[next_word.word]
			except KeyError:
				pass
	# return next_words_dict


if __name__ == '__main__':
	# dictionary of Grimm fairy tales:
	# keys: titles, values: string of fairy tale
	fairy_dict = parser()
	fairy_tale = fairy_dict['97 The Water of Life']
	wise_folks = fairy_dict['104 Wise Folks (Die klugen Leute)']
	bearskin = fairy_dict['101 Bearskin (Der Bärenhäuter)']

	fairy_list = separate_words(fairy_tale)

	word_list = []
	for idx, word in enumerate(fairy_list):  # for each word in list
		try:  # try to get
			next_word = fairy_list[idx+1]  # next word
		except IndexError:  # if you are out of words
			continue  # continue with loop (finish)

		if word not in [item.word for item in word_list]:  # if we don't already have instance of this word
			word_instance = Word(word)  # create instance of this word
			word_list.append(word_instance)
		else:  # if there is already instance of this word in list
			word_instance = [item for item in word_list if item.word == word][0]  # THIS HAS TO BE ONLY ONE

		if next_word not in [item.word for item in word_instance.next_word_list]:  # if we don't already have instance of next word
			next_word_instance = Word(next_word)
			next_word_instance.frequency = 1
			word_instance.next_word_list.append(next_word_instance)
		else:  # if there is already instance of next word
			next_word_instance = [item for item in word_instance.next_word_list if item.word == next_word][0]  # THIS HAS TO BE ONLY ONE
			next_word_instance.frequency += 1

	for word in word_list:
		word.next_word_list.sort(key=lambda x: x.frequency, reverse=True)

	save_words_to_txt(word_list)
	# print_words(word_list)
	# print(generate_text(word_list))
	connect_next_words(word_list)
	generate_text(word_list)