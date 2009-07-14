# $Revision: 1.22 $, $Date: 2008-02-18 20:52:47
#
# TODO:
# - what to do with the .NET thingy?
#
Summary:	Irrlicht - high performance realtime 3D engine
Summary(pl.UTF-8):	Irrlicht - wysoko wydajny silnik 3D czasu rzeczywistego
Name:		irrlicht
Version:	1.5
Release:	4
License:	BSD-like
Group:		Libraries
Source0:	http://dl.sourceforge.net/irrlicht/%{name}-%{version}.zip
# Source0-md5:	e3bc8c1074fc0ec2810dc48f94c05d5a
Patch0:		%{name}-glXGetProcAddress.patch
Patch1:		%{name}-system-libs.patch
Patch2:		%{name}-sparc.patch
URL:		http://irrlicht.sourceforge.net/
BuildRequires:	dos2unix
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	unzip
BuildRequires:	xorg-lib-libXxf86vm-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Irrlicht Engine is an open source high performance realtime 3D
engine written and usable in C++ and also available for .NET
languages. It is completely cross-platform, using D3D, OpenGL and its
own software renderer, and has all of the state-of-the-art features
which can be found in commercial 3D engines.

%description -l pl.UTF-8
Silnik Irrlicht to wysoko wydajny silnik 3D czasu rzeczywistego o
otwartych źródłach. Napisany i używany w języku C++, dostępny także
dla języków .NET. Jest w pełni przenośny między platformami, używa
D3D, OpenGL oraz własnego oprogramowania renderującego, oraz zawiera
wszystkie cechy komercyjnych silników 3D.

%package devel
Summary:	Header files for Irrlicht library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Irrlicht
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
This is the package containing the header files for Irrlicht library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe biblioteki Irrlicht.

%package static
Summary:	Static Irrlicht library
Summary(pl):	Statyczna biblioteka Irrlicht
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Irrlicht library.

%description static -l pl
Statyczna biblioteka Irrlicht

%package examples
Summary:	Examples for Irrlicht library for programmers
Summary(pl.UTF-8):	Przykłady użycia biblioteki Irrlicht dla programistów
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description examples
This is the package containing examples for Irrlicht library.

%description examples -l pl.UTF-8
Ten pakiet zawiera przykłady użycia biblioteki Irrlicht.

%prep
%setup -q

dos2unix include/IrrCompileConfig.h source/Irrlicht/Makefile

%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__make} -C source/Irrlicht \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags}   -DGLX_GLXEXT_LEGACY" \
	CXXFLAGS="%{rpmcflags} -DGLX_GLXEXT_LEGACY \$(CXXINCS) -DIRRLICHT_EXPORTS=1"
%{__make} -C source/Irrlicht clean
%{__make} -C source/Irrlicht sharedlib \
	CXX="%{__cxx}" \
	CFLAGS="%{rpmcflags} -fPIC   -DGLX_GLXEXT_LEGACY" \
	CXXFLAGS="%{rpmcflags} -fPIC -DGLX_GLXEXT_LEGACY \$(CXXINCS) -DIRRLICHT_EXPORTS=1"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir},%{_examplesdir}/%{name}-%{version}}

install lib/Linux/libIrrlicht.* $RPM_BUILD_ROOT%{_libdir}
ln -s $(basename lib/Linux/libIrrlicht.so.*.*) $RPM_BUILD_ROOT%{_libdir}/libIrrlicht.so
ln -s $(basename lib/Linux/libIrrlicht.so.*.*) $RPM_BUILD_ROOT%{_libdir}/libIrrlicht.so.1
cp -r include  $RPM_BUILD_ROOT%{_includedir}/irrlicht
ln -s irrlicht $RPM_BUILD_ROOT%{_includedir}/Irrlicht
cp -r examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

cp doc/readme{,-docs}.txt

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc changes.txt readme.txt doc/*.chm doc/readme-docs.txt
%attr(755,root,root) %{_libdir}/libIrrlicht.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libIrrlicht.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libIrrlicht.so
%{_includedir}/irrlicht
%{_includedir}/Irrlicht

%files static
%defattr(644,root,root,755)
%{_libdir}/libIrrlicht.a

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
