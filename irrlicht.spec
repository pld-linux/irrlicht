#
# TODO:
# - what to do with the .NET thingy?
# - fix Makefile to accept rpm*flags as options
#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	Irrlicht - high performance realtime 3D engine
Summary(pl.UTF-8):	Irrlicht - wysoko wydajny silnik 3D czasu rzeczywistego
Name:		irrlicht
Version:	1.8.5
Release:	1
License:	BSD-like
Group:		Libraries
Source0:	https://downloads.sourceforge.net/irrlicht/%{name}-%{version}.zip
# Source0-md5:	1fcf67c2906eb84b531af512de8481b1
Source1:	http://www.opengl.org/registry/api/GL/glext.h
Patch0:		%{name}-glXGetProcAddress.patch
Patch1:		%{name}-system-libs.patch
URL:		http://irrlicht.sourceforge.net/
BuildRequires:	OpenGL-devel
BuildRequires:	OpenGL-GLX-devel >= 1.4
BuildRequires:	bzip2-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel >= 1.4
BuildRequires:	libstdc++-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	sed >= 4.0
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
Summary(pl.UTF-8):	Statyczna biblioteka Irrlicht
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Irrlicht library.

%description static -l pl.UTF-8
Statyczna biblioteka Irrlicht

%package apidocs
Summary:	API documentation for Irrlicht library
Summary(pl.UTF-8):	Dokumentacja API biblioteki Irrlicht
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Irrlicht library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Irrlicht.

%package examples
Summary:	Examples for Irrlicht library for programmers
Summary(pl.UTF-8):	Przykłady użycia biblioteki Irrlicht dla programistów
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
BuildArch:	noarch

%description examples
This is the package containing examples for Irrlicht library.

%description examples -l pl.UTF-8
Ten pakiet zawiera przykłady użycia biblioteki Irrlicht.

%prep
%setup -q

%undos include/IrrCompileConfig.h
%undos source/Irrlicht/{Makefile,CImageLoaderPNG.cpp,CImageWriterPNG.cpp}

%patch -P0 -p1
%patch -P1 -p1

cp -f %{SOURCE1} source/Irrlicht/glext.h

%build
%if %{with static_libs}
%{__make} -C source/Irrlicht \
	CXX="%{__cxx}" \
	CXXINCS="-I../../include %{rpmcppflags}" \
	CFLAGS="%{rpmcflags}   -DGLX_GLXEXT_LEGACY" \
	CXXFLAGS="%{rpmcflags} -DGLX_GLXEXT_LEGACY \$(CXXINCS) -DIRRLICHT_EXPORTS=1" \
	LDFLAGS="%{rpmldflags} -lz -lpng -ljpeg -lbz2 -lX11 -lXxf86vm -lGL"
%{__make} -C source/Irrlicht clean
%endif

%{__make} -C source/Irrlicht sharedlib \
	CXX="%{__cxx}" \
	CXXINCS="-I../../include %{rpmcppflags}" \
	CFLAGS="%{rpmcflags} -fPIC   -DGLX_GLXEXT_LEGACY" \
	CXXFLAGS="%{rpmcflags} -fPIC -DGLX_GLXEXT_LEGACY \$(CXXINCS) -DIRRLICHT_EXPORTS=1" \
	LDFLAGS="%{rpmldflags} -lz -lpng -ljpeg -lbz2 -lX11 -lXxf86vm -lGL"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir},%{_examplesdir}/%{name}-%{version}}

install lib/Linux/libIrrlicht.* $RPM_BUILD_ROOT%{_libdir}
ln -s $(basename lib/Linux/libIrrlicht.so.*.*) $RPM_BUILD_ROOT%{_libdir}/libIrrlicht.so
ln -s $(basename lib/Linux/libIrrlicht.so.*.*) $RPM_BUILD_ROOT%{_libdir}/libIrrlicht.so.1
cp -r include  $RPM_BUILD_ROOT%{_includedir}/irrlicht
ln -s irrlicht $RPM_BUILD_ROOT%{_includedir}/Irrlicht

cp -pr examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version} \
	-name '*.vc*' -o -name '*.sln' -o -name '*.cbp' -o -name '*.dev' -print0 | xargs -0 %{__rm}
%{__rm} $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/*.workspace

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc changes.txt readme.txt doc/{aesGladman,*-license,upgrade-guide}.txt
%attr(755,root,root) %{_libdir}/libIrrlicht.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libIrrlicht.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libIrrlicht.so
%{_includedir}/irrlicht
%{_includedir}/Irrlicht

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libIrrlicht.a
%endif

%files apidocs
%defattr(644,root,root,755)
# "docu" and "html" are the same
%doc doc/html/*

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
