#!/bin/bash
#########################################################
#														#
#			SELinux Springbatch policy module			#
#														#
#	Restore fcontext script:							#
#		This script restores SELinux fcontexts.			#
#														#
#    https://github.com/hubertqc/selinux_springbatch		#
#														#
#########################################################

typset -i RC
RC=0

if selinuxenabled
then
  restorecon -RFi /{opt,srv}/springbatch 
  restorecon -RFi /{lib,etc}/systemd/system/springbatch*
  restorecon -RFi /var/{lib,log,run,tmp}/springbatch
else
	echo "SElinux is not enabled, unable to restore fcontext."
	RC=1
fi

exit $RC