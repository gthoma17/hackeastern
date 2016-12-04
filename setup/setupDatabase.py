import MySQLdb, string, random, csv, sys, ConfigParser
from datetime import date
from dateutil.rrule import rrule, DAILY




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

	createTables(cursor)

	#we're done here. close up shop
	db_connection.commit()
	cursor.close()
	db_connection.close()

def createTables(cursor):
	#create jobs table if it doesn't exist
	if not tblExists("w17_courses", cursor):
		createW17coursesTbl(cursor)
	if not tblExists("evals", cursor):
		createEvalsTbl(cursor)


def createDatabase(DATABASE, cursor): 
	#create our database
	print "Creating database: " +DATABASE
	cursor.execute('create database '+DATABASE)
	execStr = "ALTER DATABASE "+DATABASE+" CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;"
	cursor.execute(execStr)

def createW17coursesTbl(cursor):
	print "Creating table: w17_courses"
	cursor.execute("""
	CREATE TABLE w17_courses(
	  course_id INTEGER  NOT NULL AUTO_INCREMENT,
	  crn INTEGER,
	  subject TEXT(65535),
	  course TEXT(65535),
	  section INTEGER,
	  campus TEXT(65535),
	  credits INTEGER,
	  title TEXT(65535),
	  days TEXT(65535),
	  start_time TEXT(65535),
	  end_time TEXT(65535),
	  capacity INTEGER,
	  accounted INTEGER,
	  remaining INTEGER,
	  wl_capacity INTEGER,
	  wl_accounted INTEGER,
	  wl_remaining INTEGER,
	  xl_capacity INTEGER,
	  xl_accounted INTEGER,
	  xl_remaining INTEGER,
	  instructor_fname TEXT(65535),
	  instructor_lname TEXT(65535),
	  instructor_id INTEGER,
	  start_date TEXT(65535),
	  end_date TEXT(65535),
	  location TEXT(65535),
	  attribute TEXT(65535),
	  score TEXT(65535),
	  days2 TEXT(65535),
	  start_time2 TEXT(65535),
	  end_time2 TEXT(65535),
	  start_date2 TEXT(65535),
	  end_date2 TEXT(65535),
	  days3 TEXT(65535),
	  start_time3 TEXT(65535),
	  end_time3 TEXT(65535),
	  start_date3 TEXT(65535),
	  end_date3 TEXT(65535),
	  days4 TEXT(65535),
	  start_time4 TEXT(65535),
	  end_time4 TEXT(65535),
	  start_date4 TEXT(65535),
	  end_date4 TEXT(65535),
	  days5 TEXT(65535),
	  start_time5 TEXT(65535),
	  end_time5 TEXT(65535),
	  start_date5 TEXT(65535),
	  end_date5 TEXT(65535),
	  days6 TEXT(65535),
	  start_time6 TEXT(65535),
	  end_time6 TEXT(65535),
	  start_date6 TEXT(65535),
	  end_date6 TEXT(65535),
	  days7 TEXT(65535),
	  start_time7 TEXT(65535),
	  end_time7 TEXT(65535),
	  start_date7 TEXT(65535),
	  end_date7 TEXT(65535),
	  days8 TEXT(65535),
	  start_time8 TEXT(65535),
	  end_time8 TEXT(65535),
	  start_date8 TEXT(65535),
	  end_date8 TEXT(65535),
	  days9 TEXT(65535),
	  start_time9 TEXT(65535),
	  end_time9 TEXT(65535),
	  start_date9 TEXT(65535),
	  end_date9 TEXT(65535),
	  days10 TEXT(65535),
	  start_time10 TEXT(65535),
	  end_time10 TEXT(65535),
	  start_date10 TEXT(65535),
	  end_date10 TEXT(65535),
	  days11 TEXT(65535),
	  start_time11 TEXT(65535),
	  end_time11 TEXT(65535),
	  start_date11 TEXT(65535),
	  end_date11 TEXT(65535),
	  PRIMARY KEY(course_id)
	)
	""")

def createEvalsTbl(cursor):
	print "Creating table: Evals"
	cursor.execute("""
	CREATE TABLE evals(
	  eval_id INTEGER  NOT NULL AUTO_INCREMENT,
	  fname TEXT(65535),
	  lname TEXT(65535),
	  department TEXT(65535),
	  course TEXT(65535),
	  section INTEGER,
	  term TEXT(65535),
	  res TEXT(65535),
	  enr TEXT(65535),
	  inst_avg TEXT(65535),
	  inst_a TEXT(65535),
	  inst_b TEXT(65535),
	  inst_c TEXT(65535),
	  inst_d TEXT(65535),
	  inst_e TEXT(65535),
	  crse_avg TEXT(65535),
	  crse_a TEXT(65535),
	  crse_b TEXT(65535),
	  crse_c TEXT(65535),
	  crse_d TEXT(65535),
	  crse_e TEXT(65535),
	  PRIMARY KEY(eval_id)
	)
	""")


def tblExists(name, cursor):
	search_tbl = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = {0}"
	search_tbl = search_tbl.format(sanitize(name))
	cursor.execute(search_tbl)
	if cursor.fetchone()[0] == 1:
		return True
	else:
		return False
def tblEmpty(name, cursor):
	query = """SELECT * from {0} limit 1"""
	entry = cursor.execute(query.format(name))
	if not entry:
		return True
	else:
		return False
def makeNewApiKey(cursor):
	potentialApiKey = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(256))
	query = """SELECT * from jobAppUsers WHERE apiKey={0}"""
	entry = cursor.execute(query.format(sanitize(potentialApiKey)))
	if not entry:
		return potentialApiKey
	else:
		return makeNewApiKey()
def sanitize(inString):
	return "'"+(str(inString).replace("'","\\'").rstrip().lstrip())+"'"

if __name__ == "__main__":
	main()	