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
Release:        7%{?dist}.6
Epoch:          2
Summary:        Free implementation of the Remote Desktop Protocol (RDP)
License:        ASL 2.0
URL:            http://www.freerdp.com/

Source0:        https://github.com/FreeRDP/FreeRDP/archive/%{version}/FreeRDP-%{version}.tar.gz

# https://issues.redhat.com/browse/RHEL-113722
Patch:          core-tcp-retry-all-DNS-entries-until-success.patch
Patch:          core-tcp-Try-next-DNS-entry-on-connect-failure.patch
Patch:          core-tcp-Don-t-ignore-connect-errors.patch
Patch:          core-tcp-Fix-PreferIPv6OverIPv4-fallback-to-IPv4-add.patch
Patch:          core-tcp-fix-double-free-in-get_next_addrinfo.patch

# https://github.com/FreeRDP/FreeRDP/commit/c4a7c371342edf0d307cea728f56d3302f0ab38c
Patch:          gdi-gfx-properly-clamp-SurfaceToSurface.patch

# https://github.com/FreeRDP/FreeRDP/commit/c4391827d7facfc874ca7f61a92afb82232a5748
Patch:          codec-clear-fix-clear_resize_buffer-checks.patch

# https://github.com/FreeRDP/FreeRDP/commit/f8688b57f6cfad9a0b05475a6afbde355ffab720
Patch:          codec-clear-fix-off-by-one-length-check.patch

# https://github.com/FreeRDP/FreeRDP/commit/1bab198a2edd0d0e6e1627d21a433151ea190500
Patch:          codec-planar-fix-decoder-length-checks.patch

# https://github.com/FreeRDP/FreeRDP/commit/243ecf804bb122e8e643a5c142ad5a49d7aa19ee
Patch:          codec-clear-check-clear_decomress-glyphData.patch

# https://github.com/FreeRDP/FreeRDP/commit/0421b53fcb4a80c95f51342e4a2c40c68a4101d3
Patch:          client-x11-fix-double-free-in-case-of-invalid-pointe.patch

# https://github.com/FreeRDP/FreeRDP/commit/52106a26726a2aba77aa6d86014d2eb3507f0783
Patch:          cache-offscreen-invalidate-bitmap-before-free.patch

# CVE-2026-22855
# https://github.com/FreeRDP/FreeRDP/commit/57c5647d98c2a026de8b681159cb188ca0439ef8
Patch:          utils-smartcard-add-length-validity-checks.patch

# CVE-2026-22858
# https://github.com/FreeRDP/FreeRDP/commit/62a9e787edb2cfce9858fa4ceda5461680efc590
Patch:          crypto-base64-ensure-char-is-singend.patch

# CVE-2026-22859
# https://github.com/FreeRDP/FreeRDP/commit/7b7e6de8fe427a2f01d331056774aec69710590b
Patch:          channels-urbdrc-check-interface-indices-before-use.patch

# CVE-2026-26955
# https://github.com/FreeRDP/FreeRDP/commit/7d8fdce2d0ef337cb86cb37fc0c436c905e04d77
Patch:          codec-clear-fix-destination-checks.patch

# CVE-2026-26965
# https://github.com/FreeRDP/FreeRDP/commit/a0be5cb87d760bb1c803ad1bb835aa1e73e62abc
Patch:          codec-planar-fix-missing-destination-bounds-checks.patch

# CVE-2026-22852
# https://github.com/FreeRDP/FreeRDP/commit/cd1ffa112cfbe1b40a9fd57e299a8ea12e23df0d
Patch:          channels-audin-free-up-old-audio-formats.patch

# CVE-2026-22854
# https://github.com/FreeRDP/FreeRDP/commit/3da319570c8a6be0a79b3306f1ed354c4a943259
Patch:          channels-drive-fix-constant-type.patch

