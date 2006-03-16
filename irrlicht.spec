#
# TODO:
# - get rid of internal zlib and libpng
# - better subpackages split (leave only docs in base package, create -shared
#   and -static (since -shared is "just experimental and probably not tested")?
# - what do do with the .NET thingy?
# - proper Group fields
#
Summary:	Irrlicht - high performance realtime 3D engine
Summary(pl):	Irrlicht - wysoko wydajny silnik 3D czasu rzeczywistego
Name:		irrlicht
Version:	0.14.0
Release:	0.2
License:	BSD-like
Group:		Development/Libraries
Source0:	http://dl.sourceforge.net/irrlicht/%{name}-%{version}.zip
# Source0-md5:	5da8c8f4632d26f971fba2d56e04a652
Patch0:		%{name}-glXGetProcAddress.patch
URL:		http://irrlicht.sourceforge.net/
BuildRequires:	X11-devel
#BuildRequires:	libpng-devel
#BuildRequires:	libtool
#BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Irrlicht Engine is an open source high performance realtime 3D
engine written and usable in C++ and also available for .NET
languages. It is completely cross-platform, using D3D, OpenGL and its
own software renderer, and has all of the state-of-the-art features
which can be found in commercial 3D engines.

%description -l pl
Silnik Irrlicht to wysoko wydajny silnik 3D czasu rzeczywistego o
otwartych ¼ród³ach. Napisany i u¿ywany w jêzyku C++, dostepny tak¿e
dla jêzyków .NET. Jest w pe³ni przeno¶ny miêdzy platformami, u¿ywa
D3D, OpenGL oraz w³asnego oprogramowania renderuj±cego, oraz zawiera
wszystkie cechy komercyjnych silników 3D.

%package devel
Summary:	Header files for Irrlicht library
Summary(pl):	Pliki nag³ówkowe biblioteki Irrlicht
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This is the package containing the header files for Irrlicht library.

%description devel -l pl
Ten pakiet zawiera pliki nag³ówkowe biblioteki Irrlicht.

%package examples
Summary:	Examples for Irrlicht library for programmers
Summary(pl):	Przyk³ady u¿ycia biblioteki Irrlicht dla programistów
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description examples
This is the package containing examples for Irrlicht library.

%description examples -l pl
Ten pakiet zawiera przyk³ady u¿ycia biblioteki Irrlicht.

#%package static
#Summary:	Static Irrlicht library
#Summary(pl):	Statyczna biblioteka Irrlicht
#Group:		Development/Libraries
#Requires:	%{name}-devel = %{version}-%{release}
#
#%description static
#Static Irrlicht library.

#%description static -l pl
#Statyczna biblioteka Irrlicht

%prep
%setup -q
%{__unzip} -d source source/source.zip
%patch0 -p1

%build
%{__make} -C source/Irrlicht \
	CFLAGS="%{rpmcflags}   -DGLX_GLXEXT_LEGACY" \
	CXXFLAGS="%{rpmcflags} -DGLX_GLXEXT_LEGACY \$(CXXINCS) -DIRRLICHT_EXPORTS=1"
%{__make} -C source/Irrlicht sharedlib \
	CFLAGS="%{rpmcflags}   -DGLX_GLXEXT_LEGACY" \
	CXXFLAGS="%{rpmcflags} -DGLX_GLXEXT_LEGACY \$(CXXINCS) -DIRRLICHT_EXPORTS=1"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir},%{_examplesdir}/%{name}-%{version}}

install lib/Linux/libIrrlicht.* $RPM_BUILD_ROOT%{_libdir}
cp -r include  $RPM_BUILD_ROOT%{_includedir}/irrlicht
ln -s irrlicht $RPM_BUILD_ROOT%{_includedir}/Irrlicht
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
%{_includedir}/Irrlicht
