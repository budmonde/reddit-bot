import math

def text_to_dict(file_path):
	file_text = open(file_path).read().lower()
	all_chars = list(file_text)

	num_chars = len(all_chars)
	char_dict = {}

	for char in all_chars:
		char_dict[char] = char_dict.get(char, 0) + (1.0/num_chars)

	return char_dict

def text_to_words(file_path, _set=False):
	file_text = open(file_path).read().lower()
	file_words = file_text.split()

	if _set:
		file_words = set(file_words)

	return file_words

def text_sorted_char_dist(file_path, to_keep):
	char_dict = text_to_dict(file_path)
	sorted_chars = sorted(char_dict.items(), key=lambda x: x[1], reverse=True)
	to_keep = min(to_keep, len(sorted_chars))

	return sorted_chars[:to_keep]

def text_kl_divergence(file_path_1, file_path_2):
	file_1_dict = text_to_dict(file_path_1)
	file_2_dict = text_to_dict(file_path_2)

	file_1_chars = file_1_dict.keys()
	file_2_chars = file_2_dict.keys()
	shared_chars = list(set(file_1_chars) & set(file_2_chars))
	num_shared_chars = len(shared_chars)

	kld = 0

	for char in shared_chars:
		p_i = file_1_dict[char]
		q_i = file_2_dict[char]

		kld += p_i * math.log(p_i/q_i)

	return kld

def expected_random_kl_divergence(file_path_1):
	file_1_dict = text_to_dict(file_path_1)
	file_1_chars = file_1_dict.keys()
	num_chars = len(file_1_chars)

	kld = 0

	for char in file_1_chars:
		p_i = file_1_dict[char]
		q_i = 1.0 / num_chars

		kld += p_i * math.log(p_i/q_i)

	return kld

def real_to_total(output_file_path, training_file_path):
	output_words = text_to_words(output_file_path)
	training_words = text_to_words(training_file_path, True)

	num_output_words = len(output_words) * 1.0
	count_real_words = 0

	for word in output_words:
		if word in training_words:
			count_real_words += 1

	return count_real_words/num_output_words






# print '4qo3ia vs. wikipedia:'
# print text_kl_divergence('./data/4qo3ia.txt', './data/ball-wikipedia.txt')
# print text_kl_divergence('./data/4qo3ia.txt', './data/dance-wikipedia.txt')
# print '\n'

# print '4qo3ia vs. other reddit stuff:'
# print text_kl_divergence('./data/4qo3ia.txt', './data/4ulqap.txt')
# print text_kl_divergence('./data/4qo3ia.txt', './data/4vq7rj.txt')
# print '\n'

# print '4qo3ia vs. hamlet and romeo and juliet:'
# print text_kl_divergence('./data/4qo3ia.txt', './data/hamlet.txt')
# print text_kl_divergence('./data/4qo3ia.txt', './data/romeoandjuliet.txt')
# print '\n'

# print '4qo3ia vs. the book of genesis:'
# print text_kl_divergence('./data/4qo3ia.txt', './data/genesis.txt')
# print '\n'

# print '4qo3ia vs. obama and trump:'
# print text_kl_divergence('./data/4qo3ia.txt', './data/obama.txt')
# print text_kl_divergence('./data/4qo3ia.txt', './data/trump.txt')
# print '\n'

# print '4qo3ia vs. wonderland:'
# print text_kl_divergence('./data/4qo3ia.txt', './data/wonderland.txt')
# print '\n'

# print '4qo3ia vs. random:'
# print expected_random_kl_divergence('./data/4qo3ia.txt')
# print '\n'

# print '4qo3ia vs. keras baseline chars 4qo3ia'
# print text_kl_divergence('./data/4qo3ia.txt', './allresults/baseline_chars_4qo3ia_output.txt')
# print '\n'

# print '4qo3ia vs. keras baseline words 4qo3ia'
# print text_kl_divergence('./data/4qo3ia.txt', './allresults/baseline_words_4qo3ia_output.txt')
# print '\n'

# print '4qo3ia vs. keras bigger words 4qo3ia'
# print text_kl_divergence('./data/4qo3ia.txt', './allresults/bigger_words_4qo3ia_output.txt')
# print '\n'