# CVE-2026-22856
# https://github.com/FreeRDP/FreeRDP/commit/b35aa3614d32bff3fc1272cd7c4617f711fca1a4
# https://github.com/FreeRDP/FreeRDP/commit/675c20f08f32ca5ec06297108bdf30147d6e2cd9
Patch:          channels-serial-lock-list-dictionary.patch
Patch:          channels-serial-explicitly-lock-serial-IrpThreads.patch

# CVE-2026-23732
# https://github.com/FreeRDP/FreeRDP/commit/3bc1eeb4f63ceec9a696af194e4c1ea0e67ff60c
# https://github.com/FreeRDP/FreeRDP/commit/9f0eb3b7d43069a1e973464bcb43d1ef965ae65e
Patch:          codec-color-add-freerdp_glyph_convert_ex.patch
Patch:          gdi-graphics-Use-freerdp_glyph_convert_ex.patch

# CVE-2026-23948
# https://github.com/FreeRDP/FreeRDP/commit/4d44e3c097656a8b9ec696353647b0888ca45860
Patch:          core-info-fix-missing-NULL-check.patch

# CVE-2026-24491
# https://github.com/FreeRDP/FreeRDP/commit/e02e052f6692550e539d10f99de9c35a23492db2
# https://github.com/FreeRDP/FreeRDP/commit/635ae3c8193256db01774fab5ff11bcae57aed6b
# https://github.com/FreeRDP/FreeRDP/commit/e01cd85c8003a245ef9778f0eda4b9235514c201
Patch:          channels-drdynvc-reset-channel_callback-before-close.patch
Patch:          channels-video-unify-error-handling.patch
Patch:          channels-video-fix-wrong-cast.patch

# CVE-2026-24675
# https://github.com/FreeRDP/FreeRDP/commit/d676518809c319eec15911c705c13536036af2ae
Patch:          channels-urbdrc-do-not-free-MsConfig-on-failure.patch

# CVE-2026-24676
# https://github.com/FreeRDP/FreeRDP/commit/026b81ae5831ac1598d8f7371e0d0996fac7db00
Patch:          channels-audin-reset-audin-format.patch

# CVE-2026-24679
# https://github.com/FreeRDP/FreeRDP/commit/2d563a50be17c1b407ca448b1321378c0726dd31
Patch:          channels-urbdrc-ensure-InterfaceNumber-is-within-ran.patch

# CVE-2026-24681
# https://github.com/FreeRDP/FreeRDP/commit/414f701464929c217f2509bcbd6d2c1f00f7ed73
Patch:          channels-urbdrc-cancel-all-usb-transfers-on-channel-.patch

# CVE-2026-24683
# https://github.com/FreeRDP/FreeRDP/commit/d9ca272dce7a776ab475e9b1a8e8c3d2968c8486
Patch:          channels-ainput-lock-context-when-updating-listener.patch

# CVE-2026-24684
# https://github.com/FreeRDP/FreeRDP/commit/622bb7b4402491ca003f47472d0e478132673696
# https://github.com/FreeRDP/FreeRDP/commit/afa6851dc80835d3101e40fcef51b6c5c0f43ea5
Patch:          channels-rdpsnd-terminate-thread-before-free.patch
Patch:          channel-rdpsnd-only-clean-up-thread-before-free.patch

# CVE-2026-31806
# https://github.com/FreeRDP/FreeRDP/commit/83d9aedea278a74af3e490ff5eeb889c016dbb2b
# https://github.com/FreeRDP/FreeRDP/commit/169971607cece48384cb94632b829bd57336af0f
Patch:          codec-nsc-limit-copy-area-in-nsc_process_message.patch
Patch:          codec-nsc-fix-use-of-nsc_process_message.patch

# CVE-2026-33984
# https://github.com/FreeRDP/FreeRDP/commit/a2dde6d9832cb032e8cf12cab3da84dafbab9006
Patch:          codec-clear-update-CLEAR_VBAR_ENTRY-size-after-alloc.patch

