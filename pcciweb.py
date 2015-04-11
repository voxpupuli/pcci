from flask import Flask, render_template
import redis
import json
import yaml

app = Flask(__name__)

r = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.route('/')
def root():
    return '<html><body><h2>Pcci Web Interface</h2><br><a href="/queue">Queue</a><br><a href="/completed">Completed</a></body></html>'


@app.route('/queue')
def show_queue():
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
                            workers=workers,
                            queue_length=queue_length,
                            queue=queue,
                            in_progress_length=in_progress_length,
                            in_progress=in_progress)


@app.route('/completed')
def show_completed():
    completed_length = r.llen('completed')

    # redis doesn't have an rindex and python doesnt have prepend
    # so build the list in reverse order then reverse it
    rev_completed = []
    for i in range(completed_length):
        item = r.lindex('completed', i)
        #item = ('x', 'y')
        rev_completed.append(item)

    completed = rev_completed[::-1]

    return render_template("completed.html", completed_length=completed_length, completed=completed)


if __name__ == '__main__':
    with open('webconfig.yaml') as f:
        conf = yaml.load(f.read())
    f.closed

    debug = conf['debug']
    host = conf['host']

    app.run(debug=debug, host=host)





