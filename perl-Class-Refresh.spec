#
# Conditional build:
%bcond_without	tests		# do not perform "make test"
#
%define		pdir	Class
%define		pnam	Refresh
%include	/usr/lib/rpm/macros.perl
Summary:	Class::Refresh - refresh your classes during runtime
Name:		perl-Class-Refresh
Version:	0.07
Release:	1
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/Class/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	12d9332777c7654368010548386aa2d9
URL:		http://search.cpan.org/dist/Class-Refresh/
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with tests}
BuildRequires:	perl(Class::Unload)
BuildRequires:	perl(Devel::OverrideGlobalRequire)
BuildRequires:	perl-Class-Load
BuildRequires:	perl-Test-Fatal
BuildRequires:	perl-Test-Requires
BuildRequires:	perl-Try-Tiny
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
During development, it is fairly common to cycle between writing code
and testing that code. Generally the testing happens within the test
suite, but frequently it is more convenient to test things by hand
when tracking down a bug, or when doing some exploratory coding. In
many situations, however, this becomes inconvenient - for instance, in
a REPL, or in a stateful web application, restarting from the
beginning after every code change can get pretty tedious. This module
allows you to reload your application classes on the fly, so that the
code/test cycle becomes a lot easier.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

# this does some temp dir hackery that fails on builders
%{__rm} t/moose-metaclasses.t

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README
%{perl_vendorlib}/Class/Refresh.pm
%{_mandir}/man3/*
