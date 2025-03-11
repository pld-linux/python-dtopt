#
# Conditional build:
%bcond_without	python2	# CPython 2.x module
%bcond_without	python3	# CPython 3.x module
%bcond_without	tests	# unit tests

%define 	module	dtopt
Summary:	Add options to doctest examples while they are running
Summary(pl.UTF-8):	Dodawanie opcji do przykładów doctest w trakcie ich działania
Name:		python-%{module}
Version:	0.1
Release:	16
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/dtopt/
Source0:	https://files.pythonhosted.org/packages/source/d/dtopt/dtopt-%{version}.tar.gz
# Source0-md5:	9a41317149e926fcc408086aedee6bab
Patch0:		dtopt-py3.patch
URL:		https://pypi.org/project/dtopt/
%if %{with python2}
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
dtopts adds options to doctest examples while they are running. When
using the doctest module it is often convenient to use the ELLIPSIS
option, which allows you to use ... as a wildcard. But you either have
to setup the test runner to use this option, or you must put
"#doctest: +ELLIPSIS" on every example that uses this feature. dtopt
lets you enable this option globally from within a doctest, by doing:
>>> from dtopt import ELLIPSIS

%description -l pl.UTF-8
dtopts dodaje opcje do przykładów doctest w trakcie ich działania.
Przy korzystaniu z modułu doctest często wygodne jest użycie opcji
ELLIPSIS, pozwalającej na użycie ... jako maski globalnej. Ale albo
trzeba konfigurować narzędzie uruchamiające do użycia tej opcji, albo
umieszczać "#doctest: +ELLIPSIS" przy każdym przykładzie używającym
tej opcji. dtopt pozwala włączyć tę opcję globalnie z poziomu doctest
poprzez:
>>> from dtopt import ELLIPSIS

%package -n python3-dtopt
Summary:	Add options to doctest examples while they are running
Summary(pl.UTF-8):	Dodawanie opcji do przykładów doctest w trakcie ich działania
Group:		Libraries/Python

%description -n python3-dtopt
dtopts adds options to doctest examples while they are running. When
using the doctest module it is often convenient to use the ELLIPSIS
option, which allows you to use ... as a wildcard. But you either have
to setup the test runner to use this option, or you must put
"#doctest: +ELLIPSIS" on every example that uses this feature. dtopt
lets you enable this option globally from within a doctest, by doing:
>>> from dtopt import ELLIPSIS

%description -n python3-dtopt -l pl.UTF-8
dtopts dodaje opcje do przykładów doctest w trakcie ich działania.
Przy korzystaniu z modułu doctest często wygodne jest użycie opcji
ELLIPSIS, pozwalającej na użycie ... jako maski globalnej. Ale albo
trzeba konfigurować narzędzie uruchamiające do użycia tej opcji, albo
umieszczać "#doctest: +ELLIPSIS" przy każdym przykładzie używającym
tej opcji. dtopt pozwala włączyć tę opcję globalnie z poziomu doctest
poprzez:
>>> from dtopt import ELLIPSIS

%prep
%setup -q -n %{module}-%{version}
%patch -P 0 -p1

# Remove bundled egg info
%{__rm} -r *.egg-info

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTHONPATH=$(pwd) \
%{__python} dtopt/tests.py 2>&1 | tee tests.log
# "one error is good"
grep -q ' 1 failures' tests.log
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd) \
%{__python3} dtopt/tests.py 2>&1 | tee tests.log
# "one error is good"
grep -q ' 1 failures' tests.log
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%{__rm} $RPM_BUILD_ROOT%{py_sitescriptdir}/dtopt/tests.py*
%py_postclean
%endif

%if %{with python3}
%py3_install

%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/dtopt/tests.py
%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/dtopt/__pycache__/tests.cpython-*.py*
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/*.txt
%{py_sitescriptdir}/dtopt
%{py_sitescriptdir}/dtopt-%{version}-py*.egg-info

%if %{with python3}
%files -n python3-dtopt
%defattr(644,root,root,755)
%doc docs/*.txt
%{py3_sitescriptdir}/dtopt
%{py3_sitescriptdir}/dtopt-%{version}-py*.egg-info
%endif
