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
%define dist .el%{dist_release_version}.centos

%define _unitdir /usr/lib/systemd/system

Name:           xenserver-release
Version:        8.2.0
Release:        2
Summary:        XenServer release file
Group:          System Environment/Base
License:        GPLv2
Requires(post): coreutils, grep
Requires:       %{name}-presets
Provides:       centos-release = %{base_release_version}
Provides:       centos-release(upstream) = %{upstream_rel}
Provides:       redhat-release = %{upstream_rel_long}
Provides:       system-release = %{upstream_rel_long}
Provides:       system-release(releasever) = %{base_release_version}
Obsoletes:      centos-release

#Obsolete CH80 hotfixes
Obsoletes:      update-XS80E001 control-XS80E001
Obsoletes:      update-XS80E002 control-XS80E002
Obsoletes:      update-XS80E003 control-XS80E003
Obsoletes:      update-XS80E004 control-XS80E004
Obsoletes:      update-XS80E005 control-XS80E005
Obsoletes:      update-XS80E006 control-XS80E006
#there has been no XS80E007
Obsoletes:      update-XS80E008 control-XS80E008
Obsoletes:      update-XS80E009 control-XS80E009
Obsoletes:      update-XS80E010 control-XS80E010
Obsoletes:      update-XS80E011 control-XS80E011
Obsoletes:      update-XS80E012 control-XS80E012

#Obsolete CH81 hotfixes
Obsoletes:      update-CH81 control-CH81
Obsoletes:      update-XS81E001 control-XS81E001
Obsoletes:      update-XS81E002 control-XS81E002
Obsoletes:      update-XS81E003 control-XS81E003
Obsoletes:      update-XS81E004 control-XS81E004
Obsoletes:      update-XS81E005 control-XS81E005

# Metadata for the installer to consume
Provides:       product-brand = XenServer
Provides:       product-version = %{PRODUCT_VERSION}
Provides:       product-build = 0x
Provides:       platform-name = XCP
Provides:       platform-version = %{PLATFORM_VERSION}
Provides:       product-version-text = %{PRODUCT_VERSION_TEXT}
Provides:       product-version-text-short = %{PRODUCT_VERSION_TEXT_SHORT}

BuildRequires:  systemd branding-xenserver

Source0: xenserver-release.tar.gz


