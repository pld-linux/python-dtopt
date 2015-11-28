#
# Conditional build:
%bcond_without	python3	# CPython 3.x module
%bcond_without	tests	# do not perform "make test"

%define 	module	dtopt
Summary:	Add options to doctest examples while they are running
Name:		python-%{module}
Version:	0.1
Release:	6
License:	MIT
Group:		Libraries/Python
URL:		http://pypi.python.org/pypi/dtopt/
Source0:	http://pypi.python.org/packages/source/d/dtopt/dtopt-%{version}.tar.gz
# Source0-md5:	9a41317149e926fcc408086aedee6bab
BuildRequires:	python-distribute
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-distribute
BuildRequires:	python3-modules
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
dtopts adds options to doctest examples while they are running. When
using the doctest module it is often convenient to use the ELLIPSIS
option, which allows you to use ... as a wildcard. But you either have
to setup the test runner to use this option, or you must put #doctest:
+ELLIPSIS on every example that uses this feature. dtopt lets you
enable this option globally from within a doctest, by doing: >>> from
dtopt import ELLIPSIS

%package -n python3-dtopt
Summary:	Add options to doctest examples while they are running
Group:		Libraries/Python

%description -n python3-dtopt
dtopts adds options to doctest examples while they are running. When
using the doctest module it is often convenient to use the ELLIPSIS
option, which allows you to use ... as a wildcard. But you either have
to setup the test runner to use this option, or you must put #doctest:
+ELLIPSIS on every example that uses this feature. dtopt lets you
enable this option globally from within a doctest, by doing: >>> from
dtopt import ELLIPSIS

%prep
%setup -q -n %{module}-%{version}

# Remove bundled egg info if it exists.
rm -r *.egg-info

%build
%py_build

%if %{with python3}
%py3_build
%endif

%install
rm -rf $RPM_BUILD_ROOT
%py_install

%py_postclean

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/*
%dir %{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}/*.py[co]
%{py_sitescriptdir}/%{module}-*.egg-info

%if %{with python3}
%files -n python3-dtopt
%defattr(644,root,root,755)
%doc docs/*
%dir %{py3_sitescriptdir}/dtopt
%{py3_sitescriptdir}/%{module}/*.py
%{py3_sitescriptdir}/%{module}/__pycache__
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif
