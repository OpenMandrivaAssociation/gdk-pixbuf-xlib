# Wine uses gdk-pixbuf
%ifarch %{x86_64}
%bcond_without compat32
%endif

%define enable_gtkdoc 0
%define enable_tests 0
#define _disable_ld_as_needed	1
#define _disable_rebuild_configure 1

%define oname gdk_pixbuf-xlib
%define pkgname gdk-pixbuf-xlib
%define binver 2.10.0
%define api 2.0
%define major 0

%define xlibname %mklibname gdk_pixbuf_xlib %{api} %{major}
%define devxlib %mklibname -d gdk_pixbuf_xlib %{api}
%define girname %mklibname gdk_pixbuf_xlib-gir %{api}

%define xlib32name %mklib32name gdk_pixbuf_xlib %{api} %{major}
%define devx32lib %mklib32name -d gdk_pixbuf_xlib %{api}
%bcond_with bootstrap

Summary:	Image loading and manipulation library for GTK+
Name:		%{pkgname}%{api}
Version:	2.40.2
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.gtk.org
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gdk-pixbuf-xlib/%(echo %{version} |cut -d. -f1-2)/%{pkgname}-%{version}.tar.xz
BuildRequires:	meson
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(jasper)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(shared-mime-info)
%if %enable_tests
BuildRequires:	x11-server-xvfb
# gw tests will fail without this
BuildRequires:	fonts-ttf-dejavu
%endif
%if %enable_gtkdoc
BuildRequires:	gtk-doc >= 0.9
BuildRequires:	sgml-tools
BuildRequires:	texinfo
%endif
Requires:	common-licenses
Requires:	shared-mime-info
Conflicts:	gtk+2.0 < 2.21.3
Conflicts:	%{_lib}gdk_pixbuf2.0_0 < 2.24.0-6
%if %{with compat32}
BuildRequires:	devel(libjpeg)
BuildRequires:	devel(libtiff)
BuildRequires:	devel(libglib-2.0)
BuildRequires:	devel(libgobject-2.0)
BuildRequires:	devel(libgio-2.0)
BuildRequires:	devel(libgmodule-2.0)
BuildRequires:	devel(libgdk_pixbuf-2.0)
BuildRequires:	devel(libz)
BuildRequires:	devel(libmount)
BuildRequires:	devel(libblkid)
BuildRequires:	devel(libpng16)
BuildRequires:	devel(libX11)
BuildRequires:	devel(libxcb)
BuildRequires:	devel(libXau)
BuildRequires:	devel(libXdmcp)
%endif

%description
This package contains libraries used by GTK+ to load and handle
various image formats.

%package -n %{xlibname}
Summary:	Image loading and manipulation library for GTK+
Group:		System/Libraries

%description -n %{xlibname}
This package contains libraries used by GTK+ to load and handle
various image formats.

%if !%{with bootstrap}
%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries

%description -n %{girname}
GObject Introspection interface description for %{name}.
%endif

%package -n %{devxlib}
Summary:	Development files for image handling library for GTK+ - Xlib
Group:		Development/GNOME and GTK+
Requires:	%{xlibname} = %{version}-%{release}

%description -n %{devxlib}
This package contains the development files needed to compile programs
that uses GTK+ image loading/manipulation Xlib library.

%if %{with compat32}
%package -n %{xlib32name}
Summary:	Image loading and manipulation library for GTK+ (32-bit)
Group:		System/Libraries

%description -n %{xlib32name}
This package contains libraries used by GTK+ to load and handle
various image formats.

%package -n %{devx32lib}
Summary:	Development files for image handling library for GTK+ - Xlib (32-bit)
Group:		Development/GNOME and GTK+
Requires:	%{xlib32name} = %{version}-%{release}

%description -n %{devx32lib}
This package contains the development files needed to compile programs
that uses GTK+ image loading/manipulation Xlib library.
%endif

%prep
%autosetup -n %{pkgname}-%{version} -p1

%if %{with compat32}
%meson32 \
	-Dgir=false \
	-Ddocs=false \
	-Dman=false \
	-Dinstalled_tests=false
%endif

# fix crash in nautilus (GNOME bug #596977)
export CFLAGS=$(echo %{optflags} | sed -e 's/-fomit-frame-pointer//g')

%meson \
%if %{with bootstrap}
	-Dgir=false \
%endif
%if %{enable_gtkdoc}
	-Ddocs=true \
	-Dman=true \
%endif
	-Dinstalled_tests=false

%build
%if %{with compat32}
%ninja_build -C build32 -j2
%endif
%meson_build -j2

%if %enable_tests
%check
xvfb-run %meson_test
%endif

%install
%if %{with compat32}
%ninja_install -C build32
%endif
%meson_install

%files -n %{xlibname}
%{_libdir}/libgdk_pixbuf_xlib-%{api}.so.%{major}*

%files -n %{devxlib}
%{_libdir}/libgdk_pixbuf_xlib-%{api}.so
%{_includedir}/gdk-pixbuf-%{api}/%{pkgname}/
%{_libdir}/pkgconfig/gdk-pixbuf-xlib-%{api}.pc

%if %{with compat32}
%files -n %{xlib32name}
%{_prefix}/lib/libgdk_pixbuf_xlib-%{api}.so.%{major}*

%files -n %{devx32lib}
%{_prefix}/lib/libgdk_pixbuf_xlib-%{api}.so
%{_prefix}/lib/pkgconfig/gdk-pixbuf-xlib-%{api}.pc
%endif
