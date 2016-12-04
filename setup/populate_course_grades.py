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
	insertCourseGrades(cursor)
	#we're done here. close up shop
	db_connection.commit()
	cursor.close()
	db_connection.close()

def insertCourseGrades(cursor):
	updateRecord = """
	UPDATE w17_courses
    SET crse_avg={0}, crse_a={1}, crse_b={2}, crse_c={3}, crse_d={4}, crse_e={5}
    WHERE department={6} AND course={7} 
	"""
	search_course = ("SELECT * FROM evals WHERE department={0} AND course={1}")
	with open('just_courses.txt', 'rb') as csvfile:
		Reader = csv.reader(csvfile, delimiter=',')
		for row in Reader:
			mult = 0
			runningAvg = 0
			runningA = 0
			runningB = 0
			runningC = 0
			runningD = 0
			runningE = 0
			query = search_course.format(sanitize(row[0]),sanitize(row[1]))
			if cursor.execute(query):
				tblRow = cursor.fetchone()
				while tblRow is not None:
					runningAvg = runningAvg + float(tblRow[-1][:-1])
					runningA = runningA + float(tblRow[-6][:-1])
					runningB = runningB + float(tblRow[-5][:-1])
					runningC = runningC + float(tblRow[-4][:-1])
					runningD = runningD + float(tblRow[-3][:-1])
					runningE = runningE + float(tblRow[-2][:-1])
					mult = mult + 1
				query = updateRecord.format((runningAvg/mult),(runningA/mult),(runningB/mult),(runningC/mult),(runningD/mult),(runningE/mult),course_pfix,course_num)
				cursor.execute(query)

def sanitize(inString):
	return "'"+(str(inString).replace("'","\\'").rstrip().lstrip())+"'"

if __name__ == '__main__':
	main()