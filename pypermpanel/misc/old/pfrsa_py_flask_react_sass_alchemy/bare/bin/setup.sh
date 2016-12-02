#!/bin/bash

#vagrant
vag_dw_ver='1.8.7'
vag_dw_file="vagrant_${vag_dw_ver}_x86_64.deb"
vag_dw_url="https://releases.hashicorp.com/vagrant/${vag_dw_ver}/${vag_dw_file}"

mkdir tmp; cd tmp; wget $vag_dw_url; dpkg -i $vag_dw_file
#; chmod u+x $vag_dw_file
