SELinux policy module for Springboot batch jobs
==========================================================
https://github.com/hubertqc/selinux_springbatch

## Introduction

This SELinux policy module aims to prevent a Springboot batch job/task to perform 
unexpected actions on a Linux host.

It should be used when the Springboot batch is possibly exposed to a world full of
 *bad guys*.

The module should prevent the batch from going rogue, and should the batch be compromised 
by an attacker this SELinux policy module should help limit the damage on the system on 
which the Springboot batch is running.

When used correctly, this SELinux policy module will make the Springboot batch jobs(s)
run on the host in the dedicated `springbatch_t` SELinux domain.

## How to use this SELinux module

Once the SELinux policy module is compiled and installed in the running Kernel SELinux
 policy, a few actions must be taken for the new policy to apply to the Springboot
 batch jobs/tasks.
 
The policy can be adjusted with a handfull of SELinux booleans.

### Filesystem labelling
This SELinux policy module SELinux file context definitions are based on the Filesystem 
Hierarchy Standards [https://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard].

The root for the Springboot batch installation is expected to be /opt/springbatch.
The root for log files of the Springboot batch jobs/tasks is expected to be
 /var/log/springbatch.

A typical directory layout for the Springboot batch `my_job` would be:

```
/opt/springbatch/my_job
                      \ conf
                      \ lib
                      \ keys
                      
/var/log/springbatch/my_job

/var/run/springbatch/my_job

/srv/springbatch/my_job
                      \ cache
                      \ work
                      \ dynlib
                      
```

Files with `.so` and `.jar` extensions under the /opt/springbatch and /srv/springbatch 
trees will be assigned the *Springbatch library* SELinux type.

Files with `.jks`, `.jceks`, `.p12` or `.pkcs12`extensions placed in a `conf`or
`properties` directory under /opt/springbatch will be assigned the *Springbatch 
authentication/credentials* SELinux type. All files located in a `keys`directory under
 /opt/springbatch will be assigned the same SELinux type.


Should you prefer to used a different directory structure, you should consider using
SELinux fcontext equivalence rules to map your specifics to the filesystem layout expected
in the policy module, using the `semanage fcontext -a -e ORIGINAL CUSTOMISATION` command.

### Networking

#### Services consumed by the Springboot application
If the batch job needs to connect to services such as databases, directory servers, ...
the SELinux type of these services network port must be allowed for the Springboot
application to connect to.
One of the `springbatch_allow_connectto` or `springbatch_allow_consumed_service` interfaces
should be used with the prefix name for the service as the only argument.

Examples:
- `springbatch_allow_connectto(postgresql)` to allow the Springboot batch job to connect to a PostgreSQL database
- `springbatch_allow_connectto(ldap)` to allow connection to LDAP directory services.

### SELinux booleans

#### allow_springbatch_purge_logs		(default: `false`)
When switched to `true`n, this boolean allows the Springboot batch job to delete its log
files. It can be useful for log file rotation, but it can also be useful for attackers who
would like to clean after themselves and remove traces of their actions...

#### allow_webadm_read_springbatch_files		(default: `false`)
Users running with the `webadm_r`SELinux role and`webadm_t`domain are granted the
permissions to browse the directories of the Springboot batch job and the permission to
stop and start the Springboot batch job **systemd** services, as well as querying their
status.

When switched to `true`, this boolean allows such users additional permissions to read the 
contents of Springboot application files: log, configuration, temp and transient/cache
files.

#### allow_sysadm_write_springbatch_files	(default: `false`)
When switched to `true`, this boolean allows users running with the `sysadm_r`SELinux role
and`sysadm_t`domain to:
- fully manage temporary files,
- delete and rename log files,
- delete and rename transient/cache files,
- modify the contents of configuration files,

Otherwise, such users are only granted read permissions on all Springboot batch jobs
files, except authentication/credentials files.
 

### Starting the Springboot batch jobs/tasks

The Springboot batch jobs should always and ony be started as a **systemd** service using
the`systemctl` command.

The service or target unit files MUST be located in /etc/systemd/system or in
/lib/systemd/system, the file name MUST start with `springbatch`.
Directories to tune or override unit behaviour are supported.
Template/instantiated units are supported provided the master file is named
`springbatch@.service`.

The script(s) used to start or stop the Springboot batch MUST be located in the 
/opt/springbatch/service/ directory. The /opt/springbatch/bin/springbatch_service file name
is also supported.

### Running multiple Springboot batch jobs/tasks on the same host

TO DO


## Disclaimer

The code of the this SELinux policy module is provided AS-IS. People and organisation
willing to use it must be fully aware that they are doing so at their own risks and
expenses.

The Author(s) of this SELinux policy module SHALL NOT be held liable nor accountable, in
 any way, of any malfunction or limitation of said module, nor of the resulting damage, of
 any kind, resulting, directly or indirectly, of the usage of this SELinux policy module.

It is strongly advised to always use the last version of the code, to check for the 
compatibility of the platform where it is about to be deployed, to compile the module on
the target specific Linux distribution and version where it is intended to be used.

Finally, users should check regularly for updates.