# CVE-2026-33983
# https://github.com/FreeRDP/FreeRDP/commit/78188ab479c8e6eb9ba2475b3732c76b4bbe5425
# https://github.com/FreeRDP/FreeRDP/commit/78677dc6e262f46937d00c3aa52381e4bb198fa5
Patch:          codec-progressive-fail-progressive_rfx_quant_sub-on-invalid-values.patch
Patch:          codec-progressive-fix-underflow-guard-in-progressive_rfx_quant_sub.patch

# CVE-2026-26986
# https://github.com/FreeRDP/FreeRDP/commit/b4f0f0a18fe53aa8d47d062f91471f4e9c5e0d51
Patch:          client-x11-fix-xf_rail_window_common-cleanup.patch

# CVE-2026-27951
# https://github.com/FreeRDP/FreeRDP/commit/118afc0b954ba9d5632b7836ad24e454555ed113
Patch:          allocations-fix-growth-of-preallocated-buffers.patch

# CVE-2026-29775
# https://github.com/FreeRDP/FreeRDP/commit/ffad58fd2b329efd81a3239e9d7e3c927b8e503f
# https://github.com/FreeRDP/FreeRDP/commit/8270e0bb3d6726c947d57c93ba9caa92a052b557
Patch:          cache-bitmap-overallocate-bitmap-cache.patch
Patch:          cache-bitmap-initialize-overallocated-bitmap-cache-extra-slot.patch

# CVE-2026-31884
# https://github.com/FreeRDP/FreeRDP/commit/03b48b3601d867afccac1cdc6081de7a275edce7
Patch:          codec-dsp-add-format-checks.patch

# CVE-2026-31883
# CVE-2026-31885
# https://github.com/FreeRDP/FreeRDP/commit/16df2300e1e3f5a51f68fb1626429e58b531b7c8
Patch:          codec-dsp-fix-array-bounds-checks.patch

# CVE-2026-33985
# https://github.com/FreeRDP/FreeRDP/commit/c49d1ad43b8c7b32794d0250f2623c2dccd7ef25
Patch:          codec-clear-update-clear_glyph_entry-count-after-alloc.patch

# CVE-2026-25952
# https://github.com/FreeRDP/FreeRDP/commit/1994e9844212a6dfe0ff12309fef520e888986b5
# https://github.com/FreeRDP/FreeRDP/commit/78fd7f580d5f9e6d9d582d82e5ea96003844fbdf
# https://github.com/FreeRDP/FreeRDP/commit/4ff57b68c2960fa414d03c78ff0e0660be1cc5bd
# https://github.com/FreeRDP/FreeRDP/commit/a278ff74117444c635c50ffa5084ecf517171f5a
Patch:          client-x11-lock-appwindow.patch
Patch:          client-x11-improve-rails-window-locking.patch
Patch:          client-x11-refactor-locking.patch
Patch:          client-x11-fix-deadlock-on-output-expose.patch

# CVE-2026-45700
# https://github.com/FreeRDP/FreeRDP/commit/4a065a941ae134a0433d1497c03b3c3eb91b9f85
Patch:          codec-planar-fix-bounds-checks.patch

# CVE-2026-64624
# https://github.com/FreeRDP/FreeRDP/commit/22c5deea52404f51a13276b3abda44e1e60704cf
Patch:          client-common-deactivate-cli-parsing-in-rdp-files.patch

# CVE-2026-67289
# https://github.com/FreeRDP/FreeRDP/commit/f163b2d2080d922cb725800781f43f16bc2882c0
# https://github.com/FreeRDP/FreeRDP/commit/ab5905cbada0d34cf85ffd32881cacaf8275744f
# https://github.com/FreeRDP/FreeRDP/commit/1db16b4b121a1221c0454f7d223096cac87bf244
Patch:          winpr-crt-add-functions-to-test-string.patch
Patch:          core-redirection-check-redirection-values-for-validity.patch
Patch:          core-redirection-relax-checks.patch

