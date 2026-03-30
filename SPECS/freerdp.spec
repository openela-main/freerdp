# Can be rebuilt with FFmpeg/OpenH264 support enabled by passing
# "--with=ffmpeg", or "--with=openh264" to mock/rpmbuild; or by globally
# setting these variables:
# https://bugzilla.redhat.com/show_bug.cgi?id=2242028
#global _with_ffmpeg 1
#global _with_openh264 1

# Can be rebuilt with OpenCL support enabled by passing # "--with=opencl"
# or by globally setting:
#global _opencl 1

# Momentarily disable GSS support
# https://github.com/FreeRDP/FreeRDP/issues/4348
#global _with_gss 1

# Disable server support in RHEL
# https://bugzilla.redhat.com/show_bug.cgi?id=1639165
%if 0%{?fedora} || 0%{?rhel} >= 10
%global _with_server 1
%endif

# Disable support for missing codecs in RHEL
%{!?rhel:%global _with_soxr 1}
%if 0%{?fedora} || 0%{?rhel} >= 8
%global _with_lame 1
%endif

Name:           freerdp
Version:        2.11.7
Release:        4%{?dist}
Epoch:          2
Summary:        Free implementation of the Remote Desktop Protocol (RDP)
License:        ASL 2.0
URL:            http://www.freerdp.com/

Source0:        https://github.com/FreeRDP/FreeRDP/archive/%{version}/FreeRDP-%{version}.tar.gz

# Revert changes that break API
# https://issues.redhat.com/browse/RHEL-53081
Patch0:	        Revert-Moved-clipboard-utils-to-core-library-fixes-6.patch

# https://github.com/FreeRDP/FreeRDP/commit/c4a7c371342edf0d307cea728f56d3302f0ab38c
Patch1:         gdi-gfx-properly-clamp-SurfaceToSurface.patch

# https://github.com/FreeRDP/FreeRDP/commit/c4391827d7facfc874ca7f61a92afb82232a5748
Patch2:         codec-clear-fix-clear_resize_buffer-checks.patch

# https://github.com/FreeRDP/FreeRDP/commit/f8688b57f6cfad9a0b05475a6afbde355ffab720
Patch3:         codec-clear-fix-off-by-one-length-check.patch

# https://github.com/FreeRDP/FreeRDP/commit/1bab198a2edd0d0e6e1627d21a433151ea190500
Patch4:         codec-planar-fix-decoder-length-checks.patch

# https://github.com/FreeRDP/FreeRDP/commit/243ecf804bb122e8e643a5c142ad5a49d7aa19ee
Patch5:         codec-clear-check-clear_decomress-glyphData.patch

# https://github.com/FreeRDP/FreeRDP/commit/0421b53fcb4a80c95f51342e4a2c40c68a4101d3
Patch6:         client-x11-fix-double-free-in-case-of-invalid-pointe.patch

# https://github.com/FreeRDP/FreeRDP/commit/52106a26726a2aba77aa6d86014d2eb3507f0783
Patch7:         cache-offscreen-invalidate-bitmap-before-free.patch

# CVE-2026-22855
# https://github.com/FreeRDP/FreeRDP/commit/57c5647d98c2a026de8b681159cb188ca0439ef8
Patch8:         utils-smartcard-add-length-validity-checks.patch

# CVE-2026-22858
# https://github.com/FreeRDP/FreeRDP/commit/62a9e787edb2cfce9858fa4ceda5461680efc590
Patch9:         crypto-base64-ensure-char-is-singend.patch

# CVE-2026-22859
# https://github.com/FreeRDP/FreeRDP/commit/7b7e6de8fe427a2f01d331056774aec69710590b
Patch10:        channels-urbdrc-check-interface-indices-before-use.patch

# CVE-2026-26955
# https://github.com/FreeRDP/FreeRDP/commit/7d8fdce2d0ef337cb86cb37fc0c436c905e04d77
Patch11:        codec-clear-fix-destination-checks.patch

