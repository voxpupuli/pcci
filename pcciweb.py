import datetime

from flask import Flask, render_template
import redis
import json
import yaml

app = Flask(__name__)

r = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.route('/')
def root():
    time = str(datetime.datetime.now())
    return render_template("index.html")


@app.route('/queue')
def show_queue():
    time = str(datetime.datetime.now())

    workers = r.get('workers')

    queue_length = r.llen('todo')
    queue = []
    for i in range(queue_length):
        name = json.loads(r.lindex('todo', i))['unique_name']
        item = json.loads(r.get(name))
        #item = ('x', 'y')
        queue.append(item)

    in_progress_names = r.smembers('in_progress')
    in_progress_length = len(in_progress_names)
    in_progress = []
    for name in in_progress_names:
        item = json.loads(r.get(name))
        #item = ('x', 'y')
        in_progress.append(item)


    return render_template("queue.html",
                            time=time,
                            workers=workers,
                            queue_length=queue_length,
                            queue=queue,
                            in_progress_length=in_progress_length,
                            in_progress=in_progress)


@app.route('/completed')
def show_completed():
    time = str(datetime.datetime.now())
    completed_length = r.llen('completed')

    # redis doesn't have an rindex and python doesnt have prepend
    # so build the list in reverse order then reverse it
    rev_completed = []
    for i in range(completed_length):
        item = r.lindex('completed', i)
        #item = ('x', 'y')
        rev_completed.append(item)

    completed = rev_completed[::-1]

    return render_template("completed.html", time=time, completed_length=completed_length, completed=completed)


@app.route('/modules')
def show_modules():
    time = str(datetime.datetime.now())

    repos = list(r.smembers('repos'))

    return render_template("modules.html", time=time, repos=repos)

@app.route('/modules/<path:module_name>')
def show_module_by_name(module_name):
    time = str(datetime.datetime.now())

    completed_length = r.llen(module_name)

    # redis doesn't have an rindex and python doesnt have prepend
    # so build the list in reverse order then reverse it
    rev_completed = []
    for i in range(completed_length):
        item = json.loads(r.lindex(module_name, i))
        #item = ('x', 'y')
        rev_completed.append(item)

    completed = rev_completed[::-1]

    return render_template("completed.html", time=time, completed_length=completed_length, completed=completed)


if __name__ == '__main__':
    with open('webconfig.yaml') as f:
        conf = yaml.load(f.read())
    f.closed

    debug = conf['debug']
    host = conf['host']

    app.run(debug=debug, host=host)



