#
# TODO:
# - get rid of internal zlib and libpng
# - better subpackages split (leave only docs in base package, create -shared
#   and -static (since -shared is "just experimental and probably not tested")?
#
Summary:	Irrlicht - high performance realtime 3D engine
#Summary(pl):	-
Name:		irrlicht
Version:	0.14.0
Release:	0.1
License:	BSD-like
Group:		Development/Libraries
Source0:	http://dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.zip
# Source0-md5:	5da8c8f4632d26f971fba2d56e04a652
URL:		http://irrlicht.sourceforge.net/
BuildRequires:	X11-devel
#BuildRequires:	zlib-devel
#BuildRequires:	libpng-devel
#BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Irrlicht Engine is an open source high performance realtime 3D engine
written and usable in C++ and also available for .NET languages. It
is completely cross-platform, using D3D, OpenGL and its own software
renderer, and has all of the state-of-the-art features which can be
found in commercial 3d engines.

#%description -l pl
#
#%package subpackage
#Summary:	-
#Summary(pl):	-
#Group:		-
#
#%description subpackage
#
#%description subpackage -l pl
#
#%package libs
#Summary:	-
#Summary(pl):	-
#Group:		Libraries
#
#%description libs
#
#%description libs -l pl


%package devel
Summary:	Header files for Irrlib library
Summary(pl):	Pliki nag³ówkowe biblioteki Irrlib
Group:		Development/Libraries
#Requires:	%{name} = %{version}-%{release}

%description devel
This is the package containing the header files for Irrlib library.

%description devel -l pl
Ten pakiet zawiera pliki nag³ówkowe biblioteki Irrlib.

%package examples
Summary:	Examples for Irrlib library for programmers
Summary(pl):	Przyk³ady u¿ycia biblioteki Irrlib dla programistów
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description examples
This is the package containing examples for Irrlib library.

%description examples -l pl
Ten pakiet zawiera przyk³ady u¿ycia biblioteki Irrlib.

#%package static
#Summary:	Static Irrlicht library
#Summary(pl):	Statyczna biblioteka Irrlicht
#Group:		Development/Libraries
#Requires:	%{name}-devel = %{version}-%{release}
#
#%description static
#Static Irrlicht library.

#%description static -l pl
#Statyczna biblioteka Irrlib

%prep
%setup -q
cd source
unzip source.zip
#%patch0 -p1

%build
%{__make} -C source/Irrlicht \
	CFLAGS="%{rpmcflags}"
%{__make} -C source/Irrlicht sharedlib \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir},%{_examplesdir}/%{name}-%{version}}

install lib/Linux/libIrrlicht.* $RPM_BUILD_ROOT%{_libdir}
cp -r include $RPM_BUILD_ROOT%{_includedir}/irrlicht
cp -r examples{,.net} $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

cp doc/readme{,-docs}.txt

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc changes.txt readme.txt doc/*.chm doc/readme-docs.txt
%{_libdir}/*

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}

%files devel
%defattr(644,root,root,755)
%{_includedir}/irrlicht
