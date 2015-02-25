
#from pdb import set_trace; set_trace()

import redis
from github import Github
import config
import time

# puppet-community-ci+test+1+1424905505+FAIL

def main_loop():
    while True:
        comment_to_make = r.lpop('completed')
        if comment_to_make is None:
            print "looping"
            time.sleep(5)
        else:
            comment(comment_to_make)


def comment(comment_to_make):
    org, project, pr, ts, success = comment_to_make.split('+')

    if project in config.commentable:
        pass
    else:
        return

    #from pdb import set_trace; set_trace()
    prs = g.get_repo(org + "/" + project).get_issues()


    pr_object = None

    for particular_pr in prs:
        if particular_pr.number == int(pr):
            pr_object = particular_pr
            break

    response_string = """
    The result of the test was: {0}
    Details at {1}/{2}

    I am a beta ci bot. I am probably lying to you.
    You can contact nibalizer for more details
    """.format(success, config.rooturl, comment_to_make)

    pr_object.create_comment(response_string)


if __name__ == "__main__":

    g = Github("puppet-community-ci", config.password)
    r = redis.StrictRedis(host='localhost', port=6379, db=0)

    main_loop()





