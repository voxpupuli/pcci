from flask import Flask, render_template
import redis
import json
import yaml

app = Flask(__name__)

r = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.route('/')
def root():
    return '<html><body><h2>Pcci Web Interface</h2><br><a href="/queue">Queue</a></body></html>'

@app.route('/queue')
def show_queue():
    queue_length = r.llen('todo')
    queue = []
    for i in range(queue_length):
        name = json.loads(r.lindex('todo', i))['unique_name']
        item = json.loads(r.get(name))
        #item = ('x', 'y')
        queue.append(item)

    return render_template("queue.html", queue_length=queue_length, queue=queue)

@app.route('/completed')
def show_completed():
    completed_length = r.llen('completed')
    completed = []
    for i in range(completed_length):
        item = r.rindex('completed', i)
        #item = ('x', 'y')
        queue.append(item)

    return render_template("completed.html", completed_length=completed_length, completed=completed)


if __name__ == '__main__':
    with open('webconfig.yaml') as f:
        conf = yaml.load(f.read())
    f.closed

    debug = conf['debug']
    host = conf['host']

    app.run(debug=debug, host=host)





