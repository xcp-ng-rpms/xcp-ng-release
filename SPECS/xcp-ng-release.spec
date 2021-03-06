# XCP-ng: TO BE UPDATED FOR EACH NEW RELEASE
# TODO: use data from branding file instead
%define PRODUCT_VERSION 8.2.0
%define PRODUCT_VERSION_TEXT 8.2
%define PRODUCT_VERSION_TEXT_SHORT %{PRODUCT_VERSION_TEXT}
%define PLATFORM_VERSION 3.2.0
%define BUILD_NUMBER release/stockholm/master/7

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
Version:        8.2.0
Release:        5
Summary:        XCP-ng release file
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
Obsoletes:      epel-release
Obsoletes:      xenserver-release <= %{version}

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


%description
XCP-ng release files

%package        presets
Summary:        XCP-ng presets file
Group:          System Environment/Base
Provides:       xs-presets = 1.3
Requires(posttrans): systemd

%description    presets
XCP-ng presets file.

%package        config
Summary:        XCP-ng configuration
Group:          System Environment/Base
Requires:       grep sed coreutils patch systemd
Requires(post): systemd xs-presets >= 1.3
Requires(preun): systemd xs-presets >= 1.3
Requires(postun): systemd xs-presets >= 1.3
Requires(post): sed
Obsoletes:      xenserver-release-config <= %{version}

%description    config
Additional utilities and configuration for XCP-ng.


%prep
%autosetup -p1
# XCP-ng: copy LICENSES from branding package
cp %{_usrsrc}/branding/LICENSES .

%build

%install
rm -rf %{buildroot}

%{_usrsrc}/branding/brand-directory.py /usr/src/branding/branding src/common %{buildroot}
%{_usrsrc}/branding/brand-directory.py /usr/src/branding/branding src/xenserver %{buildroot}
install -d -m 755 %{buildroot}%{python_sitelib}/xcp
%{_usrsrc}/branding/branding-compile.py --format=python > %{buildroot}%{python_sitelib}/xcp/branding.py

install -m 644 %{_usrsrc}/branding/EULA %{buildroot}/

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
# XCP-ng: add epel and xcp-ng repos
# install epel repos (disabled by default)
install -m 644 epel.repo %{buildroot}%{_sysconfdir}/yum.repos.d
install -m 644 epel-testing.repo %{buildroot}%{_sysconfdir}/yum.repos.d
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

%posttrans
# XCP-ng 8.1: running this in posttrans instead of post because xcp-ng-release may be installed after
# coreutils, since they both require each other: no guaranteed order
# XCP-ng 8.2: looks like CH 8.2 switched to posttrans too. I'm keeping my comment all the same.
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
# /!\ XCP-ng: if the following is updated, make sure to also adapt the rules
# in the netdata package, because they depend on this
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

# XCP-ng: exclude fallback mirror from fastestmirror
%triggerin config -- yum-plugin-fastestmirror
FM_PATCH=$(cat <<'EOF'
--- /etc/yum/pluginconf.d/fastestmirror.conf.orig     2019-07-10 18:51:55.253695553 +0200
+++ /etc/yum/pluginconf.d/fastestmirror.conf  2019-07-10 18:52:57.774059664 +0200
@@ -10,3 +10,6 @@
 maxthreads=15
 #exclude=.gov, facebook
 #include_only=.nl,.de,.uk,.ie
+
+# Exclude fallback mirror so that it's used as last resort
+exclude=updates.xcp-ng.org
EOF
)
# Do not apply patch if it was already applied
if ! echo "$FM_PATCH" | patch --dry-run -RsN -d / -p1 >/dev/null; then
    # Apply patch. Output NOT redirected to /dev/null so that error messages are displayed
    if ! echo "$FM_PATCH" | patch -tsN -r - -d / -p1; then
        echo "Error: failed to apply patch:"
        echo "$FM_PATCH"
    fi
fi

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
        echo "Error: failed to apply patch:"
        echo "$DEPMOD_PATCH"
    fi
fi

# XCP-ng: Enable chronyd and chrony-wait services.
#         They are not active in case of yum update from 8.0.
# XCP-ng: Also reduce timeout for chrony-wait
# TODO: review me for 8.3 since Citrix has implemented it differently.
# Also review me if the chrony package changed.
# We can't use an override file for ExecStart, so overriding the whole unit
# (or so I thought. Actually you can but it requires erasing it first with an empty value)
%triggerin config -- chrony
if [ ! -f /etc/systemd/system/chrony-wait.service ]; then
    cat <<'EOF' > /etc/systemd/system/chrony-wait.service
[Unit]
Description=Wait for chrony to synchronize system clock
Documentation=man:chronyc(1)
After=chronyd.service
Requires=chronyd.service
Before=time-sync.target
Wants=time-sync.target

[Service]
Type=oneshot
# Wait up to ~10 minutes for chronyd to synchronize and the remaining
# clock correction to be less than 0.1 seconds
# XCP-ng: NO! Wait only for 120s.
ExecStart=/usr/bin/chronyc -h 127.0.0.1,::1 waitsync 120 0.1 0.0 1
RemainAfterExit=yes
StandardOutput=null

