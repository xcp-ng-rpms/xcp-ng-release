# XCP-ng: TO BE UPDATED FOR EACH NEW RELEASE
# TODO: use data from branding file instead
%define PRODUCT_VERSION 8.0.0
%define PRODUCT_VERSION_TEXT 8.0
%define PRODUCT_VERSION_TEXT_SHORT %{PRODUCT_VERSION_TEXT}
%define PLATFORM_VERSION 3.0.0
%define BUILD_NUMBER release/naples/master/45

%define debug_package %{nil}
%define product_family CentOS Linux
%define variant_titlecase Server
%define variant_lowercase server
%define release_name Core
%define base_release_version 7
%define full_release_version 7
%define dist_release_version 7
%define upstream_rel_long 7.5-8
%define upstream_rel 7.5
%define centos_rel 5.1804
#define beta Beta
%define dist .xcpng%{PRODUCT_VERSION_TEXT_SHORT}

%define _unitdir /usr/lib/systemd/system

Name:           xcp-ng-release
Version:        8.0.0
Release:        7
Summary:        XCP-ng release file
Group:          System Environment/Base
License:        GPLv2
Requires:       coreutils, grep
Provides:       centos-release = %{base_release_version}
Provides:       centos-release(upstream) = %{upstream_rel}
Provides:       redhat-release = %{upstream_rel_long}
Provides:       system-release = %{upstream_rel_long}
Provides:       system-release(releasever) = %{base_release_version}
Obsoletes:      centos-release
Obsoletes:      xenserver-release <= %{version}

#Obsolete XS74+XS75 hotfixes
Obsoletes:      update-XS74 control-XS74
Obsoletes:      update-XS74E001 control-XS74E001
Obsoletes:      update-XS74E002 control-XS74E002
Obsoletes:      update-XS74E003 control-XS74E003
Obsoletes:      update-XS75 control-XS75
Obsoletes:      update-XS75E001 control-XS75E001

# Metadata for the installer to consume
Provides:       product-brand = XCP-ng
Provides:       product-version = %{PRODUCT_VERSION}
Provides:       product-build = 0x
Provides:       platform-name = XCP
Provides:       platform-version = %{PLATFORM_VERSION}
Provides:       product-version-text = %{PRODUCT_VERSION_TEXT}
Provides:       product-version-text-short = %{PRODUCT_VERSION_TEXT_SHORT}

BuildRequires:  systemd branding-xcp-ng
URL:            https://github.com/xcp-ng/xcp-ng-release
Source0:        https://github.com/xcp-ng/xcp-ng-release/archive/v%{version}/xcp-ng-release-%{version}.tar.gz


Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XS/repos/xenserver-release/archive?at=v8.0.0-2&format=tar.gz&prefix=xenserver-release-8.0.0#/xenserver-release.tar.gz) = 63ae7f04d1fa2f89d65262ad1826301c9b4b2e1c


%description
XCP-ng release files


%package        config
Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XS/repos/xenserver-release/archive?at=v8.0.0-2&format=tar.gz&prefix=xenserver-release-8.0.0#/xenserver-release.tar.gz) = 63ae7f04d1fa2f89d65262ad1826301c9b4b2e1c
Summary:        XCP-ng configuration
Group:          System Environment/Base
Requires:       grep sed coreutils patch systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires(post): sed
Obsoletes:      xenserver-release-config <= %{version}

%description    config
Additional utilities and configuration for XCP-ng.


%prep
%autosetup -p1

%build

%install
rm -rf %{buildroot}

%{_usrsrc}/branding/brand-directory.py /usr/src/branding/branding src/common %{buildroot}
%{_usrsrc}/branding/brand-directory.py /usr/src/branding/branding src/xenserver %{buildroot}
install -d -m 755 %{buildroot}%{python_sitelib}/xcp
%{_usrsrc}/branding/branding-compile.py --format=python > %{buildroot}%{python_sitelib}/xcp/branding.py

# create /etc/system-release and /etc/redhat-release
ln -s centos-release %{buildroot}%{_sysconfdir}/system-release
ln -s centos-release %{buildroot}%{_sysconfdir}/redhat-release

