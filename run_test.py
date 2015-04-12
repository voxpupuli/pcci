import datetime
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time

import redis

import config

def write_nodeset(path):
    ns = """
HOSTS:
  ubuntu-server-14041-x64:
    roles:
      - master
    platform: ubuntu-14.04-amd64
    user: 'vagrant'
    password: 'vagrant'
    hypervisor : libvirt
    qcow2: '/home/pcci/sandbox/ubuntuvagrant.qcow2'
    private_key_file: '/home/pcci/.vagrant_private.key'
CONFIG:
  type: foss
    """
    with open(path, 'w') as f:
        f.write(ns)
    f.closed


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


def signal_handler(signal, frame):
    print('Shutting down worker')
    r.decr('workers')
    sys.exit(0)


def create_pr_env(work_item):
    print "working on {0}".format(work_item)
    org, project, pr = work_item.split('/')
    tempdir = tempfile.mkdtemp()
    git_clone = subprocess.call(["git", "clone", "https://github.com/{0}/{1}".format(org, project), tempdir + "/job"])
    if pr != 'master':
        subprocess.Popen(["git", "fetch", "origin", "pull/{0}/head:pr_{0}".format(pr)], cwd=(tempdir + "/job")).communicate()
        subprocess.Popen(["git", "checkout", "pr_{0}".format(pr)], cwd=(tempdir + "/job")).communicate()
    return str(tempdir)


def run_beaker_rspec(tempdir):
    # Record starttime
    t1 = datetime.datetime.utcnow()

    jobdir = tempdir + "/job"
    print "running in {0}".format(jobdir)

    # Setup environment
    runenv = os.environ.copy()
    runenv["BEAKER_set"] = 'libvirt'
    runenv["GEM_HOME"] = '/home/pcci/ruby_pcci_gempath'
    runenv["PATH"] = '/home/pcci/ruby_pcci_gempath/bin:' + runenv["PATH"]
    print "Using libvirt nodeset"

    # Write out nodeset file
    write_nodeset(jobdir + '/spec/acceptance/nodesets/libvirt.yml')

    # Run the test
    beaker = subprocess.Popen(["rspec", "spec/acceptance"], cwd=jobdir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=runenv)
    out, err = beaker.communicate()

    # Record endtime, calculate t delta
    t2 = datetime.datetime.utcnow()
    t_delta = t2 - t1

    # Setup response object
    response = { 'out'     : out,
                 'err'     : err,
                 'success' : int(beaker.returncode),
                 'time'    : int(t_delta.seconds),
                 'harness_failure': False,
                 }

    # The most important metadata
    if response['success'] == 0:
        print "Tests passed"
    else:
        print "Tests failed"

    return response


def write_log(work_item, response):
    path = config.logpath
    org, project, pr = work_item.split('/')
    if response['success'] == 0:
        succ = 'PASS'
    else:
        succ = 'FAIL'
    unix_seconds = datetime.datetime.utcnow().strftime('%s')
    filename =  "{0}+{1}+{2}+{3}+{4}".format(org,project,pr,unix_seconds,succ)
    if response['harness_failure']:
        filename = "harness_failures/" + filename

    with open(path + "/" + filename, 'w') as f:
        f.write("Test log\n")
        f.write("Test performed at {0} - {1}\n".format(unix_seconds, datetime.datetime.utcnow()))
        f.write("{0}/{1} PR # {2}\n".format(org, project, pr))
        f.write("Took {0} Seconds\n".format(response['time']))
        if response['success'] == 0:
            f.write("Tests passed\n")
        else:
            f.write("Tests failed\n")
        for line in response['out']:
            f.write(line)
        for line in response['err']:
            f.write(line)
    f.closed
    return (filename)



if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    setup_worker()
    work_item = json.loads(r.lpop('todo'))
    if work_item == None:
        print "No work to do, shutting down"
        sys.exit()
    print "starting work on {0}".format(work_item)
    job = json.loads(r.get(work_item['unique_name']))
    now = str(datetime.datetime.now())
    job['now'] = now
    r.set(work_item['unique_name'], json.dumps(job))
    r.sadd("in_progress", work_item['unique_name'])
    response = {}
    tempdir = create_pr_env(work_item['unique_name'])
    response = run_beaker_rspec(tempdir)

    # write log
    log_path = write_log(work_item['unique_name'], response)
    print "log written to {0}".format(log_path)

    # record test results
    r.rpush('completed', log_path)

    # record test results
    module_name = "/".join(work_item['unique_name'])
    test = {}
    test['unique_name'] = work_item['unique_name']
    test['response'] = response
    test['pull'] = job
    test['log_path'] = log_path
    r.push(test_name, json.dumps(test))

    # Cleanup
    r.srem("in_progress", work_item['unique_name'])
    print('Shutting down worker')
    r.decr('workers')


