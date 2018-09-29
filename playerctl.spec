# parallel build doesn't work
%global _smp_mflags -j1

Name:           playerctl
Summary:        Command-line MPRIS-compatible Media Player Controller
Version:        0.6.1
Release:        2%{?dist}
URL:            https://github.com/acrisci/playerctl
Source0:        https://github.com/acrisci/%{name}/archive/v%{version}.tar.gz
License:        LGPLv3+
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  chrpath

%description
Playerctl is a command-line utility and library for controlling media players
that implement the MPRIS D-Bus Interface Specification. Playerctl makes it
easy to bind player actions, such as play and pause, to media keys.

%package devel
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig
Summary:        Development header files for libplayerctl
BuildRequires:  gobject-introspection-devel gtk-doc make
Requires:       gobject-introspection-devel gtk-doc

%description devel
The package contains development header files for libplayerctl.

%prep
%autosetup

%build
./autogen.sh
%configure --disable-static --with-html-dir=%{_docdir}
%make_build

%check
%__make check

%install
%make_install
# remove RPATH in binaries (required during build)
chrpath --delete %{buildroot}%{_bindir}/%{name}
# remove libarchive files
rm -fv %{buildroot}%{_libdir}/*.la
# remove compat girs
rm -fv %{buildroot}%{_libdir}/girepository-1.0/*_gir
rm -fv %{buildroot}%{_datarootdir}/gir-1.0/*_gir

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license COPYING
%{_bindir}/playerctl
%{_libdir}/girepository-1.0/Playerctl*.typelib
%{_libdir}/libplayerctl-*.so.*
%{_mandir}/man1/playerctl*

%files devel
%{_datarootdir}/gir-1.0/Playerctl*.gir
%{_includedir}/playerctl
%{_libdir}/libplayerctl-*.so
%{_libdir}/pkgconfig/playerctl-*.pc

%changelog
* Sat Sep 29 2018 Sergey Korolev <korolev.srg@gmail.com> - 0.6.1-3
- Fix url to sources and add make dependency

* Sat Sep 29 2018 Sergey Korolev <korolev.srg@gmail.com> - 0.6.1-2
- Fix url to sources and fix license

* Sat Sep 29 2018 Sergey Korolev <korolev.srg@gmail.com> - 0.6.1-1
- Update to new version

* Thu May 24 2018 Greg Wildman <greg@techno.co.za> - 0.5.0-2
- Update to new version

* Tue Oct 10 2017 Greg Wildman <greg@techno.co.za> - 0.5.0-1
- Update to new version

* Fri Sep 25 2015 Jan Vcelak <jvcelak@fedoraproject.org> 0.4.2-2
- fix devel subpackage dependencies
- disable parallel build

* Fri Sep 25 2015 Jan Vcelak <jvcelak@fedoraproject.org> 0.4.2-1
- initial version of the package
