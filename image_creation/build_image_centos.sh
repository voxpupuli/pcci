#!/bin/bash
set -x

source venv/bin/activate
export ELEMENTS_PATH=diskimage-builder/elements:custom_elements


export DIB_DISTRIBUTION_MIRROR=http://mirrors.cat.pdx.edu/centos/

export DDD_WORKDIR="$(pwd)/ddd-workdir"
export PATH=$PATH:$DDD_WORKDIR/tools/dib-dev-deploy/scripts
./ddd-workdir/tools/dib-dev-deploy/scripts/ddd-pull-tools

export DIB_DEV_USER_SHELL=/bin/bash
export DIB_DEV_USER_PWDLESS_SUDO=yess
export DIB_DEV_USER_AUTHORIZED_KEYS=/home/nibz/vagrant_key
export DIB_DEV_USER_USERNAME=vagrant
export DIB_DEV_USER_PASSWORD=vagrant
export DIB_DEBUG_TRACE=2

sudo ls


disk-image-create vm centos7 local-config devuser rubygems -a amd64 -o testcentos7 


ddd-define-vm testcentos7 `pwd`/testcentos7.qcow2 
virsh start testcentos7
echo 'sleep 4'
sleep 40
mac=`virsh dumpxml testcentos7 | grep 'mac address' | cut -d "'" -f 2`

ip=`arp -an | grep $mac | egrep -o '[0-9.]+{8,15}'`

ssh -i  vagrant_private.key -o StrictHostKeyChecking=no "vagrant@${ip}"

virsh destroy testcentos7
virsh undefine testcentos7


