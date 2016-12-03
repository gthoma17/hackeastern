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
	createTestData(cursor)

	#we're done here. close up shop
	db_connection.commit()
	cursor.close()
	db_connection.close()

def createTables(cursor):
	#create jobs table if it doesn't exist
	if not tblExists("w17_courses", cursor):
		createW17coursesTbl(cursor)
	if not tblExists("evals", cursor):
		createProfessorsTbl(cursor)

def createTestData(cursor):
	if tblEmpty("w17_courses", cursor):
		createW17courses(cursor)
	if tblEmpty("evals", cursor):
		createEvals(cursor)

def createDatabase(DATABASE, cursor): 
	#create our database
	print "Creating database: " +DATABASE
	cursor.execute('create database '+DATABASE)
	execStr = "ALTER DATABASE "+DATABASE+" CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;"
	cursor.execute(execStr)

def createW17coursesTbl(cursor):
	print "Creating table: w17_courses"
	cursor.execute("""
	CREATE TABLE courses(
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
	  instructor_name TEXT(65535),
	  instructor_id INTEGER,
	  start_date TEXT(65535),
	  end_date TEXT(65535),
	  location TEXT(65535),
	  attribute TEXT(65535),
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
	  PRIMARY KEY(id)
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
	  PRIMARY KEY(id)
	)
	""")

def createW17courses(cursor):
	#course_id INTEGER  NOT NULL AUTO_INCREMENT,
	#crn INTEGER,
	#subject TEXT(65535),
	#course TEXT(65535),
	#section INTEGER,
	#campus TEXT(65535),
	#credits INTEGER,
	#title TEXT(65535),
	#days TEXT(65535),
	#start_time TEXT(65535),
	#end_time TEXT(65535),
	#capacity INTEGER,
	#accounted INTEGER,
	#remaining INTEGER,
	#wl_capacity INTEGER,
	#wl_accounted INTEGER,
	#wl_remaining INTEGER,
	#xl_capacity INTEGER,
	#xl_accounted INTEGER,
	#xl_remaining INTEGER,
	#instructor_name TEXT(65535),
	#instructor_id INTEGER,
	#start_date TEXT(65535),
	#end_date TEXT(65535),
	#location TEXT(65535),
	#attribute TEXT(65535),
	#days2 TEXT(65535),
	#start_time2 TEXT(65535),
	#end_time2 TEXT(65535),
	#start_date2 TEXT(65535),
	#end_date2 TEXT(65535),
	#days3 TEXT(65535),
	#start_time3 TEXT(65535),
	#end_time3 TEXT(65535),
	#start_date3 TEXT(65535),
	#end_date3 TEXT(65535),
	#days4 TEXT(65535),
	#start_time4 TEXT(65535),
	#end_time4 TEXT(65535),
	#start_date4 TEXT(65535),
	#end_date4 TEXT(65535),
	#days5 TEXT(65535),
	#start_time5 TEXT(65535),
	#end_time5 TEXT(65535),
	#start_date5 TEXT(65535),
	#end_date5 TEXT(65535),
	#PRIMARY KEY(id)
	print "creating data for table: w17_courses"
	addCourse = """
	INSERT INTO w17_courses
		(id, crn, subject, course, section, campus, credits, title, days, start_time, end_time, capacity, accounted, remaining, wl_capacity, wl_accounted, wl_remaining, xl_capacity, xl_accounted, xl_remaining, instructor_name, instructor_id, start_date, end_date, location, attribute, days2, start_time2, end_time2, start_date2, end_date2)
    VALUES
    	(NULL, {0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16}, {17}, {18}, {19}, {20}, {21}, {22}, {23}, {24}, {25}, {26}, {27}, {28}, {29}, {30})
	"""
	coursesToMake = [
		{"crn":"27095" , "subject":"COSC" , "course":"211" , "section":"0" , "campus":"M1" , "credits":"3" , "title":"Programming Data Structures" , "days":"MW" , "start_time":"11:00" , "end_time":"12:50" , "capacity":"13" , "accounted":"12" , "remaining":"1" , "wl_capacity":"0" , "wl_accounted":"0" , "wl_remaining":"0" , "xl_capacity":"25" , "xl_accounted":"18" , "xl_remaining":"7" , "instructor_name":"Li Zhang" ,         "instructor_id":"" , "start_date":"01/04" , "end_date":"04/25" , "location":"PRAY-H 514" , "attribute":"Honors Only Section" , "days2":"" , "start_time2":"" , "end_time2":"" , "start_date2":"" , "end_date2":""},
		{"crn":"27102" , "subject":"COSC" , "course":"211" , "section":"0" , "campus":"M1" , "credits":"3" , "title":"Programming Data Structures" , "days":"MW" , "start_time":"19:20" , "end_time":"21:00" , "capacity":"30" , "accounted":"27" , "remaining":"3" , "wl_capacity":"0" , "wl_accounted":"0" , "wl_remaining":"0" , "xl_capacity":"0" , "xl_accounted":"0" ,   "xl_remaining":"0" , "instructor_name":"Matthew Evett" ,    "instructor_id":"" , "start_date":"01/04" , "end_date":"04/25" , "location":"PRAY-H 520" , "attribute":"" , "days2":"" , "start_time2":"" , "end_time2":"" , "start_date2":"" , "end_date2":""},
		{"crn":"27147" , "subject":"COSC" , "course":"211" , "section":"0" , "campus":"M1" , "credits":"3" , "title":"Programming Data Structures" , "days":"TR" , "start_time":"11:00" , "end_time":"12:50" , "capacity":"29" , "accounted":"29" , "remaining":"0" , "wl_capacity":"0" , "wl_accounted":"0" , "wl_remaining":"0" , "xl_capacity":"0" , "xl_accounted":"0" ,   "xl_remaining":"0" , "instructor_name":"Ranjan Chaudhuri" , "instructor_id":"" , "start_date":"01/04" , "end_date":"04/25" , "location":"PRAY-H 503" , "attribute":"" , "days2":"" , "start_time2":"" , "end_time2":"" , "start_date2":"" , "end_date2":""},
		{"crn":"27868" , "subject":"COSC" , "course":"211" , "section":"0" , "campus":"M1" , "credits":"3" , "title":"Programming Data Structures" , "days":"MW" , "start_time":"11:00" , "end_time":"12:50" , "capacity":"12" , "accounted":"6"  , "remaining":"6" , "wl_capacity":"0" , "wl_accounted":"0" , "wl_remaining":"0" , "xl_capacity":"25" , "xl_accounted":"18" , "xl_remaining":"7" , "instructor_name":"Susan Haynes" ,     "instructor_id":"" , "start_date":"01/04" , "end_date":"04/25" , "location":"PRAY-H 514" , "attribute":"" , "days2":"" , "start_time2":"" , "end_time2":"" , "start_date2":"" , "end_date2":""}
	]
	for course in coursesToMake:
		thisUserAdd = addUser.format(sanitize(user['crn']), sanitize(user['subject']), sanitize(user['course']), sanitize(user['section']), sanitize(user['campus']), sanitize(user['credits']), sanitize(user['title']), sanitize(user['days']), sanitize(user['start_time']), sanitize(user['end_time']), sanitize(user['capacity']), sanitize(user['accounted']), sanitize(user['remaining']), sanitize(user['wl_capacity']), sanitize(user['wl_accounted']), sanitize(user['wl_remaining']), sanitize(user['xl_capacity']), sanitize(user['xl_accounted']), sanitize(user['xl_remaining']), sanitize(user['instructor_name']), sanitize(user['instructor_id']), sanitize(user['start_date']), sanitize(user['end_date']), sanitize(user['location']), sanitize(user['attribute']), sanitize(user['days2']), sanitize(user['start_time2']), sanitize(user['end_time2']), sanitize(user['start_date2']), sanitize(user['end_date2']))
		cursor.execute(thisUserAdd)
