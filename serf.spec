#
# Conditional build:
%bcond_with	tests	# perform "make check" (uses localhost network, fails on apr side when IPV6 is enabled and localhost resolves only to IPV4 addresses)
#
Summary:	A high-performance asynchronous HTTP client library
Summary(pl.UTF-8):	Wysokowydajna biblioteka asynchronicznego klienta HTTP
Name:		serf
Version:	1.0.0
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: http://code.google.com/p/serf/downloads/list
Source0:	http://serf.googlecode.com/files/%{name}-%{version}.tar.bz2
# Source0-md5:	3b179ed18f65c43141528aa6d2440db4
Patch0:		%{name}-sh.patch
URL:		http://code.google.com/p/serf/
BuildRequires:	apr-devel
BuildRequires:	apr-util-devel
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The serf library is a C-based HTTP client library built upon the
Apache Portable Runtime (APR) library. It multiplexes connections,
running the read/write communication asynchronously. Memory copies and
transformations are kept to a minimum to provide high performance
operation.

%description -l pl.UTF-8
Biblioteka serf to napisana w C biblioteka klienta HTTP stworzona w
oparciu o bibliotekę Apache Portable Runtime (APR). Obsługuje
połączenia naprzemiennie, wywołując asynchronicznie komunikację
odczyt-zapis. Kopiowanie i transformacje w pamięci są ograniczone do
minimum w celu zapewnienia wydajnego działania.

%package devel
Summary:	Header files for serf
Summary(pl.UTF-8):	Pliki nagłówkowe serf
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	apr-devel
Requires:	apr-util-devel

%description devel
C header files for the serf library.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla biblioteki serf.

%package static
Summary:	Static libraries for serf
Summary(pl.UTF-8):	Biblioteki statyczne serf
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static serf libraries.

%description static -l pl.UTF-8
Statyczne biblioteki serf.

%prep
%setup -q
%patch0 -p1

%build
%{__aclocal} -I build
%{__autoconf}
%configure \
	--with-apr=%{_prefix} \
	--with-apr-util=%{_prefix} \
	--with-openssl=%{_prefix}
%{__make}

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

chmod 755 $RPM_BUILD_ROOT%{_libdir}/lib*.so*

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES NOTICE README
%attr(755,root,root) %{_libdir}/libserf-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libserf-1.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libserf-1.so
%{_libdir}/libserf-1.la
%{_includedir}/serf*.h
%{_pkgconfigdir}/serf-1.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libserf-1.a