# create /etc/issue from /etc/issue.net
cp %{buildroot}%{_sysconfdir}/issue.net %{buildroot}%{_sysconfdir}/issue
echo >> %{buildroot}%{_sysconfdir}/issue
touch -r %{buildroot}%{_sysconfdir}/issue.net %{buildroot}%{_sysconfdir}/issue

# copy yum repos
install -d -m 755 %{buildroot}%{_sysconfdir}/yum.repos.d
# Use the production yum repos
install -m 644 CentOS-Base-production.repo %{buildroot}%{_sysconfdir}/yum.repos.d/CentOS-Base.repo
#install -m 644 CentOS-Base-devel.repo %{buildroot}%{_sysconfdir}/yum.repos.d/CentOS-Base.repo
install -m 644 CentOS-Debuginfo.repo %{buildroot}%{_sysconfdir}/yum.repos.d
install -m 644 CentOS-Sources.repo %{buildroot}%{_sysconfdir}/yum.repos.d
# install the xcp-ng repo
install -m 644 xcp-ng.repo %{buildroot}%{_sysconfdir}/yum.repos.d

# set up the dist tag macros
install -d -m 755 %{buildroot}%{_sysconfdir}/rpm
cat >> %{buildroot}%{_sysconfdir}/rpm/macros.dist << EOF
# dist macros.

%%centos_ver %{base_release_version}
%%centos %{base_release_version}
%%rhel %{base_release_version}
%%dist %dist
%%el%{base_release_version} 1
EOF

# use unbranded datadir
install -d -m 755 %{buildroot}/%{_datadir}/centos-release
ln -s centos-release %{buildroot}/%{_datadir}/redhat-release

# use unbranded docdir
install -d -m 755 %{buildroot}/%{_docdir}/centos-release
ln -s centos-release %{buildroot}/%{_docdir}/redhat-release

# Prevent spawning gettys on tty1 and tty2
mkdir -p %{buildroot}%{_sysconfdir}/systemd/system
ln -s /dev/null %{buildroot}%{_sysconfdir}/systemd/system/getty@tty1.service
ln -s /dev/null %{buildroot}%{_sysconfdir}/systemd/system/getty@tty2.service
ln -s /dev/null %{buildroot}%{_sysconfdir}/systemd/system/autovt@tty1.service
ln -s /dev/null %{buildroot}%{_sysconfdir}/systemd/system/autovt@tty2.service

ln -s XCP-ng-index.html %{buildroot}/opt/xensource/www/index.html

%post
/usr/bin/uname -m | grep -q 'x86_64'  && echo 'centos' >/etc/yum/vars/contentdir || echo 'altarch' > /etc/yum/vars/contentdir

%clean
rm -rf %{buildroot}

%triggerin config -- mcelog

( patch -tsN -r - -d / -p1 || : ) >/dev/null <<'EOF'
--- /etc/mcelog/mcelog.conf	2014-01-22 00:03:35.000000000 +0000
+++ /etc/mcelog/mcelog.conf	2014-11-13 13:49:57.152247000 +0000
@@ -22,7 +22,7 @@

 [dimm]
 # Enable DIMM-tracking
-dimm-tracking-enabled = yes
+dimm-tracking-enabled = no
 # Disable DIMM DMI pre-population unless supported on your system
 dmi-prepopulate = no

@@ -35,23 +35,23 @@

 [socket]
 # Memory error accounting per socket
-socket-tracing-enabled = yes
+socket-tracing-enabled = no
 mem-uc-error-threshold = 100 / 24h
-mem-ce-error-trigger = socket-memory-error-trigger
-mem-ce-error-threshold = 100 / 24h
-mem-ce-error-log = yes
+#mem-ce-error-trigger = socket-memory-error-trigger
+#mem-ce-error-threshold = 100 / 24h
+#mem-ce-error-log = yes

 [cache]
 # Attempt to off-line CPUs causing cache errors
