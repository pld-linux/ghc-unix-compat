#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	unix-compat
Summary:	Portable POSIX-compatibility layer
Summary(pl.UTF-8):	Przenośna warstwa zgodności z POSIX
Name:		ghc-%{pkgname}
Version:	0.5.2
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/unix-compat
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	6775a2f0e03863ea847f907a08599144
URL:		http://hackage.haskell.org/package/unix-compat
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-unix >= 2.4
BuildRequires:	ghc-unix < 2.8
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-unix-prof >= 2.4
BuildRequires:	ghc-unix-prof < 2.8
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
Requires:	ghc-unix >= 2.4
Requires:	ghc-unix < 2.8
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddoc files
%define		_noautocompressdoc	*.haddock

%description
This package provides portable implementations of parts of the unix
package. This package re-exports the unix package when available.
When it isn't available, portable implementations are used.

%description -l pl.UTF-8
Ten pakiet dostarcza przenośne implementacje części pakietu unix. O
ile to możliwe, reeksportuje pakiet unix. Jeśli nie jest on dostępny,
używane są przenośne implementacje.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC.
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-unix-prof >= 2.4
Requires:	ghc-unix-prof < 2.8

%description prof
Profiling %{pkgname} library for GHC. Should be installed when GHC's
profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.lhs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs build
runhaskell Setup.lhs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.lhs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSunix-compat-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSunix-compat-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSunix-compat-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/include
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/PosixCompat
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/PosixCompat/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/PosixCompat/*.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSunix-compat-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/System/PosixCompat/*.p_hi
%endif
