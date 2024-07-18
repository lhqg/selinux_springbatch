Name:		springbatch-selinux-devel
Version:	%{_provided_version}
Release:	%{_provided_release}%{?dist}
Summary:	SELinux policy module for Springboot batch jobs/tasks - devel
Vendor:   LHQG, https://www.lhqg.fr/
License:	GPLv3
URL:		https://github.com/lhqg/selinux_springbatch
#Source:	%{name}-%{version}.tar.gz
BuildArch:	noarch

Requires:	selinux-policy-devel
Requires:	springbatch-selinux = %{version}-%{release}

%description
SELinux policy development interface for Springbatch policy module.

###################################

%clean
%{__rm} -rf %{buildroot}

#%prep
#%setup -q

###################################

%install

mkdir -p -m 0755 %{buildroot}/usr/share/selinux/devel/include/apps
install -m 0444 %{_builddir}/se_module/springbatch.if %{buildroot}/usr/share/selinux/devel/include/apps/

###################################

%files
%defattr(-,root,root,-)

/usr/share/selinux/devel/include/apps/springbatch.if