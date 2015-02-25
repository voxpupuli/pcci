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
    workers = int(r.get('workers'))
    print "found {0} workers".format(workers)
    if workers >= config.workers:
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
        tempdir = create_pr_env('puppet-community-ci/test/1')
        run_beaker_rspec(tempdir)
        clean_tempdir(tempdir)

def create_pr_env(work_item):
    print "working on {0}".format(work_item)
    org, project, pr = work_item.split('/')
    tempdir = tempfile.mkdtemp()
    git_clone = subprocess.call(["git", "clone", "https://github.com/{0}/{1}".format(org, project), tempdir + "/job"])
    subprocess.Popen(["git", "fetch", "origin", "pull/{0}/head:pr_{0}".format(pr)], cwd=(tempdir + "/job")).communicate()
    subprocess.Popen(["git", "checkout", "pr_{0}".format(pr)], cwd=(tempdir + "/job")).communicate()
    return tempdir

def run_beaker_rspec(tempdir):
    out,err = subprocess.Popen(["bundle", "exec", "beaker", "spec/acceptance"], cwd=(tempdir + "/job"), stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    print "the out is"
    print out
    print "the err is"
    print err

def clean_tempdir(tempdir):
    shutil.rmtree(tempdir)


if __name__ == "__main__":
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    setup_worker()
    main_loop()


