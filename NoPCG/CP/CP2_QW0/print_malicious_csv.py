filtered_lines = []

mal_result_f = open("result_malicious.txt", "r")
lines = mal_result_f.readlines()

# print(lines)
mal_index = []
for l in lines:
	if "Violation: Sample " in l:
		l_substr = l[len("Violation: Sample "):]
		line_no = l_substr[:l_substr.find(":")]
		print(line_no)
		mal_index.append(int(line_no))


f_name = "ChemicalPlant-ActuatorAttack.csv"

samples_f = open(f_name, "r")
lines = samples_f.readlines()

output_f = open(f_name[:-4] + "_output" + f_name[-4:], "w")


i = 0
for l in lines:
	if i == 0 or i-1 in mal_index:
		output_f.write(l)
		i += 1
		# print("Y) i = " + str(i))
		continue

	# print("N) i = " + str(i))
	i += 1
