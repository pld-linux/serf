#
# Conditional build:
%bcond_without	kerberos5	# GSSAPI support
%bcond_with	tests		# perform "scons check" (uses localhost network, fails on apr side when IPV6 is enabled and localhost resolves only to IPV4 addresses)
#
Summary:	A high-performance asynchronous HTTP client library
Summary(pl.UTF-8):	Wysokowydajna biblioteka asynchronicznego klienta HTTP
Name:		serf
Version:	1.3.9
Release:	1
License:	Apache v2.0
Group:		Libraries
Source0:	https://www.apache.org/dist/serf/%{name}-%{version}.tar.bz2
# Source0-md5:	370a6340ff20366ab088012cd13f2b57
Patch0:		%{name}-scons.patch
URL:		https://serf.apache.org/
BuildRequires:	apr-devel
BuildRequires:	apr-util-devel
%{?with_kerberos5:BuildRequires:	heimdal-devel}
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	scons >= 2.3.0
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
%{?with_kerberos5:Requires:	heimdal-devel}
Requires:	openssl-devel >= 0.9.7d

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
%scons \
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir} \
	GSSAPI=/usr

%if %{with tests}
%scons check
%endif

%install
rm -rf $RPM_BUILD_ROOT

%scons install \
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir} \
	--install-sandbox=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES NOTICE README
%attr(755,root,root) %{_libdir}/libserf-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libserf-1.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libserf-1.so
%{_includedir}/serf-1
%{_pkgconfigdir}/serf-1.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libserf-1.a
