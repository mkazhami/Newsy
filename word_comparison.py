
punctuation = [',', '.']

def remove_puctuation(s):
	for c in punctuation:
		s = s.replace(c, "")
	return s


def number_of_substrings(s):
	count = 0
	for i in range(0,len(s)):
		for j in range(i, len(s)):
			count += 1
	return count

# consider anything above 0.9 to be very similar
def compare_words(s1, s2):
	s1 = remove_puctuation(s1)
	s2 = remove_puctuation(s2)

	# split up multiple words
	s1 = s1.split(" ")
	s2 = s2.split(" ")

	largest_match_word1 = " "
	largest_match_word2 = " "
	entire_word_match_count = 0
	max_substring_length = 0
	substring_matches = []
	# inefficient way of checking similarity
	# TODO: replace with trie implementation later
	for word1 in s1:
		for word2 in s2:
			word1 = word1.lower()
			word2 = word2.lower()
			for i in range(len(word1) - 1):
				subword1 = word1[i:]
				for j in range(len(word2) - 1):
					subword2 = word2[j:]

					count = 0
					min_length = len(subword1) if len(subword1) < len(subword2) else len(subword2)
					while count < min_length and subword1[count] == subword2[count]:
						count += 1


					if count > max_substring_length:
						max_substring_length = count
						largest_match_word1 = word1
						largest_match_word2 = word2

					# match of 3 or more characters is good
					if count >= 3:
						substring_matches.append(count)

					# if one of the words matched entirely
					if count in (len(word1), len(word2)):
						#print("entire word matched: {} and {}".format(word1, word2))
						entire_word_match_count += 1


	#print((float(entire_word_match_count) / max([len(s1), len(s2)])))
	#print(float(len(substring_matches)) / (number_of_substrings(s1) * number_of_substrings(s2)))
	#print(max_substring_length / min([len(largest_match_word1), len(largest_match_word2)]))
	#print(1 if entire_word_match_count > 0 else 0)

	score = (float(entire_word_match_count) / max([len(s1), len(s2)])) * 0.2 + \
			(float(len(substring_matches)) / (number_of_substrings(s1) * number_of_substrings(s2))) * 0.05 + \
			(max_substring_length / min([len(largest_match_word1), len(largest_match_word2)])) * 0.25 + \
			(1 if entire_word_match_count > 0 else 0) * 0.5

	return score
	#print("max substring match length: {}".format(max_substring_length))
	#print("entire word match count: {}".format(entire_word_match_count))
	#print("score is {}".format(score))


# just get number of capitalized words for now - decent measure for importance
def word_importance(s):
	words = s.split(" ")
	capitalized = 0
	for word in words:
		if len(word) > 0 and word[0] >= 'A' and word[0] < 'Z':
			capitalized += 1
	return capitalized / len(words)