-cache-threshold-trigger = cache-error-trigger
-cache-threshold-log = yes
+#cache-threshold-trigger = cache-error-trigger
+#cache-threshold-log = yes

 [page]
 # Try to soft-offline a 4K page if it exceeds the threshold
 memory-ce-threshold = 10 / 24h
 memory-ce-trigger = page-error-trigger
 memory-ce-log = yes
-memory-ce-action = soft
+memory-ce-action = account

 [trigger]
 # Maximum number of running triggers
EOF

%triggerin config -- rsyslog
( patch -tsN -r - -d / -p1 || : ) >/dev/null <<'EOF'
--- /etc/rsyslog.conf	2014-11-12 13:55:42.000000000 +0000
+++ /etc/rsyslog.conf	2014-11-12 13:56:01.000000000 +0000
@@ -7,8 +7,8 @@

 # The imjournal module bellow is now used as a message source instead of imuxsock.
 $ModLoad imuxsock # provides support for local system logging (e.g. via logger command)
-$ModLoad imjournal # provides access to the systemd journal
-#$ModLoad imklog # reads kernel messages (the same are read from journald)
+#$ModLoad imjournal # provides access to the systemd journal
+$ModLoad imklog # reads kernel messages (the same are read from journald)
 #$ModLoad immark  # provides --MARK-- message capability

 # Provides UDP syslog reception
@@ -37,10 +37,10 @@

 # Turn off message reception via local log socket;
 # local messages are retrieved through imjournal now.
-$OmitLocalLogging on
+#$OmitLocalLogging on

 # File to store the position in the journal
-$IMJournalStateFile imjournal.state
+#$IMJournalStateFile imjournal.state


 #### RULES ####
EOF

%triggerin config -- openssh-server
( patch -tsN -r - -d / -p1 || : ) >/dev/null <<'EOF'
--- /etc/ssh/sshd_config	2010-03-31 10:24:13.000000000 +0100
+++ /etc/ssh/sshd_config	2010-09-03 16:08:27.000000000 +0100
--- /etc/ssh/sshd_config.orig   2016-01-22 14:23:59.000000000 +0000
+++ /etc/ssh/sshd_config    2016-01-22 15:50:45.000000000 +0000
@@ -90,7 +90,7 @@
 #KerberosUseKuserok yes

 # GSSAPI options
-GSSAPIAuthentication yes
+GSSAPIAuthentication no
 GSSAPICleanupCredentials no
 #GSSAPIStrictAcceptorCheck yes
 #GSSAPIKeyExchange no
EOF

%triggerin config -- net-snmp
grep -qs '^OPTIONS' %{_sysconfdir}/sysconfig/snmpd || echo 'OPTIONS="-c %{_sysconfdir}/snmp/snmpd.xs.conf"' >>%{_sysconfdir}/sysconfig/snmpd

%triggerun config -- net-snmp
if [ $1 -eq 0 ]; then
  if [ -e %{_sysconfdir}/sysconfig/snmpd ]; then
    sed -i -e '\#%{_sysconfdir}/snmp/snmpd.xs.conf# d' %{_sysconfdir}/sysconfig/snmpd
  fi
fi

%triggerin config -- logrotate
( patch -tsN -r - -d / -p1 || : ) >/dev/null <<'EOF'
--- /etc/logrotate.conf   2013-07-31 12:46:23.000000000 +0100
+++ /etc/logrotate.conf   2015-08-06 11:47:36.000000000 +0100
@@ -1,18 +1,16 @@
 # see "man logrotate" for details
-# rotate log files weekly
-weekly
+# rotate log files daily
+daily

-# keep 4 weeks worth of backlogs
-rotate 4
+# keep one months worth of backlogs
+rotate 31

 # create new (empty) log files after rotating old ones
 create

-# use date as a suffix of the rotated file
-dateext
-
-# uncomment this if you want your log files compressed
-#compress
+# compress log files
+compress
+delaycompress

 # RPM packages drop log rotation information into this directory
 include /etc/logrotate.d
EOF

%triggerin config -- iscsi-initiator-utils
/usr/bin/systemctl -q disable iscsi.service
/usr/bin/systemctl -q disable iscsid.socket

