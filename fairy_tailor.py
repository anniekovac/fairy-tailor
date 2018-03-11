from pprint import pprint as pp
from fairy_parser import parser
import random, pickle, os


class Word(object):
	"""
	Object for storing word. It has
	"word" property for actual word string, 
	"next_word_list" property for saving list
	of all possible words after this word, "frequency"
	property for storing how many times this word shows up
	right after some other word.
	This "frequency" property is to be used only when Word()
	instance is in next_word_list of some other word.
	"""
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
		if "." in word:
			new_fairy_list.append("".join(letter for letter in word if letter.isalnum()))
			new_fairy_list.append(".")

		elif "\n" in word:
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
	"""
	for word in word_list:
		print(word.word)
		for next_word in word.next_word_list:
			print("    ", next_word.word, next_word.frequency)


def save_words_to_txt(word_list, filename="word_list_output.txt"):
	"""
	Function for saving words, next words and their frequencies to
	txt file. Default name of the file is "word_list_output.txt".
	:param word_list: list of Word object instances - [Word(), Word(), ...]
	:param filename: str (name of the output file where you want to save the words)
	"""
	with open(filename, "w") as file:
		for word in word_list:
			file.write("\n{}".format(word.word))
			for next_word in word.next_word_list:
				file.write("\n    {}, {}".format(next_word.word, next_word.frequency))


def select_next_word(word, select_first=False):
	"""
	Function created for selecting next word.
	For now, only selecting first possible word (with highest
	frequency number) is implemented.
	:param word: Word() instance
	:param select_first: boolean (True if you want to select first possible word)
	:return: Word() instance
	"""
	if select_first:
		return word.next_word_list[0]
	else:
		choices = {word: word.frequency for word in word.next_word_list}
		max = sum(choices.values())
		pick = random.uniform(0, max)
		current = 0
		for key, value in choices.items():
			current += value
			if current > pick:
				return key


def generate_text(word_list):
	"""
	Function for generating text from word_list.
	:param word_list: list of Word object instances - [Word(), Word(), ...]
	:return: string (generated text) 
	"""
	text = ""
	random_word = random.choice(word_list)  # choose one random word (for start)
	text = text.join(random_word.word + " ")  # append this random word to text
	while len(text) < 120:  # while text has smaller length than 100
		random_word = select_next_word(random_word)
		append_word = random_word.word + " "
		text = text + append_word
		print(text)
	return text


def connect_next_words(word_list):
	"""
	Connecting word from next_lists to their next_word lists.
	:param word_list: list of Word object instances - [Word(), Word(), ...]
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


def create_word_list(separate_words):
	"""
	From list of strings this function creates list of Word() instances, 
	appends next words to initial words and calculates their frequency.
	For every word, next_word_list is in the end sorted by frequency (from highest to lowest).
	:param separate_words: list of strings
	:return: list of Word object instances - [Word(), Word(), ...]
	"""
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
	return word_list


def select_fairy_tales(select_all=False):
	"""
	Function for selecting fairy tales from dictionary
	returned by parser() function.
	:return: 
	"""
	fairy_dict = parser()
	fairy_list = []
	# for key in fairy_dict.keys():
	# 	print(key)
	fairy_tales = []
	if select_all:
		for key in fairy_dict.keys():
			fairy_tales.append(key)
	else:
		fairy_tales = ['97 The Water of Life', '104 Wise Folks (Die klugen Leute)',
					   '101 Bearskin (Der Bärenhäuter)', '12 Rapunzel', '21 Cinderella',
					   '22 The Riddle', '23 The Mouse, the Bird, and the Sausage',
					   '24 Mother Holle', '25 The Seven Ravens', '126 Ferdinand the Faithful',
					   '128 The Lazy Spinner', '132 The Fox and the Horse', '137 The Three Black Princesses',
					   '184 The Nail', '185 The Poor Boy in the Grave', '186 The True Sweethearts',
					   '187 The Hare and the Hedgehog', '189 The Peasant and the Devil',
					   '190 The Crumbs on the Table', '191 The Sea-Hare', '192 The Master-Thief',
					   '200 The Golden Key', '199 The Boots of Buffalo-Leather', '198 Maid Maleen',
					   '197 The Crystal Ball', '196 Old Rinkrank', '195 The Grave-Mound', '194 The Ear of Corn',
					   '193 The Drummer', '183 The Giant and the Tailor', "182 The Little Folks' Presents",
					   "181 The Nix of the Mill-Pond", "180 Eve's Various Children", "179 The Goose-Girl at the Well",
					   "178 Master Pfriem (Master Cobbler's Awl)", "177 Death's Messengers", "176 The Duration of Life",
					   "175 The Moon"]
	for tale in fairy_tales:
		fairy_tale = fairy_dict[tale]
		fairy_list.extend(separate_words(fairy_tale))
	return fairy_list


if __name__ == '__main__':

	fairy_list = select_fairy_tales(select_all=True)

	if os.path.exists(os.path.join(os.getcwd(), "word_list.pkl")):
		with open('word_list.pkl', 'rb') as input:
			word_list = pickle.load(input)

	else:
		with open('word_list.pkl', 'wb') as output:
			word_list = create_word_list(fairy_list)
			pickle.dump(word_list, output, pickle.HIGHEST_PROTOCOL)
		save_words_to_txt(word_list)

	connect_next_words(word_list)
	# print_words(word_list)
	# print(generate_text(word_list))

	generate_text(word_list)