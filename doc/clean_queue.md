Cleaning The Queue
==================


Sometimes jobs crash. When jobs crash they hang out in the in progress section forever, confusing humans and using up worker slots.
To clean the queue, use the ``redis-cli`` utility.
The in progress queue is controlled by the in_progress redis set.
Future work would expose this via a web endpoint on the pcci web so people can click buttons to destroy.


Example:

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

