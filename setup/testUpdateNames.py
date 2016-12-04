def updateNames():
	nameFile = open("name_equates.txt","r")
	for line in nameFile.readlines():
		names = line.split(";")
		print line
		new_fname = names[0].split(",")[0]
		new_lname = names[0].split(",")[1]
		old_fname = names[1].split(",")[0]
		old_lname = names[1].split(",")[1]

		updateRecord = """
		UPDATE  evals
		SET (fname, lname)
		VALUES ({0}, {1})
		WHERE fname={2} AND lname={3}
		"""
		query = updateRecord.format(sanitize(new_fname),sanitize(new_lname),sanitize(old_fname),sanitize(old_lname))
		print "Ran: "+query
def sanitize(inString):
	return "'"+(str(inString).replace("'","\\'").rstrip().lstrip())+"'"

if __name__ == '__main__':
	updateNames()