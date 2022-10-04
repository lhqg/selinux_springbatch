Name:      springbatch-selinux
Version:   %{provided_version}
Release:   %{provided_release}%{?dist}
Summary:	 SELinux policy module for Springboot batch jobs/tasks
License:	 GPLv2
URL:       https://github.com/hubertqc/selinux_springbatch
#Source:    %{name}-%{version}.tar.gz
BuildArch: noarch

Requires:	selinux-policy-devel
Requires:	selinux-policy-targeted
Requires:	policycoreutils
Requires:	make

%description
SELinux policy module to confine Springbatch applications started using systemd.
The systemd service unit name must start with springbatch, the start script must be 
assigned the springbatch_exec_t SELinux type.
The Springboot batch job will run in the springbatch_t domain.

###################################

%clean
%{__rm} -rf %{buildroot}

#%prep
#%setup -q

###################################

%build

make -f /usr/share/selinux/devel/Makefile -C %{_builddir} springbatch.pp

###################################

%install

mkdir -p -m 0755 %{buildroot}/usr/share/selinux/packages/targeted
mkdir -p -m 0755 %{buildroot}/usr/share/selinux/devel/include/apps
mkdir -p -m 0755 %{buildroot}/%{_docdir}/%{name}

install -m 0444 %{_builddir}/se_module/springbatch.if %{buildroot}/usr/share/selinux/devel/include/apps/

bzip2 %{_builddir}/springbatch.pp
install -m 0444 %{_builddir}/springbatch.pp.bz2 %{buildroot}/usr/share/selinux/packages/targeted/

install -m 0444 %{_builddir}/{LICENSE,README.md} %{buildroot}/%{_docdir}/%{name}/

###################################

%post

mkdir -m 0700 /tmp/selinux-springbatch
bzcat -dc /usr/share/selinux/packages/targeted/springbatch.pp.bz2 > /tmp/selinux-springbatch/springbatch.pp
semodule -i /tmp/selinux-springbatch/springbatch.pp
rm -rf /tmp/selinux-springbatch

###################################

%postun

if [ $1 -eq 0 ]
then
  semodule -r springbatch
fi

###################################

%files
%defattr(-,root,root,-)

/usr/share/selinux/devel/include/apps/springbatch.if
/usr/share/selinux/packages/targeted/springbatch.pp.bz2
%license  %{_docdir}/%{name}/LICENSE
%doc      %{_docdir}/%{name}/README.md
