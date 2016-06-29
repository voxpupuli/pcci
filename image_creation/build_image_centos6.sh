#!/bin/bash
set -x

source venv/bin/activate
export ELEMENTS_PATH=diskimage-builder/elements:custom_elements


export DIB_DISTRIBUTION_MIRROR=http://mirrors.cat.pdx.edu/centos/

export DDD_WORKDIR="$(pwd)/ddd-workdir"
export PATH=$PATH:${DDD_WORKDIR}/tools/dib-dev-deploy/scripts
${DDD_WORKDIR}/tools/dib-dev-deploy/scripts/ddd-pull-tools

export DIB_DEV_USER_SHELL=/bin/bash
export DIB_DEV_USER_PWDLESS_SUDO=yess
export DIB_DEV_USER_AUTHORIZED_KEYS=/home/nibz/vagrant_key
export DIB_DEV_USER_USERNAME=vagrant
export DIB_DEV_USER_PASSWORD=vagrant
export DIB_DEBUG_TRACE=2

export EXTRA_PACKAGES='rubygems,ruby,augeas,ruby-augeas'

sudo ls # just to make sure sudo is hot

disk-image-create vm centos local-config devuser -a amd64 -o testcentos6 -p ${EXTRA_PACKAGES}