%triggerin config -- iscsi-initiator-utils-iscsiuio
/usr/bin/systemctl -q disable iscsiuio.socket

%triggerin config -- xcp-networkd
/sbin/chkconfig network off

%triggerin config -- lvm2
/usr/bin/systemctl -q mask lvm2-activation.service
/usr/bin/systemctl -q mask lvm2-activation-early.service
/usr/bin/systemctl -q mask lvm2-activation-net.service
/usr/bin/systemctl -q disable lvm2-monitor.service

%triggerin config -- device-mapper-event
/usr/bin/systemctl -q disable dm-event.socket

%triggerin config -- elxocmcore
/usr/bin/systemctl -q disable elxhbamgr.service
/usr/bin/systemctl -q disable elxsnmp.service

# default firewall rules, to be replaced by dynamic rule addition/removal
%triggerin config -- iptables-services
( patch -tsN -r - -d / -p1 || : ) >/dev/null <<'EOF'
--- /etc/sysconfig/iptables	2014-06-10 06:02:35.000000000 +0100
+++ /etc/sysconfig/iptables	2015-05-15 11:24:23.712024801 +0100
@@ -5,10 +5,21 @@
 :INPUT ACCEPT [0:0]
 :FORWARD ACCEPT [0:0]
 :OUTPUT ACCEPT [0:0]
--A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
--A INPUT -p icmp -j ACCEPT
--A INPUT -i lo -j ACCEPT
--A INPUT -p tcp -m state --state NEW -m tcp --dport 22 -j ACCEPT
--A INPUT -j REJECT --reject-with icmp-host-prohibited
--A FORWARD -j REJECT --reject-with icmp-host-prohibited
+:RH-Firewall-1-INPUT - [0:0]
+-A INPUT -j RH-Firewall-1-INPUT
+-A FORWARD -j RH-Firewall-1-INPUT
+-A RH-Firewall-1-INPUT -i lo -j ACCEPT
+-A RH-Firewall-1-INPUT -p icmp --icmp-type any -j ACCEPT
+# DHCP for host internal networks (CA-6996)
+-A RH-Firewall-1-INPUT -p udp -m udp --dport 67 --in-interface xenapi -j ACCEPT
+-A RH-Firewall-1-INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
+# Linux HA hearbeat (CA-9394)
+-A RH-Firewall-1-INPUT -m conntrack --ctstate NEW -m udp -p udp --dport 694 -j ACCEPT
+-A RH-Firewall-1-INPUT -m conntrack --ctstate NEW -m tcp -p tcp --dport 22 -j ACCEPT
+-A RH-Firewall-1-INPUT -m conntrack --ctstate NEW -m tcp -p tcp --dport 80 -j ACCEPT
+-A RH-Firewall-1-INPUT -m conntrack --ctstate NEW -m tcp -p tcp --dport 443 -j ACCEPT
+# dlm
+-A RH-Firewall-1-INPUT -p tcp -m tcp --dport 21064 -j ACCEPT
+-A RH-Firewall-1-INPUT -p udp -m multiport --dports 5404,5405 -j ACCEPT
+-A RH-Firewall-1-INPUT -j REJECT --reject-with icmp-host-prohibited
 COMMIT
EOF
( patch -tsN -r - -d / -p1 || : ) >/dev/null <<'EOF'
--- /etc/sysconfig/ip6tables	2014-06-10 06:02:35.000000000 +0100
+++ /etc/sysconfig/ip6tables	2015-05-15 11:25:34.416370193 +0100
@@ -5,11 +5,21 @@
 :INPUT ACCEPT [0:0]
 :FORWARD ACCEPT [0:0]
 :OUTPUT ACCEPT [0:0]
