from pprint import pprint as pp
from fairy_parser import parser

if __name__ == '__main__':
	# dictionary of Grimm fairy tales:
	# keys: titles, values: string of fairy tale
	fairy_dict = parser()
	fairy_tale = fairy_dict['97 The Water of Life']

	# splitting fairy tale into words
	fairy_list = fairy_tale.split(" ")

	# removing ",", ";", ".", "\n" from words
	new_fairy_list = []
	for word in fairy_list:
		if "\n" in word:
			new_fairy_list.extend([item.replace(".", "").replace(",", "").replace(";", "").replace("\"", "").replace("?", "").lower() for item in word.split("\n")])
		else:
			new_fairy_list.append(word.replace(".", "").replace(",", "").replace(";", "").replace("\"", "").replace("?", "").lower())

	# removing empty strings
	new_fairy_list = [item for item in new_fairy_list if item]

	# pp(new_fairy_list)

	# word dict je rjecnik gdje su kljucevi
	# rijeci, a vrijednosti rjecnici
	# ovi rjecnici imaju kljuceve koji su takodjer rijeci
	# to su rijeci koje se pojavljuju nakon originalne rijeci
	# vrijednosti tog rjecnika su frekvencije pojavljivanja neke
	# rijeci nakon originalne rijeci
	word_dict = dict()
	for idx, word in enumerate(new_fairy_list):  # za svaku rijec u listi rijec
		try:
			next_word = new_fairy_list[idx+1]
		except IndexError:
			continue
		if word in word_dict:  # ako rijec vec postoji kao kljuc u rijecniku
			next_word_dict = word_dict[word]  # rjecnik sljedecih rijeci
			if next_word in next_word_dict:  # ako je sljedeca rijec vec u rjecniku
				word_dict[word][next_word] += 1  # povecaj joj frekvenciju
			else:  # ako sljedeca rijec jos nije u rijecniku
				word_dict[word][next_word] = 1  # dodaj ju u rjecnik i postavi joj frekvenciju na 1
		else:  # ako originalna rijec jos ne postoji u rjecniku
			word_dict[word] = dict()  # postavi da je njena vrijednost isto rijecnik
			word_dict[word][next_word] = 1  # i dodaj riječi koja je nakon nje

	pp(word_dict)