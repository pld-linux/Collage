#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs

Summary:	Cross-platform C++ network library
Summary(pl.UTF-8):	Wieloplatformowa biblioteka sieciowa dla C++
Name:		Collage
Version:	1.1.2
Release:	5
License:	LGPL v2.1
Group:		Libraries
Source0:	https://github.com/Eyescale/Collage/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	89d37ca9f592da59ddfa57ac82eb83c3
Source1:	https://github.com/Eyescale/CMake/archive/92d0663/Eyescale-CMake-92d0663.tar.gz
# Source1-md5:	7abca85af7f36fec7e22d7f63d601cf8
URL:		http://libcollage.net/
BuildRequires:	Lunchbox-devel >= 1.10
BuildRequires:	boost-devel >= 1.41.0
BuildRequires:	cmake >= 2.8
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	libibverbs-devel
BuildRequires:	librdmacm-devel
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	udt-devel
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

%description devel
Header files for Collage library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Collage.

%package apidocs
Summary:	Collage API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki Collage
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for Collage library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Collage.

%prep
%setup -q -a1

%{__mv} CMake-* CMake/common
%{__rm} .gitexternals

%build
install -d build
cd build
%cmake .. \
	-DBUILDYARD_DISABLED=ON
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
%doc AUTHORS CHANGES.txt LICENSE.txt README.md doc/{README.IB,README.udt} build/doc/RelNotes.md
%attr(755,root,root) %{_bindir}/coNetperf
%attr(755,root,root) %{_bindir}/coNodeperf
%attr(755,root,root) %{_bindir}/coObjectperf
%attr(755,root,root) %{_libdir}/libCollage.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libCollage.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libCollage.so
%{_includedir}/co
%{_pkgconfigdir}/Collage.pc
%dir %{_datadir}/Collage
%{_datadir}/Collage/CMake

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc build/doc/html/*
%endif
