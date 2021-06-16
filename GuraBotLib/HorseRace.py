def race(length):
	members = ["🦈","🐙","🥜","🦃","👻"]
	who_is_win = [False,False,False,False,False]
	output = ""
	for i in range(5):
		if length[i] >= 19:
			length[i] = 19
			who_is_win[i] = True
		else:
			who_is_win[i] = False
		output += "{}:".format(i+1)+"="*(19-int(length[i]))+members[i]+"="*int(length[i])+"\n"
	return output,who_is_win