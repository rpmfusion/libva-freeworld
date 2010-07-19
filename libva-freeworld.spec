%global apiver	0.31
%global sver	%{apiver}.1
%global sdsver	4
%global uver	%{sver}-1+sds%{sdsver}


Name:		libva-freeworld
# The rather complex versioning is due to the upstream being a patched
# version of the real upstream libva; when the real upstream 0.5 comes
# out we will no longer need to use Gwenole's patched version of 0.3
Version:	0.31.1
Release:	1.sds%{sdsver}%{?dist}
Summary:	Video Acceleration (VA) API for Linux
Group:		System Environment/Libraries
License:	MIT
URL:		http://www.splitted-desktop.com/~gbeauchesne/libva/
Source0:	http://www.splitted-desktop.com/~gbeauchesne/libva/libva_%{uver}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	libtool
BuildRequires:	libudev-devel
BuildRequires:	libXext-devel
BuildRequires:	libXfixes-devel
BuildRequires:	libdrm-devel
BuildRequires:	mesa-libGL-devel

Provides:	libva = %{version}-%{release}
Obsoletes:	libva < 0.31.1
Provides:	libva-utils = 0.31.1
Obsoletes:	libva-utils < 0.31.1

%description
Libva is a library providing the VA API video acceleration API.

%package	devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig
Provides:	libva-devel = %{version}-%{release}
Obsoletes:	libva-devel < 0.31.1

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n libva-%{sver}
for p in debian/patches/*.patch; do patch -p1 < $p; done

%build
autoreconf -i
%configure --disable-static --enable-glx --enable-i965-driver
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="install -p"

find %{buildroot} -regex ".*\.la$" | xargs rm -f --


%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING
%{_libdir}/libva*.so.*
%{_libdir}/va
%{_bindir}/vainfo

%files devel
%defattr(-,root,root,-)
%{_includedir}/va
%{_libdir}/libva*.so
%{_libdir}/pkgconfig/libva*.pc


%changelog
* Fri Jul 16 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.31.1-1.sds4
- Update to 0.31.1-1+sds4
- Add BR libudev-devel
- Obsoletes libva-utils 
  (tests files aren't installed anymore).

* Fri Jul 16 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.31.0.1.sds13-3
- Revert to the previous version scheme
- Fix mix use of spaces and tabs

* Wed Jul 14 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.31.0-1.sds13
- Move to libva-freeworld
- Virtual provides libva bumped with epoch
- Remove duplicate licence file.

* Mon Jul 05 2010 Nicolas Chauvet <kwizart@gmail.com> - 0.31.0.1.sds130-1
- Update to 0.31.0-1+sds13

* Fri Mar 12 2010 Adam Williamson <awilliam@redhat.com> - 0.31.0.1.sds10-1
- new SDS patch version (sds10):
	+ Add detection of Broadcom Crystal HD chip.
	+ Require vaDriverInit() function to include SDS API version. 
	+ OpenGL extensions updates:
		- Drop the 'bind' API. Only keep vaCopySurfaceGLX().
		- Fix FBO check for the generic implementation with TFP.
	+ Compat: strip vaPutSurface() flags to match older API.
		- This fixes deinterlacing support with GMA500 "psb" driver.
	+ Upgrade to GIT snapshot 2009/12/17:
		- Add a "magic" number to VADisplayContext.
		- Add more test programs, including h264 encoding.
- add -utils package for the various new binaries in this build

* Thu Dec 3 2009 Adam Williamson <awilliam@redhat.com> - 0.31.0.1.sds9-1
- new SDS patch version (sds9):
	+ Add extra picture info for VDPAU/MPEG-4

* Mon Nov 23 2009 Adam Williamson <awilliam@redhat.com> - 0.31.0.1.sds8-1
- new SDS patch version (sds8) - note sds7 package actually contained
  sds5 due to an error on my part:
	+ Fix detection of ATI chipsets with fglrx >= 8.69-Beta1.
	+ Upgrade to GIT snapshot 2009/11/20:
	  + Merge in some G45 fixes and additions.
	  + Add VA_STATUS_ERROR_SURFACE_IN_DISPLAYING.

* Tue Nov 17 2009 Adam Williamson <awilliam@redhat.com> - 0.31.0.1.sds7-1
- new SDS patch version:
	+ Fix compatibility with older programs linked against libva.so.0
	+ G45 updates:
	  + Fix vaCreateImage() and vaDestroyImage()
	  + Fix subpictures association to parent surfaces
	  + Fix rendering of subpictures (extra level of scaling)
	  + Fix subpicture palette upload (IA44 and AI44 formats for now)
	  + Add RGBA subpicture formats
	  + Add YV12 vaGetImage() and vaPutImage()
	  + Fix subpicture rendering (flickering)
	  + Fix return value for unimplemented functions
	  + Fix vaPutSurface() to handle cliprects (up to 80)


* Thu Oct 8 2009 Adam Williamson <awilliam@redhat.com> - 0.31.0.1.sds5-2
- enable the i965 driver build

* Tue Oct 6 2009 Adam Williamson <awilliam@redhat.com> - 0.31.0.1.sds5-1
- new SDS patch version:
	+ G45 updates:
	+ Fix VA driver version
	+ Fix vaAssociateSubpicture() arguments
	+ Add vaQueryDisplayAttributes() as a no-op
	+ Fix vaQueryImageFormats() to return 0 formats at this time

* Tue Sep 22 2009 Adam Williamson <awilliam@redhat.com> - 0.31.0.1.sds4-1
- new SDS patch version:
	+ Fix chek for GLX extensions
	+ Fix libva pkgconfig dependencies
	+ Fix vainfo dependencies (Konstantin Pavlov)
	+ Add C++ guards to <va/va_glx.h>
	+ Don't search LIBGL_DRIVERS_PATH, stick to extra LIBVA_DRIVERS_PATH
	+ Upgrade to GIT snapshot 2009/09/22:
		- Merge in SDS patches 001, 201, 202
		- i965_drv_driver: use the horizontal position of a slice

* Thu Sep 10 2009 Adam Williamson <awilliam@redhat.com> - 0.31.0.1.sds3-1
- new upstream + SDS patch version:
	+ Add OpenGL extensions (v3)
	+ Upgrade to VA API version 0.31 (2009/09/07 snapshot)
	+ Add drmOpenOnce() / drmCloseOnce() replacements for libdrm < 2.3
	+ Add generic VA/GLX implementation with TFP and FBO
	+ Fix detection of ATI chipsets with fglrx >= 8.66-RC1
	+ Add VASliceParameterBufferMPEG2.slice_horizontal_position for i965 
	  driver

* Thu Sep 3 2009 Adam Williamson <awilliam@redhat.com> - 0.30.4.1.sds5-3
- don't declare the stack as executable when creating libva.so.0

* Mon Aug 31 2009 Adam Williamson <awilliam@redhat.com> - 0.30.4.1.sds5-2
- enable glx support

* Mon Aug 31 2009 Adam Williamson <awilliam@redhat.com> - 0.30.4.1.sds5-1
- new SDS patch version:
	+ Add VA_STATUS_ERROR_UNIMPLEMENTED
	+ Add vaBindSurfaceToTextureGLX() and vaReleaseSurfaceFromTextureGLX()

* Wed Aug 26 2009 Adam Williamson <awilliam@redhat.com> - 0.30.4.1.sds4-1
- new SDS patch version:
	+ Add OpenGL extensions
	+ Fix NVIDIA driver version check
	+ Fix libva-x11-VERSION.so.* build dependencies

* Wed Aug 12 2009 Adam Williamson <awilliam@redhat.com> - 0.30.4.1.sds3-1
- initial package
