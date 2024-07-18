Name:		springbatch-systemd
Version:	%{_provided_version}
Release:	%{_provided_release}%{?dist}
Summary:	springbatch systemd units
Vendor:   LHQG, https://www.lhqg.fr/
License:	GPLv3
URL:		https://github.com/lhqg/selinux_springbatch
#Source:	%{name}-%{version}.tar.gz
BuildArch:	noarch

Requires:	systemd
Requires:	springbatch-selinux = %{version}-%{release}

%description
Definitions of systemd units for Springboot batch jobs.

###################################

%clean
%{__rm} -rf %{buildroot}

#%prep
#%setup -q

###################################

%install

mkdir -p -m 0755 %{buildroot}/%{_docdir}/%{name}/examples
mkdir -p -m 0755 %{buildroot}/usr/lib/systemd/system
mkdir -p -m 0755 %{buildroot}/opt/springbatch/bin
mkdir -p -m 0755 %{buildroot}/opt/springbatch/service

install -m 0444 %{_builddir}/systemd/springbatch@.service %{buildroot}/usr/lib/systemd/system/
install -m 0555 %{_builddir}/systemd/springbatch-service.sh %{buildroot}/opt/springbatch/bin/

install -m 0444 %{_builddir}/systemd/env.SAMPLE %{buildroot}/%{_docdir}/%{name}/examples/

###################################

%post

if selinuxenabled
then
  restorecon -Fi /opt/springbatch/bin/springbatch-service.sh
  restorecon -RFi /{lib,etc}/systemd/system/springbatch*
  restorecon -RFi %{_docdir}/%{name}/
fi
  
###################################

%files
%defattr(-,root,root,-)

/usr/lib/systemd/system/springbatch@.service
/opt/springbatch/bin/springbatch-service.sh
  
%dir		%{_docdir}/%{name}
%doc		%{_docdir}/%{name}/examples/env.SAMPLE

