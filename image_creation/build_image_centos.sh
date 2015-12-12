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


ddd-define-vm testcentos7 "$(pwd)/testcentos7.qcow2"
virsh start testcentos7
echo 'sleep 4'
sleep 40
mac=$(virsh domiflist testcentos7 | grep -oE "([0-9a-f]{2}:){5}[0-9a-f]{2}")

ip_addr=$(ip -4 n | awk -v mac="$mac" '$0 ~ mac {print $1}')

ssh -i  vagrant_private.key -o StrictHostKeyChecking=no "vagrant@${ip_addr}"

virsh destroy testcentos7
virsh undefine testcentos7


