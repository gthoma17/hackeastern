import web, ConfigParser, json, string, random, socket, urllib, datetime, boto, base64
from os import path
from identitytoolkit import gitkitclient
import plotly.plotly as py
import plotly.graph_objs as go

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
	"/eval/(.*)/(.*)/(.*)/(.*)", "eval",
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
class eval:
	def GET(self, f_name, l_name, sub, crs):
		runningA = 0
		runningB = 0
		runningC = 0
		runningD = 0
		runningE = 0
		mult = 0
		bestEvals = list(db.where('evals', fname=f_name, lname=l_name, department=sub, course=crs))
		goodEvals = list(db.where('evals', fname=f_name, lname=l_name))
		for val in bestEvals:
			val = dict(val)
			runningA = runningA + (float(val['inst_a'][0:-1])*5)
			runningB = runningB + (float(val['inst_b'][0:-1])*5)
			runningC = runningC + (float(val['inst_c'][0:-1])*5)
			runningD = runningD + (float(val['inst_d'][0:-1])*5)
			runningE = runningE + (float(val['inst_e'][0:-1])*5)
			mult = mult + 5
		for val in goodEvals:
			val = dict(val)
			runningA = runningA + float(val['inst_a'][0:-1])
			runningB = runningB + float(val['inst_b'][0:-1])
			runningC = runningC + float(val['inst_c'][0:-1])
			runningD = runningD + float(val['inst_d'][0:-1])
			runningE = runningE + float(val['inst_e'][0:-1])
			mult = mult + 1
		ret = {}
		ret['a'] = runningA / mult
		ret['b'] = runningB / mult
		ret['c'] = runningC / mult
		ret['d'] = runningD / mult
		ret['e'] = runningE / mult
		
		return json.dumps(ret)
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