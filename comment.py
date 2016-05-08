#!/usr/bin/env python

# from pdb import set_trace; set_trace()

import redis
from github import Github
import config
import time
import json

# puppet-community-ci+test+3+1424905505+FAIL


def main_loop():
    while True:
        comment_to_make = r.lpop('completed')
        if comment_to_make is None:
            print "looping"
            time.sleep(5)
        else:
            comment(json.loads(comment_to_make))


def comment(comment_to_make):
    org, project, pr = comment_to_make['unique_name'].split('/')
    nodeset = comment_to_make['nodeset']
    success = comment_to_make['success']
    print "Considering: {0}".format(comment_to_make)
    print "org: {0}, project: {1}, pr {2}".format(org, project, pr)

    if project not in config.commentable:
        return

    pr_object = g.get_repo(org + "/" + project).get_pull(int(pr))
    sha = pr_object.head.sha
    print "sha: {0}".format(sha)
    commits = pr_object.get_commits()
    commit = None
    for c in commits:
        if c.sha == sha:
            commit = c
            break

    if success == 'pending':
        status = 'pending'
        target_url = config.queueurl
    else:
        if success == 0:
            status = 'success'
        else:
            status = 'failure'
        target_url = config.rooturl + comment_to_make['log_path']

    commit.create_status(status, target_url=target_url,
                         description="PCCI Voting System",
                         context="continuous-integration/pcci-{0}".format(nodeset))


if __name__ == "__main__":

    g = Github(config.pccibottoken)
    r = redis.StrictRedis(host='localhost', port=6379, db=0)

    main_loop()
