import os
import commands

output = commands.getoutput("ps -aux | grep gdm")

parsedString = str(output).split("\n")

for line in parsedString:
	parsedLine = line.split(' ')
	while "" in parsedLine:
		parsedLine.remove("")
	print parsedLine[1]
	killCommand = "kill " + parsedLine[1]
	os.system(killCommand)