# CVE-2026-26965
# https://github.com/FreeRDP/FreeRDP/commit/a0be5cb87d760bb1c803ad1bb835aa1e73e62abc
Patch12:        codec-planar-fix-missing-destination-bounds-checks.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  alsa-lib-devel
BuildRequires:  cmake >= 2.8
BuildRequires:  cups-devel
BuildRequires:  gsm-devel
%{?_with_lame:BuildRequires:  lame-devel}
BuildRequires:  libicu-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libX11-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libXdamage-devel
BuildRequires:  libXext-devel
BuildRequires:  libXi-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libxkbfile-devel
BuildRequires:  libXrandr-devel
%{?_with_server:BuildRequires:  libXtst-devel}
BuildRequires:  libXv-devel
%{?_with_opencl:BuildRequires: opencl-headers >= 3.0}
%{?_with_opencl:BuildRequires: ocl-icd-devel}
%{?_with_openh264:BuildRequires:  openh264-devel}
%{?_with_x264:BuildRequires:  x264-devel}
%{?_with_server:BuildRequires:  pam-devel}
BuildRequires:  xmlto
BuildRequires:  zlib-devel
BuildRequires:  multilib-rpm-config

BuildRequires:  pkgconfig(cairo)
%{?_with_gss:BuildRequires:  pkgconfig(krb5) >= 1.13}
BuildRequires:  pkgconfig(libpcsclite)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  pkgconfig(openssl)
%{?_with_soxr:BuildRequires:  pkgconfig(soxr)}
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(xkbcommon)

%{?_with_ffmpeg:
BuildRequires:  pkgconfig(libavcodec) >= 57.48.101
BuildRequires:  pkgconfig(libavutil)
}

Provides:       xfreerdp = %{?epoch}:%{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{?epoch}:%{version}-%{release}
Requires:       libwinpr%{?_isa} = %{?epoch}:%{version}-%{release}

%description
The xfreerdp & wlfreerdp Remote Desktop Protocol (RDP) clients from the FreeRDP
project.

xfreerdp & wlfreerdp can connect to RDP servers such as Microsoft Windows
machines, xrdp and VirtualBox.

%package        libs
Summary:        Core libraries implementing the RDP protocol
Requires:       libwinpr%{?_isa} = %{?epoch}:%{version}-%{release}
Obsoletes:      %{name}-plugins < 1:1.1.0
Provides:       %{name}-plugins = %{?epoch}:%{version}-%{release}
%description    libs
libfreerdp-core can be embedded in applications.

libfreerdp-channels and libfreerdp-kbd might be convenient to use in X
applications together with libfreerdp-core.

libfreerdp-core can be extended with plugins handling RDP channels.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{?epoch}:%{version}-%{release}
Requires:       pkgconfig
Requires:       cmake >= 2.8

%description    devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}-libs.

