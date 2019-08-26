#!/bin/bash

set -ex

prep() {
    yum -y update
    yum -y install epel-release
    yum -y install python36 python36-virtualenv which libarchive
    yum -y install gcc git
}

prep
./qa/runtests.sh