# CVE-2026-68580
# https://github.com/FreeRDP/FreeRDP/commit/3bf07d4470bbe42faf4ef8197c8fe1b6b759b00f
Patch:          channels-audin-limit-FramesPerPacket.patch

# CVE-2026-67299
# https://github.com/FreeRDP/FreeRDP/commit/172edbddd24f33033b9eafae6ea1fff0641a24f4
Patch:          core-message-fix-update_message_WindowIcon.patch

# CVE-2026-55194
# https://github.com/FreeRDP/FreeRDP/commit/9f2da52c2341cc14a96ad12e69c5b83d0bcd8b5a
Patch:          core-gateway-ensure-buffer-size-for-current-write.patch

# CVE-2026-67288
# https://github.com/FreeRDP/FreeRDP/commit/efe40e15d508f9754b7a3af851de4d2a0b1128d8
Patch:          scard-handle-nullptr-for-LookupName.patch

# CVE-2026-67291
# https://github.com/FreeRDP/FreeRDP/commit/649efd9326b3c5b236d39467b6e7de92d70efb59
Patch:          cache-glyph-tighten-bounds-checks.patch

# CVE-2026-67301
# https://github.com/FreeRDP/FreeRDP/commit/d0bf57c721b28c50d698cd5ffebea46fe86f6507
Patch:          core-message-fix-PolygonSC-and-PolygonCB-async-updates.patch

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
* Sat Aug 22 2026 RHEL Packaging Agent <redhat-ymir-agent@redhat.com> - 2:2.11.7-7.6
- Backport several CVE fixes (CVE-2026-55194, CVE-2026-67288, CVE-2026-67291,
  CVE-2026-67301)
  Resolves: RHEL-225096, RHEL-227729, RHEL-236060, RHEL-246241

* Wed Aug 05 2026 RHEL Packaging Agent <redhat-ymir-agent@redhat.com> - 2:2.11.7-7.5
- Backport several CVE fixes (CVE-2026-64624, CVE-2026-67289, CVE-2026-67299,
  CVE-2026-68580)
  Resolves: RHEL-213169, RHEL-222785, RHEL-222966, RHEL-223605

* Wed Jun 24 2026 RHEL Packaging Agent <redhat-ymir-agent@redhat.com> - 2:2.11.7-7.4
- Fix incorrect bounds checks in planar codec (CVE-2026-45700)
  Resolves: RHEL-186991

* Tue May 05 2026 Ondrej Holy <oholy@redhat.com> - 2:2.11.7-7.3
- Lock appWindow to fix use-after-free in RAIL mode (CVE-2026-25952)
  Resolves: RHEL-159860

* Tue Apr 28 2026 Ondrej Holy <oholy@redhat.com> - 2:2.11.7-7.2
- Fix double free in xf_rail_window_common cleanup (CVE-2026-26986)
- Fix growth of preallocated buffers (CVE-2026-27951)
- Fix heap-buffer-overflow in bitmap_cache_put (CVE-2026-29775)
- Add DSP format checks (CVE-2026-31884)
- Fix DSP array bounds checks (CVE-2026-31883)
- Fix DSP array bounds checks (CVE-2026-31885)
- Update CLEAR_GLYPH_ENTRY::count after alloc (CVE-2026-33985)
  Resolves: RHEL-159816, RHEL-155478, RHEL-161047, RHEL-161482
  Resolves: RHEL-161519, RHEL-161085, RHEL-168463

* Tue Apr 14 2026 Ondrej Holy <oholy@redhat.com> - 2:2.11.7-7.1
- Update CLEAR_VBAR_ENTRY size after alloc (CVE-2026-33984)
- Fail progressive_rfx_quant_sub on invalid values (CVE-2026-33983)
  Resolves: RHEL-163097, RHEL-163113

