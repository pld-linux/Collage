#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs

Summary:	Cross-platform C++ network library
Summary(pl.UTF-8):	Wieloplatformowa biblioteka sieciowa dla C++
Name:		Collage
Version:	1.7.0
Release:	8
License:	LGPL v2.1
Group:		Libraries
#Source0Download: https://github.com/Eyescale/Collage/releases
Source0:	https://github.com/Eyescale/Collage/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	f0e57c1a2f6196c11ad8ac6029483e56
Patch0:		boost-1.61.patch
Patch1:		%{name}-boost.patch
Patch2:		includes.patch
Patch3:		boost-1.87.patch
URL:		http://libcollage.net/
BuildRequires:	Eyescale-CMake >= 2017.05
BuildRequires:	Lunchbox-devel >= 1.16.0
BuildRequires:	Pression-devel >= 2.0.0
BuildRequires:	Servus-devel >= 1.5.1
BuildRequires:	boost-devel >= 1.41.0
BuildRequires:	cmake >= 3.1
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	libibverbs-devel
BuildRequires:	librdmacm-devel
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	udt-devel
Requires:	Lunchbox >= 1.16.0
Requires:	Pression >= 2.0.0
Requires:	Servus >= 1.5.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Collage is a cross-platform C++ library for building heterogenous,
distributed applications. Among other things, it is the cluster
backend for the Equalizer parallel rendering framework. Collage
provides an abstraction of different network connections, peer-to-peer
messaging, node discovery, synchronization and high-performance,
object-oriented, versioned data distribution. Collage is designed for
low-overhead multi-threaded execution which allows applications to
easily exploit multi-core architectures.

%description -l pl.UTF-8
Collage to wieloplatformowa biblioteka C++ do tworzenia
heterogenicznych, rozproszonych aplikacji. Jest to między innymi
backend klastrowy dla szkieletu równoległego renderowania Equalizer.
Zapewnia abstrakcję różnych połączeń sieciowych, przesyłania
komunikatów między węzłami, wykrywanie węzłów, synchronizację oraz
wydajne, zorientowane obiektowo i wersjonowane rozproszenie danych.
Collage został zaprojektowany pod kątem lekkiej wielowątkowości, co
pozwala aplikacjom łatwo wykorzystywać architektury wielordzeniowe.

%package devel
Summary:	Header files for Collage library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Collage
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Lunchbox-devel >= 1.16.0
Requires:	Pression-devel >= 2.0.0
Requires:	Servus-devel >= 1.5.1
Requires:	boost-devel >= 1.41.0

%description devel
Header files for Collage library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Collage.

%package apidocs
Summary:	Collage API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki Collage
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Collage library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Collage.

%prep
%setup -q
%patch -P 0 -p1
%patch -P 1 -p1
%patch -P 2 -p1
%patch -P 3 -p1

rmdir CMake/common
ln -s %{_datadir}/Eyescale-CMake CMake/common

%build
install -d build
cd build

# boost 1.87 requires at least c++14, but something inside
# this PoS forces -stdc=gnu++11
%cmake .. \
	-DBUILDYARD_DISABLED=ON \
	-DCOMMON_DISABLE_WERROR=ON
%{__make}

%if %{with apidocs}
doxygen doc/Doxyfile
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/Collage/{doc,tests}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE.txt README.md doc/{README.IB,README.udt} doc/Changelog.md
%attr(755,root,root) %{_bindir}/coNetperf
%attr(755,root,root) %{_bindir}/coNodeperf
%attr(755,root,root) %{_bindir}/coObjectperf
%attr(755,root,root) %{_libdir}/libCollage.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libCollage.so.7

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libCollage.so
%{_includedir}/co
%dir %{_datadir}/Collage
%{_datadir}/Collage/CMake

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc build/doc/html/*
%endif