--A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
--A INPUT -p ipv6-icmp -j ACCEPT
--A INPUT -i lo -j ACCEPT
--A INPUT -p tcp -m state --state NEW -m tcp --dport 22 -j ACCEPT
--A INPUT -d fe80::/64 -p udp -m udp --dport 546 -m state --state NEW -j ACCEPT
--A INPUT -j REJECT --reject-with icmp6-adm-prohibited
--A FORWARD -j REJECT --reject-with icmp6-adm-prohibited
+:RH-Firewall-1-INPUT - [0:0]
+-A INPUT -j RH-Firewall-1-INPUT
+-A FORWARD -j RH-Firewall-1-INPUT
+-A RH-Firewall-1-INPUT -i lo -j ACCEPT
+-A RH-Firewall-1-INPUT -p icmpv6 -j ACCEPT
+# DHCP for host internal networks (CA-6996)
+-A RH-Firewall-1-INPUT -p udp -m udp --dport 67 --in-interface xenapi -j ACCEPT
+-A RH-Firewall-1-INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
+# Linux HA hearbeat (CA-9394)
+-A RH-Firewall-1-INPUT -m state --state NEW -m udp -p udp --dport 694 -j ACCEPT
+-A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp --dport 22 -j ACCEPT
+-A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp --dport 80 -j ACCEPT
+-A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp --dport 443 -j ACCEPT
+# dlm
+-A RH-Firewall-1-INPUT -p tcp -m tcp --dport 21064 -j ACCEPT
+-A RH-Firewall-1-INPUT -p udp -m multiport --dports 5404,5405 -j ACCEPT
+-A RH-Firewall-1-INPUT -j REJECT --reject-with icmp6-port-unreachable
 COMMIT
EOF

# CA-38350
%triggerin config -- dhclient
( patch -tsN -r - -d / -p1 || : ) >/dev/null <<'EOF'
--- /usr/sbin/dhclient-script	2015-11-19 21:28:36.000000000 +0000
+++ /usr/sbin/dhclient-script	2016-01-22 17:15:09.000000000 +0000
@@ -790,6 +790,8 @@
             fi

             flush_dev ${interface}
+            # Remove IP address but leave up so that subsequent DHCPDISCOVERs are not dropped
+            ip link set $interface up
             exit_with_hooks 1
         else
             exit_with_hooks 1
EOF

%triggerin config -- smartmontools
( patch -tsN -r - -d / -p1 || : ) >/dev/null <<'EOF'
--- /etc/smartmontools/smartd.conf.orig	2015-09-24 09:13:05.000000000 +0100
+++ /etc/smartmontools/smartd.conf	2015-09-24 09:12:19.000000000 +0100
@@ -20,7 +20,7 @@
 # Directives listed below, which will be applied to all devices that
 # are found.  Most users should comment out DEVICESCAN and explicitly
 # list the devices that they wish to monitor.
-DEVICESCAN -H -m root -M exec /usr/libexec/smartmontools/smartdnotify -n standby,10,q
+DEVICESCAN -H -n standby,10,q

 # Alternative setting to ignore temperature and power-on hours reports
 # in syslog.
EOF

%triggerin config -- tzdata
ln -f %{_datadir}/zoneinfo/Asia/Shanghai %{_datadir}/zoneinfo/Asia/Beijing

%triggerin config -- ntpdate
( patch -tsN -r - -d / -p1 || : ) >/dev/null <<'EOF'
--- /etc/sysconfig/ntpdate.orig 2015-11-19 21:46:56.000000000 +0000
+++ /etc/sysconfig/ntpdate  2016-01-22 14:23:25.000000000 +0000
@@ -2,7 +2,7 @@
 OPTIONS="-p 2"

 # Number of retries before giving up
-RETRIES=2
+RETRIES=3

 # Set to 'yes' to sync hw clock after successful ntpdate
 SYNC_HWCLOCK=no
EOF

%triggerin config -- shadow-utils
( patch -tsN -r - -d / -p1 || : ) >/dev/null <<'EOF'
--- /etc/login.defs.orig    2016-02-26 11:11:20.000000000 +0000
+++ /etc/login.defs 2016-02-26 11:11:57.000000000 +0000
@@ -70,3 +70,4 @@
 # Use SHA512 to encrypt password.
 ENCRYPT_METHOD SHA512

+MOTD_FILE /etc/motd.xs
EOF

