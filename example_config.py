# Example configuration file

# Copy this file to config.py with your own values

# Get this token by going to your Github profile settings and generating an
# application key
pccibottoken = 'CHANGEME'

rooturl = 'http://localhost/'

workers = 4

logpath = '/tmp/logs'
build_todo_aggressively = False


commentable = ['puppetlabs/puppetlabs-stdlib',
               'puppetlabs/puppetlabs-mysql']

repos = ['puppetlabs/puppetlabs-stdlib',
         'puppetlabs/puppetlabs-mysql']

nodeset = {}
nodeset['trusty'] = """
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

nodeset['centos7'] = """
HOSTS:
  centos-7-1505-x86_64:
    roles:
      - master
    platform: centos-7-1505-x86_64
    user: 'vagrant'
    password: 'vagrant'
    hypervisor : libvirt
    qcow2: '/home/pcci/sandbox/centosvagrant.qcow2'
    private_key_file: '/home/pcci/.vagrant_private.key'
CONFIG:
  type: foss
"""