def createEvals(cursor):
	print "creating data for table: evals"
	  #eval_id INTEGER  NOT NULL AUTO_INCREMENT,
	  #fname TEXT(65535),
	  #lname TEXT(65535),
	  #department TEXT(65535),
	  #course TEXT(65535),
	  #section INTEGER,
	  #term TEXT(65535),
	  #res TEXT(65535),
	  #enr TEXT(65535),
	  #inst_avg TEXT(65535),
	  #inst_a TEXT(65535),
	  #inst_b TEXT(65535),
	  #inst_c TEXT(65535),
	  #inst_d TEXT(65535),
	  #inst_e TEXT(65535),
	  #crse_avg TEXT(65535),
	  #crse_a TEXT(65535),
	  #crse_b TEXT(65535),
	  #crse_c TEXT(65535),
	  #crse_d TEXT(65535),
	  #crse_e TEXT(65535),
	  #PRIMARY KEY(id)
	addThing = """
	INSERT INTO w17_courses
		(id, crn, subject, course, section, campus, credits, title, days, start_time, end_time, capacity, accounted, remaining, wl_capacity, wl_accounted, wl_remaining, xl_capacity, xl_accounted, xl_remaining, instructor_name, instructor_id, start_date, end_date, location, attribute, days2, start_time2, end_time2, start_date2, end_date2)
    VALUES
    	(NULL, {0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16}, {17}, {18}, {19})
	"""
	thingsToMake = [
		["L","ZHANG","COSC","231","000","Wi13","19","25","3.14","33%","47%","13%","7%","0%","3.07","40%","40%","7%","13%","0%"]
	]
	for thing in thingsToMake:
		thisThingAdd = addThing.format(sanitize(thing[0]), sanitize(thing[1]), sanitize(thing[2]), sanitize(thing[3]), sanitize(thing[4]), sanitize(thing[5]), sanitize(thing[6]), sanitize(thing[7]), sanitize(thing[8]), sanitize(thing[9]), sanitize(thing[10]), sanitize(thing[11]), sanitize(thing[12]), sanitize(thing[13]), sanitize(thing[14]), sanitize(thing[15]), sanitize(thing[16]), sanitize(thing[17]), sanitize(thing[18]), sanitize(thing[19]))
		cursor.execute(thisThingAdd)