* Tue Mar 31 2026 Ondrej Holy <oholy@redhat.com> - 2:2.11.7-7
- Fix use of nsc_process_message
  Resolves: RHEL-155994

* Fri Mar 27 2026 Ondrej Holy <oholy@redhat.com> - 2:2.11.7-6
- Backport several CVE fixes
  Resolves: RHEL-148052, RHEL-148053, RHEL-148056, RHEL-148075, RHEL-148081
  Resolves: RHEL-148098, RHEL-148105, RHEL-148106, RHEL-148941, RHEL-149032
  Resolves: RHEL-149043, RHEL-149066, RHEL-155994

* Wed Mar 25 2026 Ondrej Holy <oholy@redhat.com> - 2:2.11.7-5
- Backport several CVE fixes
  Resolves: RHEL-151989, RHEL-152216

* Tue Feb 17 2026 Ondrej Holy <oholy@redhat.com> - 2:2.11.7-4
- Backport several CVE fixes
  Resolves: RHEL-148849, RHEL-148891, RHEL-149030

* Tue Jan 27 2026 Ondrej Holy <oholy@redhat.com> - 2:2.11.7-3
- Backport several CVE fixes
  Resolves: RHEL-142427, RHEL-142411, RHEL-142395, RHEL-142379, RHEL-142363
  Resolves: RHEL-142348, RHEL-142332

* Fri Jan 16 2026 Ondrej Holy <oholy@redhat.com> - 2:2.11.7-2
- Try next DNS entry on connect failure
  Resolves: RHEL-113722

* Thu May 09 2024 Ondrej Holy <oholy@redhat.com> - 2:2.11.7-1
- Update to 2.11.7 (CVE-2024-32039, CVE-2024-32040, CVE-2024-32041,
  CVE-2024-32458, CVE-2024-32459, CVE-2024-32460, CVE-2024-32658,
  CVE-2024-32659, CVE-2024-32660, CVE-2024-32661, CVE-2024-32662)

* Tue Mar 12 2024 Ondrej Holy <oholy@redhat.com> - 2:2.11.2-2
- CVE-2024-22211: Check codec resolution for overflow (RHEL-22244)

* Fri Nov 10 2023 Ondrej Holy <oholy@redhat.com> - 2:2.11.2-1
- Update to 2.11.2 (RHEL-4290, RHEL-4292, RHEL-4296, RHEL-4298, RHEL-4300,
  RHEL-4302, RHEL-4304, RHEL-4306, RHEL-4308, RHEL-4310, RHEL-4312,
  RHEL-10060)

