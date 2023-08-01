Summary: Applies updates and reboots a RHEL machine if needed
Name: autoupdater
Version: 1.0
Release: 1%{?dist}
License: GPLv2
URL: https://nux.se/
Source0: autoupdater
Source1: autoupdater.conf
Source2: autoupdater.cron
Requires: dnf-automatic yum-utils
BuildArch: noarch

%description
This package automatically applies updates and reboots a RHEL machine if needed.

Requires the following packages:

* dnf-automatic
* yum-utils

%prep

%setup -c -T
cp %{SOURCE0} .
cp %{SOURCE1} .
cp %{SOURCE2} .

%build

%install
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_sysconfdir}/cron.daily

install -m0755 autoupdater %{buildroot}%{_bindir}/autoupdater
install -m0644 autoupdater.conf %{buildroot}%{_sysconfdir}/autoupdater.conf
install -m0644 autoupdater.cron %{buildroot}%{_sysconfdir}/cron.daily/autoupdater

%post
if [ $1 = "1" ]; then
    sed -i 's|^apply_updates.*|apply_updates = yes|g' %{_sysconfdir}/dnf/automatic.conf || :
    sed -i 's|^emit_via.*|emit_via = stdio|g' %{_sysconfdir}/dnf/automatic.conf || :
    systemctl enable dnf-automatic.timer || :
    systemctl start dnf-automatic.timer || :
fi

%preun
if [ $1 = "0" ]; then
    systemctl stop dnf-automatic.timer || :
    systemctl disable dnf-automatic.timer || :
fi

%files
%config(noreplace) %{_sysconfdir}/autoupdater.conf
%{_sysconfdir}/cron.daily/autoupdater
%{_bindir}/autoupdater

%changelog
* Tue Aug 01 2023 Oden Eriksson <oe@nux.se> - 1.0-1
- initial package