%{?_with_server:
%package        server
Summary:        Server support for %{name}
Requires:       libwinpr%{?_isa} = %{?epoch}:%{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{?epoch}:%{version}-%{release}

%description    server
The %{name}-server package contains servers which can export a desktop via
the RDP protocol.
}

%package -n     libwinpr
Summary:        Windows Portable Runtime
Provides:       %{name}-libwinpr = %{?epoch}:%{version}-%{release}
Obsoletes:      %{name}-libwinpr < 1:1.2.0

%description -n libwinpr
WinPR provides API compatibility for applications targeting non-Windows
environments. When on Windows, the original native API is being used instead of
the equivalent WinPR implementation, without having to modify the code using it.

%package -n     libwinpr-devel
Summary:        Windows Portable Runtime development files
Requires:       libwinpr%{?_isa} = %{?epoch}:%{version}-%{release}
Requires:       pkgconfig
Requires:       cmake >= 2.8

%description -n libwinpr-devel
The %{name}-libwinpr-devel package contains libraries and header files for
developing applications that use %{name}-libwinpr.

%prep
%autosetup -p1 -n FreeRDP-%{version}

# Rpmlint fixes
find . -name "*.h" -exec chmod 664 {} \;
find . -name "*.c" -exec chmod 664 {} \;

%build
%cmake %{?_cmake_skip_rpath} \
    -DCMAKE_INSTALL_LIBDIR:PATH=%{_lib} \
    -DWITH_ALSA=ON \
    -DWITH_CAIRO=ON \
    -DWITH_CUPS=ON \
    -DWITH_CHANNELS=ON -DBUILTIN_CHANNELS=OFF \
    -DWITH_CLIENT=ON \
    -DWITH_DIRECTFB=OFF \
    -DWITH_DSP_FFMPEG=%{?_with_ffmpeg:ON}%{?!_with_ffmpeg:OFF} \
    -DWITH_FFMPEG=%{?_with_ffmpeg:ON}%{?!_with_ffmpeg:OFF} \
    -DWITH_GSM=ON \
    -DWITH_GSSAPI=%{?_with_gss:ON}%{?!_with_gss:OFF} \
    -DWITH_ICU=ON \
    -DWITH_IPP=OFF \
    -DWITH_JPEG=ON \
    -DWITH_LAME=%{?_with_lame:ON}%{?!_with_lame:OFF} \
    -DWITH_MANPAGES=ON \
    -DWITH_OPENCL=%{?_with_opencl:ON}%{?!_with_opencl:OFF} \
    -DWITH_OPENH264=%{?_with_openh264:ON}%{?!_with_openh264:OFF} \
    -DWITH_OPENSSL=ON \
    -DWITH_PCSC=ON \
    -DWITH_PULSE=ON \
    -DWITH_SERVER=%{?_with_server:ON}%{?!_with_server:OFF} \
    -DWITH_SERVER_INTERFACE=%{?_with_server:ON}%{?!_with_server:OFF} \
    -DWITH_SHADOW_X11=%{?_with_server:ON}%{?!_with_server:OFF} \
    -DWITH_SHADOW_MAC=%{?_with_server:ON}%{?!_with_server:OFF} \
    -DWITH_SOXR=%{?_with_soxr:ON}%{?!_with_soxr:OFF} \
    -DWITH_WAYLAND=ON \
    -DWITH_X11=ON \
    -DWITH_XCURSOR=ON \
    -DWITH_XEXT=ON \
    -DWITH_XKBFILE=ON \
    -DWITH_XI=ON \
    -DWITH_XINERAMA=ON \
    -DWITH_XRENDER=ON \
    -DWITH_XTEST=%{?_with_server:ON}%{?!_with_server:OFF} \
    -DWITH_XV=ON \
    -DWITH_ZLIB=ON \
%ifarch x86_64
    -DWITH_SSE2=ON \
    -DWITH_VAAPI=%{?_with_ffmpeg:ON}%{?!_with_ffmpeg:OFF} \
%else
    -DWITH_SSE2=OFF \
%endif
%ifarch armv7hl
    -DARM_FP_ABI=hard \
    -DWITH_NEON=OFF \
%endif
%ifarch armv7hnl
    -DARM_FP_ABI=hard \
    -DWITH_NEON=ON \
%endif
%ifarch armv5tel armv6l armv7l
    -DARM_FP_ABI=soft \
    -DWITH_NEON=OFF \
%endif
    %{nil}

%cmake_build

%install
%cmake_install

find %{buildroot} -name "*.a" -delete

%multilib_fix_c_header --file %{_includedir}/freerdp2/freerdp/build-config.h

%files
%{_bindir}/winpr-hash
%{_bindir}/winpr-makecert
%{_bindir}/wlfreerdp
%{_bindir}/xfreerdp
%{_mandir}/man1/winpr-hash.1*
%{_mandir}/man1/winpr-makecert.1*
%{_mandir}/man1/wlfreerdp.1*
%{_mandir}/man1/xfreerdp.1*

%files libs
%license LICENSE
%doc README.md ChangeLog
%{_libdir}/freerdp2/
%{_libdir}/libfreerdp-client2.so.*
%{?_with_server:
%{_libdir}/libfreerdp-server2.so.*
%{_libdir}/libfreerdp-shadow2.so.*
%{_libdir}/libfreerdp-shadow-subsystem2.so.*
}
%{_libdir}/libfreerdp2.so.*
%{_libdir}/libuwac0.so.*
%{_mandir}/man7/wlog.*

%files devel
%{_includedir}/freerdp2
%{_includedir}/uwac0
%{_libdir}/cmake/FreeRDP2
%{_libdir}/cmake/FreeRDP-Client2
%{?_with_server:
%{_libdir}/cmake/FreeRDP-Server2
%{_libdir}/cmake/FreeRDP-Shadow2
}
%{_libdir}/cmake/uwac0
%{_libdir}/libfreerdp-client2.so
%{?_with_server:
%{_libdir}/libfreerdp-server2.so
%{_libdir}/libfreerdp-shadow2.so
%{_libdir}/libfreerdp-shadow-subsystem2.so
}
%{_libdir}/libfreerdp2.so
%{_libdir}/libuwac0.so
%{_libdir}/pkgconfig/freerdp2.pc
%{_libdir}/pkgconfig/freerdp-client2.pc
%{?_with_server:
%{_libdir}/pkgconfig/freerdp-server2.pc
%{_libdir}/pkgconfig/freerdp-shadow2.pc
}
%{_libdir}/pkgconfig/uwac0.pc

%{?_with_server:
%files server
%{_bindir}/freerdp-proxy
%{_bindir}/freerdp-shadow-cli
%{_mandir}/man1/freerdp-shadow-cli.1*
}

%files -n libwinpr
%license LICENSE
%doc README.md ChangeLog
%{_libdir}/libwinpr2.so.*
%{_libdir}/libwinpr-tools2.so.*

%files -n libwinpr-devel
%{_libdir}/cmake/WinPR2
%{_includedir}/winpr2
%{_libdir}/libwinpr2.so
%{_libdir}/libwinpr-tools2.so
%{_libdir}/pkgconfig/winpr2.pc
%{_libdir}/pkgconfig/winpr-tools2.pc

%changelog
* Wed Mar 25 2026 Ondrej Holy <oholy@redhat.com> - 2:2.11.7-4
- Backport several CVE fixes
  Resolves: RHEL-151979, RHEL-152206

* Tue Feb 17 2026 Ondrej Holy <oholy@redhat.com> - 2:2.11.7-3
- Backport several CVE fixes
  Resolves: RHEL-148825, RHEL-148865, RHEL-148982

* Tue Jan 27 2026 Ondrej Holy <oholy@redhat.com> - 2:2.11.7-2
- Backport several CVE fixes
  Resolves: RHEL-142417, RHEL-142401, RHEL-142385, RHEL-142369, RHEL-142353
  Resolves: RHEL-142337, RHEL-142321

* Tue Oct 01 2024 Ondrej Holy <oholy@redhat.com> - 2:2.11.7-1
- Update to 2.11.7 (RHEL-53081)

* Tue Dec 13 2022 Ondrej Holy <oholy@redhat.com> - 2:2.2.0-10
- Fix "implicit declaration of function" errors (#2136153, #2145139)

* Thu Dec 08 2022 Ondrej Holy <oholy@redhat.com> - - 2:2.2.0-9
- CVE-2022-39282: Fix length checks in parallel driver (#2136151)
- CVE-2022-39283: Add missing length check in video channel (#2136153)
- CVE-2022-39316, CVE-2022-39317: Add missing length checks in zgfx (#2145139)
- CVE-2022-39318: Fix division by zero in urbdrc channel (#2145139)
- CVE-2022-39319: Add missing length checks in urbdrc channel (#2145139)
- CVE-2022-39320: Ensure urb_create_iocompletion uses size_t (#2145139)
- CVE-2022-39347: Fix path validation in drive channel (#2145139)
- CVE-2022-41877: Add missing length check in drive channel (#2145139)

* Thu Aug 11 2022 Ondrej Holy <oholy@redhat.com> - 2:2.2.0-8
- Fix /monitor-list output (rhbz#2108866)

* Wed Nov 10 2021 Ondrej Holy <oholy@redhat.com> - 2:2.2.0-4
- Refactored RPC gateway parser (rhbz#2017949)

* Fri Nov 05 2021 Felipe Borges <feborges@redhat.com> - 2:2.2.0-3
- Add checks for bitmap and glyph width and heigth values (rhbz#2017956)

* Wed Apr 28 2021 Ondrej Holy <oholy@redhat.com> - 2:2.2.0-2
- Fix exit codes for /help and similar options (rhbz#1910029)

* Fri Nov 20 2020 Ondrej Holy <oholy@redhat.com> - 2:2.2.0-1
- Update to 2.2.0 (rhbz#1881971)

* Mon May 25 2020 Ondrej Holy <oholy@redhat.com> - 2:2.1.1-1
- Update to 2.1.1 (rhbz#1834287).

* Fri Apr 17 2020 Ondrej Holy <oholy@redhat.com> - 2:2.0.0-47.rc4
- Fix SCARD_INSUFFICIENT_BUFFER error (rhbz#1803054)
- Do not advertise /usb in help output (rhbz#1761144)

* Wed Nov 28 2018 Ondrej Holy <oholy@redhat.com> - 2:2.0.0-46.rc4
- Update to 2.0.0-rc4 (#1624340)

* Mon Oct 15 2018 Ondrej Holy <oholy@redhat.com> - 2:2.0.0-45.rc3
- Disable server support in RHEL (#1639165)

* Wed Oct 10 2018 Ondrej Holy <oholy@redhat.com> - 2:2.0.0-44.rc3
- Fix packaging issues found by rpmdiff (#1637487)

* Tue Sep 25 2018 Ondrej Holy <oholy@redhat.com> - 2:2.0.0-43.rc3
- Fix important defects found by covscan (#1602500)

* Thu Sep 06 2018 Ondrej Holy <oholy@redhat.com> - 2:2.0.0-42.rc3
- Update to 2.0.0-rc3 (#1624340)

* Mon Apr 09 2018 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-41.20180405gita9ecd6a
- Update to latest snapshot.

* Wed Mar 21 2018 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-40.20180320gitde83f4d
- Add PAM support (fixes freerdp-shadow-cli). Thanks Paolo Zeppegno.
- Update to latest snapshot.

* Thu Mar 15 2018 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-39.20180314gitf8baeb7
- Update to latest snapshot.
- Fixes connection to RDP servers with the latest Microsoft patches:
  https://github.com/FreeRDP/FreeRDP/issues/4449

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.0.0-38.20180115git8f52c7e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 18 2018 Karsten Hopp <karsten@redhat.com> - 2.0.0-37git}
- use versioned build requirement on pkgconfig(openssl) to prevent using
  compat-openssl10-devel instead of openssl-devel

* Tue Jan 16 2018 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-36.20180115git8f52c7e
- Update to latest snapshot.
- Make GSS support optional and disable it for now (#1534094 and FreeRDP #4348,
  #1435, #4363).

* Wed Dec 20 2017 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-35.20171220gitbfe8359
- Update to latest snapshot post 2.0.0rc1.

* Mon Sep 11 2017 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-34.20170831git3b83526
- Update to latest snapshot.
- Trim changelog.

* Mon Aug 07 2017 Björn Esser <besser82@fedoraproject.org> - 2:2.0.0-33.20170724gitf8c9f43
- Rebuilt for AutoReq cmake-filesystem

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.0.0-32.20170724gitf8c9f43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-31.20170724gitf8c9f43
- Update to latest snapshot, Talos security fixes.

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.0.0-30.20170710gitf580bea
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 12 2017 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-29.20170710gitf580bea
- Update to latest snapshot.

* Mon Jun 26 2017 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-28.20170623git9904c32
- Update to latest snapshot.

* Mon May 15 2017 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-27.20170512gitb1df835
- Update to latest snapshot.

* Thu Apr 20 2017 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-26.20170419gitbfcf8e7
- Update to latest 2.0 snapshot.

* Thu Apr 13 2017 Orion Poplawski <orion@cora.nwra.com> - 2:2.0.0-25.20170317git8c68761
- Install tools via make install

* Wed Mar 22 2017 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-24.20170317git8c68761
- Update to latest snapshot.

* Mon Mar 06 2017 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-23.20170302git210de68
- Remove shared libxfreerdp-client shared library.

* Thu Mar 02 2017 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-22.20170302git210de68
- Move libxfreerdp-client shared object into devel subpackage.

* Thu Mar 02 2017 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-21.20170302git210de68
- Update to latest snapshot.
- Update build requirements, tune build options.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.0.0-20.20161228git90877f5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 09 2017 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-19.20161228git90877f5
- Update to latest snapshot.