%triggerin config -- yum
( patch -tsN -r - -d / -p1 || : ) >/dev/null <<'EOF'
--- /etc/yum.conf.orig  2016-11-07 09:39:42.594325044 +0000
+++ /etc/yum.conf   2016-11-07 09:39:58.478743042 +0000
@@ -7,6 +7,7 @@
 obsoletes=1
 gpgcheck=1
 plugins=1
+installonlypkgs=
 installonly_limit=5
 bugtracker_url=http://bugs.centos.org/set_project.php?project_id=23&ref=http://bugs.centos.org/bug_report_page.php?category=yum
 distroverpkg=centos-release
EOF

# XCP-ng: change depmod global configuration to give priority to 'override' modules dir
%triggerin config -- kmod
DEPMOD_PATCH=$(cat <<'EOF'
--- /etc/depmod.d/dist.conf.orig        2019-04-23 11:31:19.107096410 +0200
+++ /etc/depmod.d/dist.conf     2019-04-23 11:31:30.533088996 +0200
@@ -3,4 +3,4 @@
 #

 # override default search ordering for kmod packaging
-search updates extra built-in weak-updates
+search override updates extra built-in weak-updates
EOF
)
# Do not apply patch if it was already applied
if ! echo "$DEPMOD_PATCH" | patch --dry-run -RsN -d / -p1 >/dev/null; then
    # Apply patch. Output NOT redirected to /dev/null so that error messages are displayed
    if ! echo "$DEPMOD_PATCH" | patch -tsN -r - -d / -p1; then
        echo "Error: failed to patch /etc/depmod.d/dist.conf"
    fi
fi

## Comment out hotfix hiding logic until it is needed again
## Hide previous 7.4+7.5 hotfixes from xapi
#%%triggerun config -- %%{name}-config = 7.4.0, %%{name}-config = 7.5.0
#if [ -d /var/update/applied ]; then
#    shopt -s nullglob
#    for sfile in /var/update/applied/*; do
#        label=$(xmllint --xpath "string(//update/@name-label)" $sfile)
#        if [[ "$label" =~ ^XS7[45](E[0-9]{3}$|$) ]]; then
#            rm -f $sfile
#        fi
#    done
#fi

%post config
%systemd_post move-kernel-messages.service
%systemd_post update-issue.service
%systemd_post xs-fcoe.service

if [ -f %{_sysconfdir}/xensource-inventory ]; then
    sed -i \
        -e "s@^\(PRODUCT_VERSION=\).*@\1'%{PRODUCT_VERSION}'@" \
        -e "s@^\(PLATFORM_VERSION=\).*@\1'%{PLATFORM_VERSION}'@" \
        -e "s@^\(PRODUCT_VERSION_TEXT=\).*@\1'%{PRODUCT_VERSION_TEXT}'@" \
        -e "s@^\(PRODUCT_VERSION_TEXT_SHORT=\).*@\1'%{PRODUCT_VERSION_TEXT_SHORT}'@" \
        -e "s@^\(BUILD_NUMBER=\).*@\1'%{BUILD_NUMBER}'@" \
        %{_sysconfdir}/xensource-inventory
fi


%preun config
%systemd_preun move-kernel-messages.service
%systemd_preun update-issue.service
%systemd_preun xs-fcoe.service


%postun config
%systemd_postun move-kernel-messages.service
%systemd_postun update-issue.service
%systemd_postun xs-fcoe.service

%triggerpostun config -- xenserver-release-config < 7.5
# To be reviewed at each release to make sure the fixes are still valid.
# Fix upgrade from XCP-ng 7.4.x:
# when xenserver-release-config gets obsoleted by xcp-ng-release-config,
# its preun gets run last and disables the services.
# We don't want that, so we re-enable the services in this trigger
# which will be set off after postun has been executed.
systemctl preset move-kernel-messages.service >/dev/null 2>&1 || :
systemctl preset update-issue.service >/dev/null 2>&1 || :
systemctl preset xs-fcoe.service >/dev/null 2>&1 || :
# Also restore changes to /etc/sysconfig/snmp, removed by a triggerun scriptlet
if [ -f /etc/sysconfig/snmpd ]; then
    grep -qs '^OPTIONS' /etc/sysconfig/snmpd || echo 'OPTIONS="-c /etc/snmp/snmpd.xs.conf"' >>/etc/sysconfig/snmpd
