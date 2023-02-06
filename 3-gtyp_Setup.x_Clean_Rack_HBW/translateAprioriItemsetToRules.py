file = open("rules5_itemsets.txt")
lines = file.readlines()

actuator_file = open("actuator.txt")
actuator = actuator_file.readlines()[0]

for l in lines:
	line = "1. support = 1 (100%) , confidence = 100 %  :  "
	splitted_line = l.split(", ")
	part1 = splitted_line[0][2:]
	part2 = splitted_line[1][:splitted_line[1].find(" }")]

	side1 = ""
	side2 = ""

	var = part1[:part1.find(" =")]
	val = part1[part1.find(" = ")+3:]
	if val.isnumeric():
		side1 += var + " in [" + val + "; " + val + "]"
	else:
		side1 += var + " = " + val

	var = part2[:part2.find(" =")]
	val = part2[part2.find(" = ")+3:]
	if val.isnumeric():
		side2 += var + " in [" + val + "; " + val + "]"
	else:
		side2 += var + " = " + val
		
	if actuator in side1:
		line += side2 + "   -->   " + side1
	else:
		line += side1 + "   -->   " + side2

	print(line)

