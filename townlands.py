import pandas as pd


def top10(input_list):
	# makes a dict of strings -> no. of appearances
	# returns the top ten strings

	counter_dict = {}
	
	for word in input_list:
		if word in counter_dict:
			counter_dict[word] += 1
		else:
			counter_dict[word] = 1

	most_common = sorted(counter_dict, key = counter_dict.get, 
                             reverse = True)

	top_10 = []
	for i in range(10):
		word = most_common[i]
		word_tuple = (word, counter_dict[word])
		top_10.append(word_tuple)

	return top_10


if __name__ == '__main__':

	df = pd.read_csv('townlands-no-geom.csv')
	ga_names = df[df.NAME_EN.notnull()].NAME_EN.values	

	first_words = [i.split(' ')[0] for i in ga_names]
	print top10(first_words)