[Install]
WantedBy=multi-user.target
EOF

    systemctl enable chronyd >/dev/null 2>&1 || :
    # Disable chrony-wait first before enabling in case it was enabled
    # so that the symlink points to our service file written above
    systemctl disable chrony-wait >/dev/null 2>&1 || :
    systemctl enable chrony-wait >/dev/null 2>&1 || :
fi


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

# XCP-ng: we update the BUILD_NUMBER here because in XS world
# it is updated separately by a script in the update-XSxx package.
# 
# Also, we update the file each time the package is installed, not just for upgrades, because in the past we renamed the package and then this wasn't run.
# Theoretically we shouldn't need that anymore, but it's not doing any harm
# and who knows, maybe we'll change the name again in the future.
if [ -f %{_sysconfdir}/xensource-inventory ]; then
    sed -i \
        -e "s@^\(PRODUCT_VERSION=\).*@\1'%{PRODUCT_VERSION}'@" \
        -e "s@^\(PLATFORM_VERSION=\).*@\1'%{PLATFORM_VERSION}'@" \
        -e "s@^\(PRODUCT_VERSION_TEXT=\).*@\1'%{PRODUCT_VERSION_TEXT}'@" \
        -e "s@^\(PRODUCT_VERSION_TEXT_SHORT=\).*@\1'%{PRODUCT_VERSION_TEXT_SHORT}'@" \
        -e "s@^\(BUILD_NUMBER=\).*@\1'%{BUILD_NUMBER}'@" \
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

# XCP-ng: Not needed anymore but kept as documentation in case
# we rename the package again in the future
##%%triggerpostun config -- xenserver-release-config < 7.5
## XCP-ng: To be reviewed at each release to make sure the fixes are still valid.
## Fix upgrade from XCP-ng 7.4.x:
## when xenserver-release-config gets obsoleted by xcp-ng-release-config,
## its preun gets run last and disables the services.
## We don't want that, so we re-enable the services in this trigger
## which will be set off after postun has been executed.
#systemctl preset move-kernel-messages.service >/dev/null 2>&1 || :
#systemctl preset update-issue.service >/dev/null 2>&1 || :
#systemctl preset xs-fcoe.service >/dev/null 2>&1 || :
## Also restore changes to /etc/sysconfig/snmp, removed by a triggerun scriptlet
#if [ -f /etc/sysconfig/snmpd ]; then
#    grep -qs '^OPTIONS' /etc/sysconfig/snmpd || echo 'OPTIONS="-c /etc/snmp/snmpd.xs.conf"' >>/etc/sysconfig/snmpd
#fi

%posttrans presets
# Install or Upgrade, run when all new .service files got installed by other packages.
# Ensure that new service files installed by existing packages get appropriate defaults.
systemctl preset-all --preset-mode=enable-only || :

%files
%doc xcp-ng.repo LICENSES
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

# Keep this changelog through future updates
%changelog
* Wed Feb 03 2021 Samuel Verschelde <stormi-xcp@ylix.fr> - 8.2.0-5
- Sync with XS82E015
- Fix sshd and ssh config patching
- Handling of chronyd systemd unit override not synced yet, on purpose

* Fri Nov 13 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 8.2.0-4
- Show xe CLI in the host page instead of XCP-ng Center

* Thu Oct 01 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 8.2.0-2
- Update link to official doc in the HTML welcome page

* Wed Jul 01 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 8.2.0-1
- Update to XCP-ng 8.2

* Fri Apr 03 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 8.1.0-6
- Enable chronyd and chrony-wait service
- Reduce chrony-wait timeout from 600s to 120s
- This reduces boot time a lot for hosts that can't reach a ntp server

* Wed Mar 25 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 8.1.0-3
- Update console welcome message to invite using Xen Orchestra

* Mon Jan 20 2020 Samuel Verschelde <stormi-xcp@ylix.fr> - 8.1.0-2
- Move POST scriptlet to POSTTRANS to avoid bugs due to ordering issues
- Avoids issue where uname is missing when executing the script
- See https://bugs.centos.org/view.php?id=14795

* Fri Dec 20 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 8.1.0-1
- Update to XCP-ng 8.1.0
- Add EULA and LICENSES back

* Thu Jul 18 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 8.0.0-13
- Add EPEL repos, disabled by default
- Warn against enabling CentOS and EPEL repos in .repo files

* Wed Jul 10 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 8.0.0-12
- Add fallback yum mirror in case mirrors.xcp-ng.org is down
- Includes updated repo file and updated fastestmirror configuration

* Thu Jun 27 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 8.0.0-11
- Update XOA quick deploy: workaround issue with xoa-updater

* Thu Jun 27 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 8.0.0-10
- Update XOA quick deploy: set XOA unix password

* Fri Jun 14 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 8.0.0-9
- Fix auto-add of first host in XOA during fast deploy

* Thu Jun 13 2019 Samuel Verschelde <stormi-xcp@ylix.fr> - 8.0.0-8
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
