Name:      springbatch-selinux
Version:   #{version}#
Release:   1
Summary:	 SELinux policy module for Springboot batch jobs/tasks
License:	 GPLv2
URL:       https://github.com/hubertqc/selinux_springbatch
Source:    %{name}-%{version}.tar.gz
BuildArch: noarch

Requires:	selinux-policy-devel
Requires:	selinux-policy-targeted
Requires:	policycoreutils
Requires:	make

%description
SELinux policy module to confine Springbatch applications started using systemd.
The systemd service unit name must start with springbatch, the start script must be 
assigned the springbatch_exec_t SELinux type.
The Springbatch application will run in the springbatch_t domain.

%prep
%setup -q

%build

mkdir -p -m 0755 %{buildroot}/usr/share/selinux/packages/targeted
mkdir -p -m 0755 %{buildroot}/usr/share/selinux/devel/include/apps

install -m 0444 se_module/springbatch.if %{buildroot}/usr/share/selinux/devel/include/apps/springbatch.if
cd se_module/ && tar cfvj %{buildroot}/usr/share/selinux/packages/targeted/springbatch.pp.bz2 springbatch.te springbatch.fc

%post
mkdir -m 0700 /tmp/selinux-springbatch
cd /tmp/selinux-springbatch/ && tar xfj /usr/share/selinux/packages/targeted/springbatch.pp.bz2
make -f /usr/share/selinux/devel/Makefile springbatch.pp
semodule -i springbatch.pp
bzip2 springbatch.pp
mv springbatch.pp.bz2 /usr/share/selinux/packages/targeted/
cd /tmp
rm -rf /tmp/selinux-springbatch

%postun
semodule -r springbatch

%files
/usr/share/selinux/devel/include/apps/springbatch.if
%verify(not size filedigest mtime) /usr/share/selinux/packages/targeted/springbatch.pp.bz2

%license LICENSE
%doc    README.md