fi

%files
%doc xcp-ng.repo
%defattr(0644,root,root,0755)
%{_sysconfdir}/redhat-release
%{_sysconfdir}/system-release
%{_sysconfdir}/centos-release
%config(noreplace) %{_sysconfdir}/os-release
%config(noreplace) %{_sysconfdir}/issue
%config(noreplace) %{_sysconfdir}/issue.net
%{_sysconfdir}/pki/rpm-gpg/
%config(noreplace) %{_sysconfdir}/yum.repos.d/*
%config(noreplace) %{_sysconfdir}/yum/vars/*
%{_sysconfdir}/rpm/macros.dist
%{_docdir}/redhat-release
%{_docdir}/centos-release
%{_datadir}/redhat-release
%{_datadir}/centos-release
%{_prefix}/lib/systemd/system-preset/*
%{python_sitelib}/xcp/branding.py*

%files config
%defattr(0644,root,root,0755)
%config(noreplace) %{_sysconfdir}/modprobe.d/*.conf
%config(noreplace) %{_sysconfdir}/motd.xs
%config(noreplace) %{_sysconfdir}/profile.d/*.sh
%config(noreplace) %{_sysconfdir}/sysctl.d/*.conf
%config(noreplace) %{_sysconfdir}/snmp/snmpd.xs.conf
%{_sysconfdir}/rsyslog.d/xenserver.conf
%{_sysconfdir}/logrotate.d/*
%{_sysconfdir}/udev/rules.d/*.rules
%{_sysconfdir}/systemd/system/*
%{_unitdir}/*
/opt/xensource/www/*
%attr(0755,-,-) /sbin/update-issue
%attr(0755,-,-) /opt/xensource/libexec/xen-cmdline
%attr(0755,-,-) /opt/xensource/libexec/ibft-to-ignore
%attr(0755,-,-) /opt/xensource/libexec/bfs-interfaces
%attr(0755,-,-) /opt/xensource/libexec/fcoe_driver
%attr(0755,-,-) %{_sysconfdir}/dhcp/dhclient.d/xs.sh

# custom log rotation, only enabled for legacy partition layout
/etc/cron.d/logrotate.cron.rpmsave
/etc/logrotate-xenserver.conf
%attr(0755,-,-) /opt/xensource/bin/logrotate-xenserver

# kernel logging to VT2
%attr(0755,-,-) /opt/xensource/libexec/move-kernel-messages
%attr(0755,-,-) /opt/xensource/libexec/set-printk-console

# Keep this changelog through future updates
%changelog
* Thu Jun 07 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 8.0.0-7
- Add custom bash prompt for XCP-ng

* Wed May 15 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 8.0.0-5
- Update to XCP-ng 8.0.0
- Update 'dist' macro to include the version number: ".xcpng8.0"
- Update web page and add XOA deployment

* Tue Nov 27 2018 Samuel Verschelde <stormi-xcp@ylix.fr> - 7.6.0-4
- Set the 'dist' macro to ".xcpng"

* Wed Oct 10 2018 Samuel Verschelde <stormi-xcp@ylix.fr> - 7.6.0-3
- Add XCP-ng's RPM GPG key

* Tue Sep 25 2018 Samuel Verschelde <stormi-xcp@ylix.fr> - 7.6.0-2
- Update to XCP-ng 7.6.0
- New welcome page

* Wed Jul 25 2018 Samuel Verschelde <stormi-xcp@ylix.fr> - 7.5.0-2
- Add triggerun scriptlet for smooth upgrade

* Fri Jul 06 2018 Samuel Verschelde <stormi-xcp@ylix.fr> - 7.5.0-1
- Rename to xcp-ng-release
- Update to XCP-ng 7.5.0

* Sun Apr 29 2018 John Else <john.else@gmail.com>
- Update packaging for XCP-ng

* Wed Nov 19 2014 Ross Lagerwall <ross.lagerwall@citrix.com>
- Initial xenserver-release packaging
