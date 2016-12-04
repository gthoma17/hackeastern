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
	emptyEvalTbl(cursor)
	parseCSV(cursor)	
	#we're done here. close up shop
	db_connection.commit()
	cursor.close()
	db_connection.close()

def emptyEvalTbl(cursor):
	cursor.execute("TRUNCATE evals;")

def parseCSV(cursor):
	print "Parsing CSV"
	with open('eval_input.txt', 'rb') as csvfile:
		evalReader = csv.reader(csvfile, delimiter=',')
		for row in evalReader:
			#if row has grade, insert into database
			if len(row) != 18: #record doesn't have eval data
				print "Skipping: "+row[5]+row[2]+row[3]+row[4]+" numcols: "+str(len(row))
				pass
			else:
				print "Adding: "+row[5]+row[2]+row[3]+row[4]
				insertEvalRecord(cursor, row)
def insertEvalRecord(cursor, csvRow):
	addRecord = """
	INSERT INTO evals
		(eval_id, fname, lname, department, course, section , term, res, enr, inst_a, inst_b, inst_c, inst_d, inst_e, crse_a, crse_b, crse_c, crse_d, crse_e, inst_avg, crse_avg)
    VALUES
    	(NULL, {0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16}, {17}, {18}, {19})
	"""
	res = float(csvRow[6])
	instAvg = (((res*(float(csvRow[8].strip('%')))/100)*4) + ((res*(float(csvRow[9].strip('%')))/100)*3) + ((res*(float(csvRow[10].strip('%')))/100)*2) + ((res*(float(csvRow[11].strip('%')))/100)*1)) / res
	crseAvg = (((res*(float(csvRow[13].strip('%')))/100)*4) + ((res*(float(csvRow[14].strip('%')))/100)*3) + ((res*(float(csvRow[15].strip('%')))/100)*2) + ((res*(float(csvRow[16].strip('%')))/100)*1)) / res
	query = addRecord.format(sanitize(csvRow[0]),sanitize(csvRow[1]),sanitize(csvRow[2]),sanitize(csvRow[3]),sanitize(csvRow[4]),sanitize(csvRow[5]),sanitize(csvRow[6]),sanitize(csvRow[7]),sanitize(csvRow[8]),sanitize(csvRow[9]),sanitize(csvRow[10]),sanitize(csvRow[11]),sanitize(csvRow[12]),sanitize(csvRow[13]),sanitize(csvRow[14]),sanitize(csvRow[15]),sanitize(csvRow[16]),sanitize(csvRow[17]), sanitize(instAvg), sanitize(crseAvg))
	cursor.execute(query)



def sanitize(inString):
	return "'"+(str(inString).replace("'","\\'").rstrip().lstrip())+"'"

if __name__ == '__main__':
	main()