import MySQLdb, string, random, csv, sys, ConfigParser

def main():
	config = ConfigParser.ConfigParser()
	config.read("backend.cfg")	

	#db access info
	HOST = config.get("Database", "host")
	USER = config.get("Database", "user")
	PASSWD = config.get("Database", "password")
	DATABASE = config.get("Database", "name")
	
	# make a connection to the database
	db_connection = MySQLdb.connect(
		host=HOST,
		user=USER, 
		passwd=PASSWD, 
	)
	
	#create cursor
	cursor = db_connection.cursor()	
	#create our database if it doesn't exist
	try:
		cursor.execute('use '+DATABASE)
	except:
		createDatabase(DATABASE, cursor)
	finally:
		cursor.execute('use '+DATABASE)	
	emptyCoursesTbl(cursor)
	parseCSV(cursor)	
	#we're done here. close up shop
	db_connection.commit()
	cursor.close()
	db_connection.close()

def emptyCoursesTbl(cursor):
	cursor.execute("TRUNCATE w17_courses;")

def parseCSV(cursor):
	print "Parsing CSV"
	with open('course_input.txt', 'rb') as csvfile:
		evalReader = csv.reader(csvfile, delimiter=',')
		for row in evalReader:
			#if row has grade, insert into database
			if len(row) != 25: #record doesn't have valid data
				print "Data Anomoly: "+row[0]+" numcols: "+str(len(row))
				pass
			elif row[0].strip() == "&nbsp;":
				numDay = numDay + 1
				#print "Updating "+str(lastid)+" with day #"+str(numDay)
				addStartTime(cursor, row, lastid, numDay)
			else:
				#print "Adding: "+row[0]
				lastid = insertCourseRecord(cursor, row)
				numDay = 1
def insertCourseRecord(cursor, csvRow):
	addRecord = """
	INSERT INTO w17_courses
		(course_id, crn, subject, course, section, campus, credits, title, days, start_time, end_time, capacity, accounted, remaining, wl_capacity, wl_accounted, wl_remaining, xl_capacity, xl_accounted, xl_remaining, instructor_fname, instructor_lname, start_date, end_date, location, attribute, score)
    VALUES
    	(NULL, {0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16}, {17}, {18}, {19}, {20}, {21}, {22}, {23}, {24}, {25})
	"""
	
	score = makeScore(cursor, sanitize(csvRow[19]), sanitize(csvRow[20]), sanitize(csvRow[1]), sanitize(csvRow[2]))
	#print "Submitting: "+query
	query = addRecord.format(sanitize(csvRow[0]),sanitize(csvRow[1]),sanitize(csvRow[2]),sanitize(csvRow[3]),sanitize(csvRow[4]),sanitize(csvRow[5]),sanitize(csvRow[6]),sanitize(csvRow[7]),sanitize(csvRow[8]),sanitize(csvRow[9]),sanitize(csvRow[10]),sanitize(csvRow[11]),sanitize(csvRow[12]),sanitize(csvRow[13]),sanitize(csvRow[14]),sanitize(csvRow[15]),sanitize(csvRow[16]),sanitize(csvRow[17]), sanitize(csvRow[18]), sanitize(csvRow[19]), sanitize(csvRow[20]), sanitize(csvRow[21]), sanitize(csvRow[22]), sanitize(csvRow[23]), sanitize(csvRow[24]), sanitize(score))
	return cursor.execute(query)

def addStartTime(cursor, csvRow, eval_id, dayNum):
	#days2 TEXT(65535),
	#start_time2 TEXT(65535),
	#end_time2 TEXT(65535),
	#start_date2 TEXT(65535),
	#end_date2 TEXT(65535),
	setString = "SET (days{0}, start_time{0}, end_time{0}, start_date{0}, end_date{0})"
	setString = setString.format(dayNum)
	updateRecord = """
	UPDATE  w17_courses
	{0}
	VALUES ({1}, {2}, {3}, {4}, {5})
	WHERE course_id={6}
	"""
	query = updateRecord.format(setString,sanitize(csvRow[7]),sanitize(csvRow[8]),sanitize(csvRow[9]),sanitize(csvRow[20]),sanitize(csvRow[21]),eval_id)
	#cursor.execute(query)
def makeScore(cursor, prof_fname, prof_lname, course_pfix, course_num):
	#print "Scoring: "+prof_fname+prof_lname+course_pfix+course_num
	mult = 0
	runningScore = 0
	search_prof_and_course = ("SELECT * FROM evals WHERE fname={0} AND lname={1} AND department={2} AND course={3}")
	search_prof = ("SELECT * FROM evals WHERE fname={0} AND lname={1}")
	search_course = ("SELECT * FROM evals WHERE department={0} AND course={1}")

	#print "Scoring: "+prof_fname+prof_lname+course_pfix+course_num

	if prof_fname == "TBA":
		return -1
	query = search_prof_and_course.format(prof_fname,prof_lname,course_pfix,course_num)
	#print "query1: "+query
	if cursor.execute(query):
		tblRow = cursor.fetchone()
		while tblRow is not None:
			#print tblRow
			runningScore = runningScore + (float(tblRow[9]) * 5)
			mult = mult + 5
			tblRow = cursor.fetchone()
	query = search_prof.format(prof_fname,prof_lname)
	#print "query2: "+query
	if cursor.execute(query):
		tblRow = cursor.fetchone()
		while tblRow is not None:
			runningScore = runningScore + (float(tblRow[9]) * 3)
			mult = mult + 3
			tblRow = cursor.fetchone()
	if mult != 0:
		print "Scored: "+str((runningScore / mult))+" : "+prof_fname+prof_lname+course_pfix+course_num
		return (runningScore / mult)
	else:
		return -1

def sanitize(inString):
	return "'"+(str(inString).replace("'","\\'").rstrip().lstrip())+"'"

if __name__ == '__main__':
	main()