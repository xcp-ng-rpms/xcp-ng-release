%global distro  XCP-ng
%global major   9
%global minor   0
%global beta    pre-alpha
%global eol_date not yet defined

%global xsmajor 9
%global elmajor 10

Name:           xcp-ng-release
Version:        %{major}.%{minor}
Release:        0.ydi.2%{?dist}
Summary:        %{distro} release files
Group:          System Environment/Base
License:        GPL-2.0-or-later
URL:            https://xcp-ng.org

Requires:       almalinux-release
Requires:       xcp-ng-repos = %{version}-%{release}

Source200:      EULA
# FIXME this should be this package's LICENSE
#Source201:      LICENSE

Source500:      xcp-ng.repo

# FIXME: might want a new one for v9
Source600:      RPM-GPG-KEY-xcpng

## XCP-ng-specific stuff below
# FIXME: isn't this one redundant with /usr/share/licenses/?
Source9000:     LICENSES

%package -n xcp-ng-repos
Summary:        %{distro} package repositories
Requires:       xcp-ng-release = %{version}-%{release}
Requires:       xcp-ng-gpg-keys = %{version}-%{release}

%package -n xcp-ng-gpg-keys
Summary:        %{distro} RPM keys
Requires:       almalinux-gpg-keys

%description
%{distro} release files.

%description -n xcp-ng-gpg-keys
This package provides the RPM signature keys for %{distro}.

%description -n xcp-ng-repos
This package provides the package repository files for %{distro}.

%install
# # copy license and contributors doc here for %%license and %%doc macros
# mkdir -p ./docs
# cp %{SOURCE201} ./docs

install -d -m 0755 %{buildroot}%{_sysconfdir}
echo "%{distro} release %{major}.%{minor}%{?beta: %{beta}} (%{release_name})" > %{buildroot}%{_sysconfdir}/xcp-ng-release
ln -s xcp-ng-release %{buildroot}%{_sysconfdir}/almalinux-release

# -------------------------------------------------------------------------
# Definitions for /etc/os-release and for macros in macros.dist.  These
# macros are useful for spec files where distribution-specific identifiers
# are used to customize packages.

# Name of vendor / name of distribution. Typically used to identify where
# the binary comes from in --help or --version messages of programs.
# Examples: gdb.spec, clang.spec
%global dist_vendor Vates SAS
%global dist_name   %{distro}

# URL of the homepage of the distribution
# Example: gstreamer1-plugins-base.spec
%global dist_home_url https://xcp-ng.org/

# Bugzilla / bug reporting URLs shown to users.
# Examples: gcc.spec
%global dist_bug_report_url https://github.com/xcp-ng/xcp

# debuginfod server, as used in elfutils.spec.
# %global dist_debuginfod_url https://debuginfod.centos.org/
# -------------------------------------------------------------------------

# Create the os-release file
install -d -m 0755 %{buildroot}%{_prefix}/lib
cat > %{buildroot}%{_prefix}/lib/os-release << EOF
NAME="%{dist_name}"
VERSION="%{major}.%{minor}"
ID="xcp-ng"
ID_LIKE="rhel centos fedora almalinux"
VERSION_ID="%{major}.%{minor}"
PLATFORM_ID="platform:el%{elmajor}"
PRETTY_NAME="%{distro} %{major}.%{minor}%{?beta: %{beta}}"
ANSI_COLOR="0;34"
#LOGO="fedora-logo-icon"
#CPE_NAME="cpe:/o:almalinux:almalinux:%{major}::baseos"
HOME_URL="%{dist_home_url}"
DOCUMENTATION_URL="https://docs.xcp-ng.org/"
VENDOR_NAME="Vates"
VENDOR_URL="%{dist_home_url}"
BUG_REPORT_URL="%{dist_bug_report_url}"

REDHAT_SUPPORT_PRODUCT="%{distro}"
REDHAT_SUPPORT_PRODUCT_VERSION="%{major}.%{minor}%{?beta: %{beta}}"
SUPPORT_END=%{eol_date}
EOF

# set up the dist tag macros
mkdir -p %{buildroot}%{_rpmmacrodir}
cat > %{buildroot}%{_rpmmacrodir}/macros.dist << EOF
# dist macros.

%%__bootstrap ~bootstrap
%%xcpng %{major}
%%xenserver %{xsmajor}
%%almalinux_ver %{elmajor}
%%almalinux %{elmajor}
%%centos_ver %{elmajor}
%%centos %{elmajor}
%%rhel %{elmajor}
%%el%{elmajor} 1
%%distcore            .el%{elmajor}
%%dist %%{!?distprefix0:%%{?distprefix}}%%{expand:%%{lua:for i=0,9999 do print("%%{?distprefix" .. i .."}") end}}%%{distcore}%%{?distsuffix}%%{?with_bootstrap:%{__bootstrap}}
%%dist_vendor         %{dist_vendor}
%%dist_name           %{dist_name}
%%dist_home_url       %{dist_home_url}
%%dist_bug_report_url %{dist_bug_report_url}
EOF

# make xcp-ng-release a protected package
install -p -d -m 755 %{buildroot}%{_sysconfdir}/dnf/protected.d/
touch xcp-ng-release.conf
echo xcp-ng-release > xcp-ng-release.conf
install -p -c -m 0644 xcp-ng-release.conf %{buildroot}%{_sysconfdir}/dnf/protected.d/
rm -f xcp-ng-release.conf

# copy yum repos
install -d -m 0755 %{buildroot}%{_sysconfdir}/yum.repos.d
install -p -m 0644 %{SOURCE500} %{buildroot}%{_sysconfdir}/yum.repos.d/

# copy GPG keys
install -d -m 0755 %{buildroot}%{_sysconfdir}/pki/rpm-gpg
install -p -m 0644 %{SOURCE600} %{buildroot}%{_sysconfdir}/pki/rpm-gpg/

## XCP-ng-specific stuff below
install -d -m 0755 %{buildroot}%{_pkgdocdir}
install -p -m 0644 %{SOURCE9000} %{buildroot}%{_pkgdocdir}/

%files
# %license docs/LICENSE
%{_sysconfdir}/xcp-ng-release
%{_sysconfdir}/almalinux-release
%{_sysconfdir}/dnf/protected.d/xcp-ng-release.conf
%{_rpmmacrodir}/macros.dist
%{_prefix}/lib/os-release
%{_pkgdocdir}/LICENSES

%files -n xcp-ng-gpg-keys
%{_sysconfdir}/pki/rpm-gpg

%files -n xcp-ng-repos
%config(noreplace) %{_sysconfdir}/yum.repos.d/xcp-ng.repo

%changelog
* Wed Nov 19 2025 Yann Dirson <yann.dirson@vates.tech> - 9.0-0.ydi.2
- Initial release, taking bits from almalinux-release 10.0-32
