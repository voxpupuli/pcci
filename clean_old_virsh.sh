#!/bin/bash

for vm in `virsh list | grep running| awk '{print $2}'`; do
        echo cleaning $vm
        virsh destroy $vm
        virsh undefine $vm
done
