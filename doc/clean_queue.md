Cleaning The Queue
==================


Sometimes jobs crash. When jobs crash they hang out in the in progress section forever, confusing humans and using up worker slots.
To clean the queue, use the ``redis-cli`` utility.
The in progress queue is controlled by the in_progress redis set. After this, you need to clean out any running tests that haven't died on there own. Then you need to decrement workers.
Future work would expose this via a web endpoint on the pcci web so people can click buttons to destroy.



Redis
-----


```
pcci@planck:~/pcci$ redis-cli
127.0.0.1:6379> get in_progresse
(nil)
127.0.0.1:6379> get in_progress
(error) WRONGTYPE Operation against a key holding the wrong kind of value
127.0.0.1:6379> smembers in_progress
1) "voxpupuli/puppet-corosync/306-centos6"
2) "puppetlabs/puppetlabs-apache/1423-centos7"
3) "voxpupuli/puppet-corosync/301-centos6"
4) "puppetlabs/puppetlabs-mysql/860-centos7"
5) "puppetlabs/puppetlabs-rabbitmq/467-centos7"
6) "puppetlabs/puppetlabs-apache/1423-trusty"
7) "puppetlabs/puppetlabs-apt/601-trusty"
127.0.0.1:6379> srem in_progress voxpupuli/puppet-corosync/306-centos6
(integer) 1
127.0.0.1:6379> smembers in_progress
1) "puppetlabs/puppetlabs-stdlib/607-centos7"
2) "puppetlabs/puppetlabs-stdlib/607-trusty"
3) "puppetlabs/puppetlabs-apache/1423-centos7"
4) "voxpupuli/puppet-corosync/301-centos6"
5) "puppetlabs/puppetlabs-mysql/860-centos7"
6) "puppetlabs/puppetlabs-rabbitmq/467-centos7"
7) "puppetlabs/puppetlabs-apache/1423-trusty"
8) "puppetlabs/puppetlabs-apt/601-trusty"
```



Process Cleanup
---------------

Use 'ps' to find old test runs. In this example no tests have been running for more than a few hours. Usually old test runs that need to be deleted will be days old.

```
pcci@planck:~/pcci$ ps -ef | head -n 1
UID        PID  PPID  C STIME TTY          TIME CMD
pcci@planck:~/pcci$ ps -ef | grep run_test.py
pcci      8794 18418  0 16:48 pts/6    00:00:00 python run_test.py
pcci      8804 18385  0 16:48 pts/5    00:00:00 python run_test.py
pcci      9760 18591  0 17:01 pts/10   00:00:00 python run_test.py
pcci      9770 18269  0 17:01 pts/8    00:00:00 python run_test.py
pcci     10141 18513  0 17:03 pts/12   00:00:00 python run_test.py
pcci     10203  7686  0 17:04 pts/1    00:00:00 grep --color=auto run_test.py
```

Use ``kill`` to abort old jobs.


Redis again
-----------


Set ``workers`` to the correct number of workers.

```
pcci@planck:~/pcci$ redis-cli
127.0.0.1:6379> get workers
"4"
127.0.0.1:6379> set workers 0
OK
```

Note that we only set workers to 0 because there were no tests running, this example was done at a different time than the ps example above.


