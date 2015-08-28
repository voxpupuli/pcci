#!/bin/bash

for vm in $(virsh list --all | awk '/running|shut/ {print $2}'); do
        echo cleaning "${vm}"
        virsh destroy "${vm}"
        virsh undefine "${vm}"
done
