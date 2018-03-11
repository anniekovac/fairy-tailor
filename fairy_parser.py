import os


def parser():
	txt_file = "grimm.txt"
	txt_dict = dict()
	with open(txt_file, "r") as file:
		flag = False
		for line in file:

			if line[0].isdigit():
				title = line.strip(os.linesep)
				txt_dict[title] = ""
				flag = True
			elif flag and title:
				if line.strip(os.linesep):  # if line is not only \n
					txt_dict[title] += line
	return txt_dict

if __name__ == '__main__':
	parser()
