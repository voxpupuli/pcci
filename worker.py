import shutil
import signal
import subprocess
import sys
import tempfile
import time

import redis

import config


def signal_handler(signal, frame):
    print('Shutting down worker')
    r.decr('workers')
    sys.exit(0)


def setup_worker():
    #register as a worker
    workers = r.get('workers')
    if workers is None:
        r.set('workers', 0)
    else:
        print "found {0} workers".format(workers)
        if int(workers) >= config.workers:
            # we already have enough workers
            print "deactivating because we already have enough workers"
            sys.exit()
    r.incr('workers')


def main_loop():
    #never exits
    while True:
        print 'looping'
        work_item = r.lpop('todo')
        if work_item == None:
            time.sleep(5)
            continue
        tempdir = create_pr_env(work_item)
        run_beaker_rspec(tempdir)
        clean_tempdir(tempdir)

def create_pr_env(work_item):
    print "working on {0}".format(work_item)
    org, project, pr = work_item.split('/')
    tempdir = tempfile.mkdtemp()
    git_clone = subprocess.call(["git", "clone", "https://github.com/{0}/{1}".format(org, project), tempdir + "/job"])
    subprocess.Popen(["git", "fetch", "origin", "pull/{0}/head:pr_{0}".format(pr)], cwd=(tempdir + "/job")).communicate()
    subprocess.Popen(["git", "checkout", "pr_{0}".format(pr)], cwd=(tempdir + "/job")).communicate()
    return str(tempdir)

def run_beaker_rspec(tempdir):
    jobdir = tempdir + "/job"
    print "running in {0}".format(jobdir)
    out,err = subprocess.Popen(["bundle", "exec", "beaker", "spec/acceptance"], cwd=jobdir, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    print "the out is"
    print out
    print "the err is"
    print err

def clean_tempdir(tempdir):
    shutil.rmtree(tempdir)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    setup_worker()
    main_loop()