* Tue Dec 13 2022 Ondrej Holy <oholy@redhat.com> - 2:2.4.1-5
- Fix "implicit declaration of function" errors (#2136155, #2145140)

* Thu Dec 08 2022 Ondrej Holy <oholy@redhat.com> - - 2:2.4.1-4
- CVE-2022-39282: Fix length checks in parallel driver (#2136152)
- CVE-2022-39283: Add missing length check in video channel (#2136154)
- CVE-2022-39316, CVE-2022-39317: Add missing length checks in zgfx (#2145140)
- CVE-2022-39318: Fix division by zero in urbdrc channel (#2145140)
- CVE-2022-39319: Add missing length checks in urbdrc channel (#2145140)
- CVE-2022-39320: Ensure urb_create_iocompletion uses size_t (#2145140)
- CVE-2022-39347: Fix path validation in drive channel (#2145140)
- CVE-2022-41877: Add missing length check in drive channel (#2145140)

* Wed Jun 22 2022 Ondrej Holy <oholy@redhat.com> - - 2:2.4.1-3
- Fix gateway functionality with OpenSSL 3.0 (#2023262)

* Fri Nov 26 2021 Ondrej Holy <oholy@redhat.com> - 2:2.4.1-2
- Fix datatype mismatch / big-endian breakage
- Load legacy provider when initializing OpenSSL 3.0

* Wed Nov 10 2021 Ondrej Holy <oholy@redhat.com> - 2:2.4.1-1
- Update to 2.4.1 (CVE-2021-41159, CVE-2021-41160).

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 2:2.4.0-3
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Tue Aug 03 2021 Ondrej Holy <oholy@redhat.com> - 2:2.4.0-2
- Load legacy provider to fix rc4 with OpenSSL 3.0 (#1988443).

* Thu Jul 29 2021 Ondrej Holy <oholy@redhat.com> - 2:2.4.0-1
- Update to 2.4.0.

* Wed Jun 16 2021 Mohan Boddu <mboddu@redhat.com> - 2:2.3.2-2
- Rebuilt for RHEL 9 BETA for openssl 3.0
  Related: rhbz#1971065

* Mon May 17 2021 Ondrej Holy <oholy@redhat.com> - 2:2.3.2-1
- Update to 2.3.2 (#1951123).

* Mon May 17 2021 Ondrej Holy <oholy@redhat.com> - 2:2.2.0-8
- Fix build with OpenSSL 3.0 (#1952937).

* Thu Apr 15 2021 Mohan Boddu <mboddu@redhat.com> - 2:2.2.0-7
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Tue Mar 23 2021 Simone Caronni <negativo17@gmail.com> - 2:2.2.0-6
- Explicitly enable Cairo support (#1938393).

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 11 2020 Ondrej Holy <oholy@redhat.com> - 2:2.2.0-4
- Use %%cmake_ macros to fix out-of-source builds (#1863586)

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.2.0-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 23 2020 Simone Caronni <negativo17@gmail.com> - 2:2.2.0-1
- Update to 2.2.0.

* Tue Jun 30 2020 Simone Caronni <negativo17@gmail.com> - 2:2.1.2-1
- Update to 2.1.2.

* Thu May 21 2020 Ondrej Holy <oholy@redhat.com> - 2:2.1.1-1
- Update to 2.1.1.

* Fri May 15 2020 Ondrej Holy <oholy@redhat.com> - 2:2.1.0-1
- Update to 2.1.0 (#1833540).

* Fri May 15 2020 Pete Walter <pwalter@fedoraproject.org> - 2:2.0.0-57.20200207git245fc60
- Rebuild for ICU 67

* Fri Feb 07 2020 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-56.20200207git245fc60
- Update to latest snapshot.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.0.0-55.20190820git6015229
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 01 2019 Pete Walter <pwalter@fedoraproject.org> - 2:2.0.0-54.20190820git6015229
- Rebuild for ICU 65

* Tue Aug 20 2019 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-53.20190820git6015229
- Update to latest snapshot.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.0.0-52.20190918git5e672d4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jul 21 2019 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-51.20190918git5e672d4
- Update to latest snapshot.

* Sat May 18 2019 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-50.20190517gitb907324
- Update to latest snapshot.

* Wed Mar 06 2019 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-49.20190304git435872b
- Fix for GFX color depth (Windows 10).

* Thu Feb 28 2019 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-48.20190228gitce386c8
- Update to latest snapshot post rc4.
- CVE-2018-1000852 (#1661642).

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.0.0-47.rc4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Nov 29 2018 Ondrej Holy <oholy@redhat.com> - 2:2.0.0-47.rc4
- Update to 2.0.0-rc4

* Mon Oct 15 2018 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-46.20181008git00af869
- Enable Xtest option (#1559606).

* Mon Oct 15 2018 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-45.20181008git00af869
- Update to last snapshot post 2.0.0-rc3.

* Mon Aug 20 2018 Simone Caronni <negativo17@gmail.com> - 2:2.0.0-44.rc3
- Update SPEC file.

* Sat Aug 04 2018 Mike DePaulo <mikedep333@fedoraproject.org> - 2:2.0.0-43.20180801.rc3
- Update to 2.0.0-rc3

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.0.0-42.20180405gita9ecd6a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

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