Provides: gitsha(ssh://git@code.citrite.net/XS/xenserver-release.git) = ce3e34e6aaff7ce4feeb2305d7251d12048bd4d2


%description
XenServer release files

%package        presets
Provides: gitsha(ssh://git@code.citrite.net/XS/xenserver-release.git) = ce3e34e6aaff7ce4feeb2305d7251d12048bd4d2
Summary:        XenServer presets file
Group:          System Environment/Base
Provides:       xs-presets = 1.3
Requires(posttrans): systemd

%description    presets
XenServer preset file.

%package        config
Provides: gitsha(ssh://git@code.citrite.net/XS/xenserver-release.git) = ce3e34e6aaff7ce4feeb2305d7251d12048bd4d2
Summary:        XenServer configuration
Group:          System Environment/Base
Requires:       grep sed coreutils patch systemd
Requires(post): systemd xs-presets >= 1.3
Requires(preun): systemd xs-presets >= 1.3
Requires(postun): systemd xs-presets >= 1.3
Requires(post): sed

%description    config
Additional utilities and configuration for XenServer.


%prep
%autosetup -p1

%build

%install
rm -rf %{buildroot}

%{_usrsrc}/branding/brand-directory.py src/common %{buildroot}
%{_usrsrc}/branding/brand-directory.py src/xenserver %{buildroot}
install -d -m 755 %{buildroot}%{python_sitelib}/xcp
%{_usrsrc}/branding/branding-compile.py --format=python > %{buildroot}%{python_sitelib}/xcp/branding.py

install -m 644 %{_usrsrc}/branding/xenserver/EULA %{buildroot}/
install -D -m 644 \
    %{_usrsrc}/branding/xenserver/LICENSES \
    %{buildroot}%{_defaultdocdir}/XenServer/LICENSES

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

ln -s Citrix-index.html %{buildroot}/opt/xensource/www/index.html

%posttrans
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
@@ -24,7 +24,12 @@
 HostKey /etc/ssh/ssh_host_ecdsa_key
 HostKey /etc/ssh/ssh_host_ed25519_key

-# Ciphers and keying
+# Ciphers, MACs, KEX Algorithms & HostKeyAlgorithms
+Ciphers chacha20-poly1305@openssh.com,aes128-ctr,aes192-ctr,aes256-ctr,aes128-gcm@openssh.com,aes256-gcm@openssh.com,aes128-cbc,aes192-cbc,aes256-cbc
+MACs hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com,hmac-sha1-etm@openssh.com,hmac-sha2-256,hmac-sha2-512,hmac-sha1
+KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,ecdh-sha2-nistp256,ecdh-sha2-nistp384,ecdh-sha2-nistp521,diffie-hellman-group-exchange-sha256,diffie-hellman-group14-sha1
+HostKeyAlgorithms ecdsa-sha2-nistp256-cert-v01@openssh.com,ecdsa-sha2-nistp384-cert-v01@openssh.com,ecdsa-sha2-nistp521-cert-v01@openssh.com,ssh-ed25519-cert-v01@openssh.com,ssh-rsa-cert-v01@openssh.com,ecdsa-sha2-nistp256,ecdsa-sha2-nistp384,ecdsa-sha2-nistp521,ssh-ed25519,ssh-rsa
+
 #RekeyLimit default none

 # Logging
@@ -90,7 +90,7 @@
 #KerberosUseKuserok yes

 # GSSAPI options
-GSSAPIAuthentication yes
+GSSAPIAuthentication no
 GSSAPICleanupCredentials no
 #GSSAPIStrictAcceptorCheck yes
 #GSSAPIKeyExchange no
EOF

%triggerin config -- openssh-clients
( patch -tsN -r - -d / -p1 || : ) >/dev/null <<'EOF'
--- /etc/ssh/ssh_config	2019-10-28 13:56:16.791811367 +0000
+++ /etc/ssh/ssh_config	2019-10-28 13:26:42.374146454 +0000
@@ -66,3 +66,8 @@
 	SendEnv LC_PAPER LC_NAME LC_ADDRESS LC_TELEPHONE LC_MEASUREMENT
 	SendEnv LC_IDENTIFICATION LC_ALL LANGUAGE
 	SendEnv XMODIFIERS
+
+	Ciphers chacha20-poly1305@openssh.com,aes128-ctr,aes192-ctr,aes256-ctr,aes128-gcm@openssh.com,aes256-gcm@openssh.com,aes128-cbc,aes192-cbc,aes256-cbc
+	MACs hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com,hmac-sha1-etm@openssh.com,hmac-sha2-256,hmac-sha2-512,hmac-sha1
+	KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,ecdh-sha2-nistp256,ecdh-sha2-nistp384,ecdh-sha2-nistp521,diffie-hellman-group-exchange-sha256,diffie-hellman-group14-sha1
+	HostKeyAlgorithms ecdsa-sha2-nistp256-cert-v01@openssh.com,ecdsa-sha2-nistp384-cert-v01@openssh.com,ecdsa-sha2-nistp521-cert-v01@openssh.com,ssh-ed25519-cert-v01@openssh.com,ssh-rsa-cert-v01@openssh.com,ecdsa-sha2-nistp256,ecdsa-sha2-nistp384,ecdsa-sha2-nistp521,ssh-ed25519,ssh-rsa
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

# Hide previous 8.0 hotfixes from xapi
%triggerun config -- %{name}-config = 8.0.0, %{name}-config = 8.1.0
if [ -d /var/update/applied ]; then
    shopt -s nullglob
    for sfile in /var/update/applied/*; do
        label=$(xmllint --xpath "string(//update/@name-label)" $sfile)
        if [[ "$label" =~ ^XS8[01](E[0-9]{3}$|$) ]]; then
            rm -f $sfile
        fi
    done
fi

%post config
%systemd_post move-kernel-messages.service
%systemd_post update-issue.service
%systemd_post xs-fcoe.service
%systemd_post vm.slice

if [ "$1" -gt "1" -a -f %{_sysconfdir}/xensource-inventory ]; then
    sed -i \
        -e "s@^\(PRODUCT_VERSION=\).*@\1'%{PRODUCT_VERSION}'@" \
        -e "s@^\(PLATFORM_VERSION=\).*@\1'%{PLATFORM_VERSION}'@" \
        -e "s@^\(PRODUCT_VERSION_TEXT=\).*@\1'%{PRODUCT_VERSION_TEXT}'@" \
        -e "s@^\(PRODUCT_VERSION_TEXT_SHORT=\).*@\1'%{PRODUCT_VERSION_TEXT_SHORT}'@" \
        %{_sysconfdir}/xensource-inventory
fi

# Add myhostname to the hosts line of nsswitch.conf if it is not there already.
# This needs to be kept until the next upgrade-only release after 8.0.
grep -q '^hosts:.*myhostname' %{_sysconfdir}/nsswitch.conf || sed -i 's/^hosts:.*/\0 myhostname/' %{_sysconfdir}/nsswitch.conf

# Add ntp configuration to /etc/sysconfig/network which is written
# normally by the installer.
# This needs to be kept until the next upgrade-only release after 8.0.
grep -q '^NTPSERVERARGS=' %{_sysconfdir}/sysconfig/network || echo 'NTPSERVERARGS="iburst prefer"' >> %{_sysconfdir}/sysconfig/network

# This package provides an updated rsyslog.service file.
# Reenable it to ensure that the systemd symlink points to the correct file.
systemctl reenable rsyslog.service


%preun config
%systemd_preun move-kernel-messages.service
%systemd_preun update-issue.service
%systemd_preun xs-fcoe.service
%systemd_preun vm.slice


%postun config
%systemd_postun move-kernel-messages.service
%systemd_postun update-issue.service
%systemd_postun xs-fcoe.service
%systemd_postun vm.slice

%posttrans presets
# Install or Upgrade, run when all new .service files got installed by other packages.
# Ensure that new service files installed by existing packages get appropriate defaults.
systemctl preset-all --preset-mode=enable-only || :

%files
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
%{_prefix}/lib/systemd/system-preset/90-default.preset
/EULA
%{_docdir}/XenServer/LICENSES
%{python_sitelib}/xcp/branding.py*

%files presets
%{_prefix}/lib/systemd/system-preset/89-default.preset

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

# harden ciphers / TLS version used by curl/wget
/root/.curlrc
/root/.wgetrc

%changelog
* Mon Dec 21 2020 Ross Lagerwall <ross.lagerwall@citrix.com> - 8.2.0-2
- CA-337541: Reduce chrony-wait timeout to 2 minutes
- CA-346481: Fix sshd and ssh config patching

* Fri Jun 05 2020 Alex Brett <alex.brett@citrix.com> - 8.1.50-13
- CA-340624: Add missing hotfix obsoletes

* Tue Apr 21 2020 Ross Lagerwall <ross.lagerwall@citrix.com> - 8.1.50-12
- CA-338188: Add missing hotfix obsoletes

* Mon Apr 20 2020 Ross Lagerwall <ross.lagerwall@citrix.com> - 8.1.50-11
- CP-28927: Remove deprecated Ciphers, Kex Algorithms, Key Algorithms, &MACs

* Thu Apr 02 2020 Ben Anson <ben.anson@citrix.com> - 8.1.50-10
- REQ-811: enforce TLSv1.2

* Sat Mar 28 2020 Alex Brett <alex.brett@citrix.com> - 8.1.50-9
- CA-337346: Add missing hotfix obsoletes

* Mon Mar 23 2020 Mark Syms <mark.syms@citrix.com> - 8.1.50-8
- CP-33141: enable GFS2 space monitor

* Thu Feb 20 2020 Ross Lagerwall <ross.lagerwall@citrix.com> - 8.1.50-7
- CA-335376: Ensure that rsyslog's systemd symlink points to the correct file

* Wed Feb 05 2020 Ross Lagerwall <ross.lagerwall@citrix.com> - 8.1.50-4
- CP-31092: Enable new firstboot services

* Wed Nov 27 2019 Jennifer Herbert <jennier.herbert@citrix.com> - 8.1.50-2
- CP-32580: Make the Stockholm obsolete Quebec

* Thu Nov 21 2019 Konstantina Chremmou <konstantina.chremmou@citrix.com> - 8.1.50-1
- Bumped version-release to 8.1.50-1 for Stockholm.

* Tue Oct 29 2019 Pau Ruiz Safont <pau.safont@citrix.com> - 8.0.50-16
- CP-32138: Enable wsproxy.socket

* Fri Sep 27 2019 Ross Lagerwall <ross.lagerwall@citrix.com> - 8.0.50-15
- CA-326057: Clean up config for interfaces stopped being FCoE capable

* Fri Aug 23 2019 Ross Lagerwall <ross.lagerwall@citrix.com> - 8.0.50-14
- CP-30221: xenserver-release: Remove ntpdate configuration
- CA-293794: Prefer NTP servers from DHCP

* Thu Aug 08 2019 Ross Lagerwall <ross.lagerwall@citrix.com> - 8.0.50-12
- CA-324664/CP-32019: Fix various issues with starting FCoE

* Thu Aug 08 2019 Ross Lagerwall <ross.lagerwall@citrix.com> - 8.0.50-12
- CA-324664/CP-32019: Fix various issues with starting FCoE
- Cleanup the fcoe_driver script

* Mon Aug 5 2019 Ming Lu <ming.lu@citrix.com> - 8.0.50-11
- CA-323312: Remove circular dependency by new xenserver-release-presets

* Fri Jun 14 2019 Edwin Török <edvin.torok@citrix.com> - 8.0.50-10
- CA-321652: move our own preset customizations to a new file
- CA-321652: xs-presets virtual package

* Wed Jun 12 2019 Ross Lagerwall <ross.lagerwall@citrix.com> - 8.0.50-9
- CA-319463: Fix rsyslog not starting under certain conditions
- CP-27247: Add a blkio cgroup for VMs

* Fri Jun 07 2019 Ross Lagerwall <ross.lagerwall@citrix.com> - 8.0.50-8
- Enable vm.slice

* Wed May 29 2019 Edwin Török <edvin.torok@citrix.com> - 8.0.50-6
- add secureboot-certificates startup service

* Tue Nov 20 2018 Alex Brett <alex.brett@citrix.com> - 7.9.50-4
- Fix typo in product-version-text-short provide

* Wed Nov 19 2014 Ross Lagerwall <ross.lagerwall@citrix.com>
- Initial xenserver-release packaging
