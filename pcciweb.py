from flask import Flask, render_template
import redis
import json

app = Flask(__name__)

r = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.route('/')
def root():
    return 'Pcci Web Interface'

@app.route('/queue')
def show_queue():
    print 'science'
    queue_length = r.llen('todo')
    queue = []
    for i in range(queue_length):
        name = json.loads(r.lindex('todo', i))['unique_name']
        item = json.loads(r.get(name))
        print item['name']
        print item['time']
        #item = ('x', 'y')
        queue.append((item['name'], item['time']))


    resp =  "<html><head></head><body>"
    resp += "Queue Length {0}<p>".format(queue_length)
    resp += "<table>"
    for item in queue:
        a,b = item
        resp += "<tr><td>{0}</td><td>{1}</td>".format(a, b)
    resp += "</table>"
    resp += "</body></html>"
    return resp

if __name__ == '__main__':
    app.run(debug=True)
