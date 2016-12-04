import web, ConfigParser, json, string, random, socket, urllib, datetime, boto, base64
from os import path
from identitytoolkit import gitkitclient

#prepare to read config
config = ConfigParser.ConfigParser()
root = path.dirname(path.realpath(__file__))

#determine if we're on a production machine, or testing machine
# load the correct config based on that.  
config.read(path.join(root, "backend.cfg"))

urls = (
	"/", "index",
	"/courses/w17", "w17",
	"/courses/w17/(.*)/(.*)", "selCrs",
	"/courses/w17/(.*)$", "selSub",
	)

app = web.application(urls, globals())
db = web.database(dbn='mysql', host=config.get("Database", "host"), port=int(config.get("Database", "port")), user=config.get("Database", "user"), pw=config.get("Database", "password"), db=config.get("Database", "name"), charset='utf8mb4')

def set_headers():
    web.header('Access-Control-Allow-Origin',      '*')

app.add_processor(web.loadhook(set_headers))

class index:
	def GET(self): 
		return "Shhhh... the database is sleeping."
	def POST(self): 
		return "Shhhh... the database is sleeping."
class w17:
	def GET(self):
		return json.dumps(list(db.where('w17_courses')))
class selSub:
	def GET(self, sub):
		return json.dumps(list(db.where('w17_courses', subject=sub)))
class selCrs:
	def GET(self, sub, crs):
		return json.dumps(list(db.where('w17_courses', subject=sub, course=crs)))

if __name__ == "__main__":
	app.run()