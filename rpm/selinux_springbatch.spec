Name:      springbatch-selinux
Version:   %{_provided_version}
Release:   %{_provided_release}%{?dist}
Summary:	 SELinux policy module for Springboot batch jobs/tasks
Vendor:   LHQG, https://www.lhqg.fr/
License:	GPLv3
URL:       https://github.com/lhqg/selinux_springbatch
#Source:    %{name}-%{version}.tar.gz
BuildArch: noarch

BuildRequires:	selinux-policy-devel
BuildRequires:	make

Requires:	selinux-policy-targeted %{?_sepol_minver_cond}
Requires:	selinux-policy-targeted %{?_sepol_maxver_cond}

Requires:	policycoreutils
Requires:	policycoreutils-python-utils
Requires:	libselinux-utils

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
mkdir -p -m 0755 %{buildroot}/%{_docdir}/%{name}
mkdir -p -m 0755 %{buildroot}/%{_datarootdir}/%{name}

install -m 0555 %{_builddir}/scripts/* %{buildroot}/%{_datarootdir}/%{name}/
install -m 0444 %{_builddir}/springbatch.pp %{buildroot}/usr/share/selinux/packages/targeted/
install -m 0444 %{_builddir}/{LICENSE,README.md} %{buildroot}/%{_docdir}/%{name}/

###################################

%post

semodule -i /usr/share/selinux/packages/targeted/springbatch.pp

if selinuxenabled
then
  restorecon -RFi /{opt,srv}/springbatch 
  restorecon -RFi /{lib,etc}/systemd/system/springbatch*
  restorecon -RFi /var/{lib,log,run,tmp}/springbatch
fi

###################################

%postun

if [ $1 -eq 0 ]
then
  semodule -r springbatch
fi

###################################

%files
%defattr(-,root,root,-)

/usr/share/selinux/packages/targeted/springbatch.pp

%dir	%{_datarootdir}/%{name}
%{_datarootdir}/%{name}/*

%dir		%{_docdir}/%{name}
%license 	%{_docdir}/%{name}/LICENSE
%doc		%{_docdir}/%{name}/README.md