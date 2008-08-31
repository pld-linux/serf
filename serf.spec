#
# Conditional build:
%bcond_without	tests	# don't perform "make check"
#
Summary:	A high-performance asynchronous HTTP client library
Summary(pl.UTF-8):	Wysokowydajna biblioteka asynchronicznego klienta HTTP
Name:		serf
Version:	0.2.0
Release:	1
License:	Apache
Group:		Libraries
Source0:	http://serf.googlecode.com/files/%{name}-%{version}.tar.bz2
# Source0-md5:	cda4d1f871fbbad1b32ed8fd6a8149cc
URL:		http://code.google.com/p/serf/
BuildRequires:	apr-devel
BuildRequires:	apr-util-devel
BuildRequires:	openssl-devel >= 0.9.7d
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

%build
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

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES NOTICE README
%attr(755,root,root) %{_libdir}/libserf-*.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libserf-*.so.[0-9]

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libserf-*.so
%{_libdir}/libserf-*.la
%{_includedir}/serf*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libserf-*.a
