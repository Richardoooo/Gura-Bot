###expression:表达式###
###original_number:原来的四个数(列表)###
def point(expression,original_number):
	print(str(expression),"   ",original_number)
	full_num_list = [1,2,3,4,5,6,7,8,9]
	list_without_original_number = [i for i in full_num_list if i not in original_number]
	for i in list_without_original_number:
		if str(i) in str(expression):
			print("??")
			return "IncorrectNumber"
	for i in original_number:
		if str(expression).count(str(i)) != 1:
			return "RepeatNumber"
	if eval(expression) == 24:
		return True
	else:
		return False