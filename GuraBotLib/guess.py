def number_guess(number,original_number):
	number = list(str(number))
	original_number = list(str(original_number))
	final = ""
	for i in range(len(number)):
		if number[i] == original_number[i]:
			final += "A"
		else:
			if number[i] not in original_number:
				final += "C"
			else:
				final += "B"
	return final