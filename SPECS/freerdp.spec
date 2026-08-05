# Can be rebuilt with FFmpeg/OpenH264 support enabled by passing
# "--with=ffmpeg", or "--with=openh264" to mock/rpmbuild; or by globally
# setting these variables:
# https://bugzilla.redhat.com/show_bug.cgi?id=2242028
#global _with_ffmpeg 1
#global _with_openh264 1

# Can be rebuilt with OpenCL support enabled by passing # "--with=opencl"
# or by globally setting:
#global _opencl 1

# Disable server support in RHEL
# https://bugzilla.redhat.com/show_bug.cgi?id=1639165
%if 0%{?fedora} || 0%{?rhel} >= 10
%global _with_server 1
%endif

# Force uwac to be static to avoid conflicts with freerdp2
# FIXME: Disable this once all freerdp2 consumers are ported to freerdp3
%global _with_static_uwac 1

# Disable unwanted dependencies for RHEL
%{!?rhel:%global _with_sdl_client 1}
%{!?rhel:%global _with_soxr 1}
%{!?rhel:%global _with_uriparser 1}

# Disable support for AAD WebView popup since it uses webkit2gtk-4.0
#global _with_webview 1

Name:           freerdp
Epoch:          2
Version:        3.10.3
Release:        12%{?dist}.7
Summary:        Free implementation of the Remote Desktop Protocol (RDP)

# The effective license is Apache-2.0 but:
# client/SDL/dialogs/font/* is OFL-1.1
# uwac/libuwac/* is HPND
# uwac/protocols/server-decoration.xml is LGPL-2.1-or-later
# winpr/libwinpr/ncrypt/pkcs11-headers/pkcs11.h is LicenseRef-Fedora-Public-Domain
License:        Apache-2.0 AND HPND AND LGPL-2.1-or-later AND LicenseRef-Fedora-Public-Domain AND OFL-1.1
URL:            http://www.freerdp.com/

# The license of the winpr/libwinpr/crt/unicode_builtin.c file is not allowed.
# See: https://gitlab.com/fedora/legal/fedora-license-data/-/issues/498
# Run the ./freerdp_download_and_repack.sh script to prepare tarball.
Source0:        FreeRDP-%{version}-repack.tar.gz
Source1:        freerdp_download_and_repack.sh

# https://bugzilla.redhat.com/show_bug.cgi?id=2365232
Patch0:         Initialize-function-pointers-after-resource-allocation.patch

# https://issues.redhat.com/browse/RHEL-86251
Patch1:         Limit-threadpool-to-16-threads.patch
Patch2:         Use-default-threadpool.patch
Patch3:         Default-minimum-thread-count.patch
Patch4:         Limit-minimum-threadpool-size.patch

# https://issues.redhat.com/browse/RHEL-73724
Patch:          core-connection-print-SSL-warnings-after-init.patch

# https://issues.redhat.com/browse/RHEL-140099
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

# CVE-2026-22853
# https://github.com/FreeRDP/FreeRDP/commit/19f48dc7d615984a24a9be89f50ef9eb8f9bdb6a
Patch:          channels-rdpear-add-checks-for-itemSize.patch

# CVE-2026-22855
# https://github.com/FreeRDP/FreeRDP/commit/57c5647d98c2a026de8b681159cb188ca0439ef8
Patch:          utils-smartcard-add-length-validity-checks.patch

# CVE-2026-22858
# https://github.com/FreeRDP/FreeRDP/commit/62a9e787edb2cfce9858fa4ceda5461680efc590
Patch:          crypto-base64-ensure-char-is-singend.patch

# CVE-2026-22859
# https://github.com/FreeRDP/FreeRDP/commit/7b7e6de8fe427a2f01d331056774aec69710590b
Patch:          channels-urbdrc-check-interface-indices-before-use.patch

# CVE-2026-24678
# https://github.com/FreeRDP/FreeRDP/commit/f3ab1a16139036179d9852745fdade18fec11600
Patch:          channels-rdpecam-ensure-all-streams-are-stopped.patch

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
# https://github.com/FreeRDP/FreeRDP/commit/cb7f295bc750de86480d60a3b58cebc56a57a1c4
# https://github.com/FreeRDP/FreeRDP/commit/635ae3c8193256db01774fab5ff11bcae57aed6b
# https://github.com/FreeRDP/FreeRDP/commit/e01cd85c8003a245ef9778f0eda4b9235514c201
Patch:          channels-drdynvc-reset-channel_callback-before-close.patch
Patch:          channels-drdynvc-check-pointer-before-reset.patch
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

# CVE-2026-24682
# https://github.com/FreeRDP/FreeRDP/commit/1c5c74223179d425a1ce6dbbb6a3dd2a958b7aee
# https://github.com/FreeRDP/FreeRDP/commit/668352a2e241ba017679c11a22ecbe29d0b17401
Patch:          channels-audin-fix-audin_server_recv_formats-cleanup.patch
Patch:          channels-audin-set-error-when-audio_format_read-fail.patch

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

# https://github.com/FreeRDP/FreeRDP/commit/907ca47e40583a7788674bb2f06258edd0c34223
Patch:          winpr-synch-increase-timeout-for-TestSynchCritical.patch

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

# CVE-2026-25997
# https://github.com/FreeRDP/FreeRDP/commit/58409406afe7c2a8a71ed2dc8e22075be4f41c0c
# https://github.com/FreeRDP/FreeRDP/commit/4c9f7e8a7129c8be15f6e2686559d3f17936677d
Patch:          client-x11-fix-clipboard-update.patch
Patch:          client-x11-fix-residual-race-in-xf_clipboard_formats_free.patch

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

# CVE-2026-33987
# https://github.com/FreeRDP/FreeRDP/commit/1a890eb43492b5eb707cb3dd6fc908f696e8fc1c
Patch:          cache-persistent-update-persistent_cache_entry-size-after-realloc.patch

# CVE-2026-33985
# https://github.com/FreeRDP/FreeRDP/commit/c49d1ad43b8c7b32794d0250f2623c2dccd7ef25
Patch:          codec-clear-update-clear_glyph_entry-count-after-alloc.patch

# CVE-2026-33982
# https://github.com/FreeRDP/FreeRDP/commit/a48dbde2c8a5b8b70a9d1c045d969a71afd6284c
Patch:          cache-persist-use-winpr_aligned_calloc.patch

# CVE-2026-25952
# https://github.com/FreeRDP/FreeRDP/commit/1994e9844212a6dfe0ff12309fef520e888986b5
# https://github.com/FreeRDP/FreeRDP/commit/78fd7f580d5f9e6d9d582d82e5ea96003844fbdf
# https://github.com/FreeRDP/FreeRDP/commit/4ff57b68c2960fa414d03c78ff0e0660be1cc5bd
# https://github.com/FreeRDP/FreeRDP/commit/a278ff74117444c635c50ffa5084ecf517171f5a
Patch:          client-x11-lock-appwindow.patch
Patch:          client-x11-improve-rails-window-locking.patch
Patch:          client-x11-refactor-locking.patch
Patch:          client-x11-fix-deadlock-on-output-expose.patch

# CVE-2026-40033
# https://github.com/FreeRDP/FreeRDP/commit/f951d8677ce6d34d9778b951f73b3072b01853cb
Patch:          gdi-gfx-fix-bounds-checks.patch

# CVE-2026-44421
# https://github.com/FreeRDP/FreeRDP/commit/b877c8c0fef1b5ccda29ccd5a1a58696486545ed
Patch:          gdi-gfx-ensure-the-cache-element-can-hold-the-data.patch

# CVE-2026-45700
# https://github.com/FreeRDP/FreeRDP/commit/4a065a941ae134a0433d1497c03b3c3eb91b9f85
Patch:          codec-planar-fix-bounds-checks.patch

# CVE-2026-44420
# https://github.com/FreeRDP/FreeRDP/commit/0fba1f4dbff7585c9c99873d7c07d7dac46510c3
# https://github.com/FreeRDP/FreeRDP/commit/d00dc5d3be369fb400344eb12e6882db2ee184f0
Patch:          channels-cliprdr-validate-capabilitySetLength-in-server-caps.patch
Patch:          channels-cliprdr-abort-on-duplicate-caps.patch

# CVE-2026-44422
# https://github.com/FreeRDP/FreeRDP/commit/668fcb49d4856fad28f685db54a572af2a284b50
# https://github.com/FreeRDP/FreeRDP/commit/ae03a9ff981ce7be1ab09dba2cd319d54984f910
Patch:          channels-rdpear-fix-ndr_read-checks.patch
Patch:          channels-rdpear-disable-ndr-pointer-aliasing.patch

# CVE-2026-55827
# https://github.com/FreeRDP/FreeRDP/pull/12899
# https://github.com/FreeRDP/FreeRDP/commit/7bbb52a193deed5943a041c9859db7ee036044a4
# https://github.com/FreeRDP/FreeRDP/commit/3c4ae49f38aa0ea9b073025eb468131375e518ff
Patch:          core-orders-add-codecID-checks.patch
Patch:          gdi-graphics-fix-gdi_Bitmap_Decompress.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  alsa-lib-devel
BuildRequires:  cmake >= 3.13
BuildRequires:  cups-devel
BuildRequires:  gsm-devel
BuildRequires:  lame-devel
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

BuildRequires:  cmake(json-c)
# Packaging error led to cmake files in the wrong place
# Fixed in https://src.fedoraproject.org/rpms/uriparser/c/1b07302bfc80983fbf84283783370e8338d36429
%{?_with_uriparser:BuildRequires:  (cmake(uriparser) and uriparser-devel)}

BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(krb5)
BuildRequires:  pkgconfig(fdk-aac)
BuildRequires:  pkgconfig(fuse3)
BuildRequires:  pkgconfig(libpcsclite)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(opus)
%{?_with_sdl_client:BuildRequires:  pkgconfig(sdl2)}
%{?_with_sdl_client:BuildRequires:  pkgconfig(SDL2_ttf)}
%{?_with_soxr:BuildRequires:  pkgconfig(soxr)}
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-scanner)
%{?_with_webview:BuildRequires:  pkgconfig(webkit2gtk-4.0)}
BuildRequires:  pkgconfig(xkbcommon)

%{?_with_ffmpeg:
BuildRequires:  pkgconfig(libavcodec) >= 57.48.101
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswscale)
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
Requires:       cmake >= 3.13

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
Requires:       cmake >= 3.13

%description -n libwinpr-devel
The %{name}-libwinpr-devel package contains libraries and header files for
developing applications that use %{name}-libwinpr.

%prep
%autosetup -p1 -n FreeRDP-%{version}

# Rpmlint fixes
find . -name "*.h" -exec chmod 664 {} \;
find . -name "*.c" -exec chmod 664 {} \;

%build
%cmake \
    -DBUILD_TESTING=ON \
    -DCMAKE_SKIP_INSTALL_RPATH=ON \
    -DCMAKE_INSTALL_LIBDIR:PATH=%{_lib} \
    -DWITH_ALSA=ON \
    -DWITH_AAD=ON \
    -DWITH_CAIRO=ON \
    -DWITH_CUPS=ON \
    -DWITH_CHANNELS=ON \
    -DWITH_CLIENT=ON \
    -DWITH_CLIENT_SDL=%{?_with_sdl_client:ON}%{?!_with_sdl_client:OFF} \
    -DWITH_DSP_FFMPEG=%{?_with_ffmpeg:ON}%{?!_with_ffmpeg:OFF} \
    -DWITH_FDK_AAC=ON \
    -DWITH_FFMPEG=%{?_with_ffmpeg:ON}%{?!_with_ffmpeg:OFF} \
    -DWITH_FUSE=ON \
    -DWITH_GSM=ON \
    -DWITH_IPP=OFF \
    -DWITH_JPEG=ON \
    -DWITH_JSONC_REQUIRED=ON \
    -DWITH_KEYBOARD_LAYOUT_FROM_FILE=ON \
    -DWITH_KRB5=ON \
    -DWITH_LAME=ON \
    -DWITH_MANPAGES=ON \
    -DWITH_OPENCL=%{?_with_opencl:ON}%{?!_with_opencl:OFF} \
    -DWITH_OPENH264=%{?_with_openh264:ON}%{?!_with_openh264:OFF} \
    -DWITH_OPENSSL=ON \
    -DWITH_OPUS=ON \
    -DWITH_PCSC=ON \
    -DWITH_PKCS11=ON \
    -DWITH_PULSE=ON \
    -DWITH_SAMPLE=OFF \
    -DWITH_SERVER=%{?_with_server:ON}%{?!_with_server:OFF} \
    -DWITH_SERVER_INTERFACE=%{?_with_server:ON}%{?!_with_server:OFF} \
    -DWITH_SHADOW_X11=%{?_with_server:ON}%{?!_with_server:OFF} \
    -DWITH_SHADOW_MAC=%{?_with_server:ON}%{?!_with_server:OFF} \
    -DWITH_SOXR=%{?_with_soxr:ON}%{?!_with_soxr:OFF} \
    -DWITH_SWSCALE=%{?_with_ffmpeg:ON}%{?!_with_ffmpeg:OFF} \
    -DWITH_TIMEZONE_COMPILED=OFF \
    -DWITH_TIMEZONE_FROM_FILE=ON \
    -DWITH_URIPARSER=%{?_with_uriparser:ON}%{?!_with_uriparser:OFF} \
    -DWITH_VERBOSE_WINPR_ASSERT=OFF \
    -DWITH_VIDEO_FFMPEG=%{?_with_ffmpeg:ON}%{?!_with_ffmpeg:OFF} \
    -DWITH_WAYLAND=ON \
    -DWITH_WEBVIEW=%{?_with_webview:ON}%{?!_with_webview:OFF} \
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
    -DUWAC_FORCE_STATIC_BUILD=%{?_with_static_uwac:ON}%{?!_with_static_uwac:OFF} \
    -DWINPR_UTILS_IMAGE_PNG=ON \
    -DWINPR_UTILS_IMAGE_WEBP=ON \
    -DWINPR_UTILS_IMAGE_JPEG=ON \
    %{nil}

%cmake_build

%check
export CTEST_OUTPUT_ON_FAILURE=1
%cmake_build --target test

%install
%cmake_install

find %{buildroot} -name "*.a" -delete

%multilib_fix_c_header --file %{_includedir}/freerdp3/freerdp/build-config.h

%files
%{?_with_sdl_client:
%{_bindir}/sdl-freerdp
}
%{_bindir}/winpr-hash
%{_bindir}/winpr-makecert
%{_bindir}/wlfreerdp
%{_bindir}/xfreerdp
%{?_with_sdl_client:
%{_mandir}/man1/sdl-freerdp.1*
}
%{_mandir}/man1/winpr-hash.1*
%{_mandir}/man1/winpr-makecert.1*
%{_mandir}/man1/wlfreerdp.1*
%{_mandir}/man1/xfreerdp.1*

%files libs
%license LICENSE
%doc README.md ChangeLog
%{_datadir}/FreeRDP/
%{_libdir}/freerdp3/
%{_libdir}/libfreerdp-client3.so.*
%{?_with_server:
%{_libdir}/libfreerdp-server3.so.*
%{_libdir}/libfreerdp-server-proxy3.so.*
%{_libdir}/libfreerdp-shadow3.so.*
%{_libdir}/libfreerdp-shadow-subsystem3.so.*
}
%{_libdir}/libfreerdp3.so.*
%{?!_with_static_uwac:
%{_libdir}/libuwac0.so.*
}
%{_libdir}/librdtk0.so.*
%{_mandir}/man7/wlog.*

%files devel
%{_includedir}/freerdp3/
%{?!_with_static_uwac:
%{_includedir}/uwac0/
}
%{_includedir}/rdtk0/
%{_libdir}/cmake/FreeRDP3/
%{_libdir}/cmake/FreeRDP-Client3/
%{?_with_server:
%{_libdir}/cmake/FreeRDP-Proxy3/
%{_libdir}/cmake/FreeRDP-Server3/
%{_libdir}/cmake/FreeRDP-Shadow3/
}
%{?!_with_static_uwac:
%{_libdir}/cmake/uwac0/
}
%{_libdir}/cmake/rdtk0/
%{_libdir}/libfreerdp-client3.so
%{?_with_server:
%{_libdir}/libfreerdp-server3.so
%{_libdir}/libfreerdp-server-proxy3.so
%{_libdir}/libfreerdp-shadow3.so
%{_libdir}/libfreerdp-shadow-subsystem3.so
}
%{_libdir}/libfreerdp3.so
%{?!_with_static_uwac:
%{_libdir}/libuwac0.so
}
%{_libdir}/librdtk0.so
%{_libdir}/pkgconfig/freerdp3.pc
%{_libdir}/pkgconfig/freerdp-client3.pc
%{?_with_server:
%{_libdir}/pkgconfig/freerdp-server3.pc
%{_libdir}/pkgconfig/freerdp-server-proxy3.pc
%{_libdir}/pkgconfig/freerdp-shadow3.pc
}
%{?!_with_static_uwac:
%{_libdir}/pkgconfig/uwac0.pc
}
%{_libdir}/pkgconfig/rdtk0.pc

%{?_with_server:
%files server
%{_bindir}/freerdp-proxy
%{_bindir}/freerdp-shadow-cli
%{_mandir}/man1/freerdp-proxy.1*
%{_mandir}/man1/freerdp-shadow-cli.1*
}

%files -n libwinpr
%license LICENSE
%doc README.md ChangeLog
%{_datadir}/WinPR/
%{_libdir}/libwinpr3.so.*
%{_libdir}/libwinpr-tools3.so.*

%files -n libwinpr-devel
%{_libdir}/cmake/WinPR3/
%{_libdir}/cmake/WinPR-tools3/
%{_includedir}/winpr3/
%{_libdir}/libwinpr3.so
%{_libdir}/libwinpr-tools3.so
%{_libdir}/pkgconfig/winpr3.pc
%{_libdir}/pkgconfig/winpr-tools3.pc

%changelog
* Sat Jul 11 2026 RHEL Packaging Agent <redhat-ymir-agent@redhat.com> - 2:3.10.3-12.7
- Add codecID checks for CACHE_BITMAP_V3_ORDER (CVE-2026-55827)
- Fix boundary checks in gdi_Bitmap_Decompress (CVE-2026-55827)
  Resolves: RHEL-194327

* Mon Jun 29 2026 Ondrej Holy <oholy@redhat.com> - 2:3.10.3-12.6
- Backport several CVE fixes (CVE-2026-40033, CVE-2026-44420, CVE-2026-44421,
  CVE-2026-44422, CVE-2026-45700)
  Resolves: RHEL-186978, RHEL-186967, RHEL-186958, RHEL-186950, RHEL-186093

* Tue May 05 2026 Ondrej Holy <oholy@redhat.com> - 2:3.10.3-12.5
- Lock appWindow to fix use-after-free in RAIL mode (CVE-2026-25952)
  Resolves: RHEL-159848

* Wed Apr 29 2026 Ondrej Holy <oholy@redhat.com> - 2:3.10.3-12.4
- Fix double free in xf_rail_window_common cleanup (CVE-2026-26986)
- Fix clipboard use-after-free during auto-reconnect (CVE-2026-25997)
- Fix heap-buffer-overflow in bitmap_cache_put (CVE-2026-29775)
- Add DSP format checks (CVE-2026-31884)
- Fix DSP array bounds checks (CVE-2026-31883)
- Fix DSP array bounds checks (CVE-2026-31885)
- Update PERSISTENT_CACHE_ENTRY::size after realloc (CVE-2026-33987)
- Update CLEAR_GLYPH_ENTRY::count after alloc (CVE-2026-33985)
- Use winpr_aligned_calloc in persistent cache (CVE-2026-33982)
  Resolves: RHEL-159804, RHEL-159660, RHEL-161034, RHEL-161469
  Resolves: RHEL-161505, RHEL-161072, RHEL-163654, RHEL-168462, RHEL-162931

* Fri Apr 10 2026 Ondrej Holy <oholy@redhat.com> - 2:3.10.3-12.2
- Update CLEAR_VBAR_ENTRY size after alloc (CVE-2026-33984)
- Fail progressive_rfx_quant_sub on invalid values (CVE-2026-33983)
  Resolves: RHEL-162947, RHEL-162963

* Thu Apr 09 2026 Ondrej Holy <oholy@redhat.com> - 2:3.10.3-12.1
- Rebuilt for errata
  Resolves: RHEL-155980

* Tue Mar 31 2026 Ondrej Holy <oholy@redhat.com> - 2:3.10.3-12
- Fix use of nsc_process_message
- Increase timeout for TestSynchCritical
  Resolves: RHEL-155980

* Fri Mar 27 2026 Ondrej Holy <oholy@redhat.com> - 2:3.10.3-11
- Backport several CVE fixes
  Resolves: RHEL-147950, RHEL-147951, RHEL-147966, RHEL-147967, RHEL-147971
  Resolves: RHEL-147997, RHEL-147998, RHEL-148006, RHEL-148007, RHEL-148900
  Resolves: RHEL-148986, RHEL-148989, RHEL-149053, RHEL-155980

* Wed Mar 25 2026 Ondrej Holy <oholy@redhat.com> - 2:3.10.3-10
- Backport several CVE fixes
  Resolves: RHEL-151976, RHEL-152203

* Tue Feb 17 2026 Ondrej Holy <oholy@redhat.com> - 2:3.10.3-9
- Backport several CVE fixes
  Resolves: RHEL-147913, RHEL-148817, RHEL-148861, RHEL-148977, RHEL-148894

* Tue Jan 27 2026 Ondrej Holy <oholy@redhat.com> - 2:3.10.3-8
- Backport several CVE fixes
  Resolves: RHEL-142414, RHEL-142398, RHEL-142382, RHEL-142366, RHEL-142350
  Resolves: RHEL-142334, RHEL-142318

* Fri Jan 16 2026 Ondrej Holy <oholy@redhat.com> - 2:3.10.3-7
- Try next DNS entry on connect failure
  Resolves: RHEL-140099

* Tue Dec 16 2025 Ondrej Holy <oholy@redhat.com> - 2:3.10.3-6
- Fix broken SSL checks and disable runtime checks (RHEL-73724)

* Tue Sep 30 2025 Marek Kasik <mkasik@redhat.com> - 2:3.10.3-5
- Silence abidiff
- Resolves: RHEL-86251

* Mon Sep 29 2025 Marek Kasik <mkasik@redhat.com> - 2:3.10.3-4
- Limit threadpool to 16 threads
- Resolves: RHEL-86251

* Mon Jun 16 2025 Marek Kasik <mkasik@redhat.com> - 2:3.10.3-3
- Initialize function pointers after resource allocation
- Fixes CVE-2025-4478
- Resolves: RHEL-91583

* Tue Dec 17 2024 Ondrej Holy <oholy@redhat.com> - 2:3.10.3-1
- Update to 3.10.3

* Thu Nov 14 2024 Ondrej Holy <oholy@redhat.com> - 2:3.9.0-1
- Update to 3.9.0

* Tue Oct 29 2024 Troy Dawson <tdawson@redhat.com> - 2:3.8.0-2
- Bump release for October 2024 mass rebuild:
  Resolves: RHEL-64018

* Thu Sep 05 2024 Ondrej Holy <oholy@redhat.com> - 2:3.8.0-1
- Update to 3.8.0

* Thu Aug 08 2024 Neal Gompa <ngompa@fedoraproject.org> - 2:3.7.0-1
- Update to 3.7.0

* Fri Jul 26 2024 Ondrej Holy <oholy@redhat.com> - 2:3.6.3-1
- Update to 3.6.3 (#2299253)

* Tue Jul 23 2024 Neal Gompa <ngompa@fedoraproject.org> - 2:3.6.2-2
- Include freerdp source download script in SRPM

* Mon Jul 08 2024 Ondrej Holy <oholy@redhat.com> - 2:3.6.2-1
- Update to 3.6.2

* Mon Jul 08 2024 Ondrej Holy <oholy@redhat.com> - 2:3.5.1-3
- Remove file with non-allowed license from the tarball

* Mon Jun 24 2024 Troy Dawson <tdawson@redhat.com> - 2:3.5.1-2
- Bump release for June 2024 mass rebuild

* Tue May 07 2024 Ondrej Holy <oholy@redhat.com> - 2:3.5.1-1
- Update to 3.5.1 (CVE-2024-32039, CVE-2024-32040, CVE-2024-32041,
  CVE-2024-32458, CVE-2024-32459, CVE-2024-32460, CVE-2024-32658,
  CVE-2024-32659, CVE-2024-32660, CVE-2024-32661, CVE-2024-32662)

* Mon Mar 25 2024 Ondrej Holy <oholy@redhat.com> - 2:3.4.0-2
- Disable unwanted dependencies for RHEL

* Fri Mar 22 2024 Ondrej Holy <oholy@redhat.com> - 2:3.4.0-1
- Update to 3.4.0

* Thu Feb 22 2024 Neal Gompa <ngompa@fedoraproject.org> - 2:3.3.0-1
- Update to 3.3.0

* Thu Feb 01 2024 Ondrej Holy <oholy@redhat.com> - 2:3.2.0-4
- Enable KRB5 support

* Wed Jan 31 2024 Pete Walter <pwalter@fedoraproject.org> - 2:3.2.0-3
- Rebuild for ICU 74

* Sat Jan 27 2024 Neal Gompa <ngompa@fedoraproject.org> - 2:3.2.0-2
- Force static libuwac to deconflict with freerdp2

* Wed Jan 24 2024 Neal Gompa <ngompa@fedoraproject.org> - 2:3.2.0-1
- Rebase to 3.2.0

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.11.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.11.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 12 2024 Ondrej Holy <oholy@redhat.com> - 2:2.11.4-1
- Update to 2.11.4.

* Wed Oct 25 2023 Ondrej Holy <oholy@redhat.com> - 2:2.11.2-3
- Disable FFmpeg support (#2242028).

* Mon Oct 09 2023 John Wiele <jwiele@redhat.com> - 2:2.11.2-2
- Enable optional build with OpenCL support.

* Wed Sep 27 2023 Ondrej Holy <oholy@redhat.com> - 2:2.11.1-2
- Update to 2.11.2.

* Tue Sep 05 2023 Ondrej Holy <oholy@redhat.com> - 2:2.11.1-1
- Update to 2.11.1.

* Fri Sep 01 2023 Ondrej Holy <oholy@redhat.com> - 2:2.11.0-1
- Update to 2.11.0 (CVE-2023-39350, CVE-2023-39351, CVE-2023-39352,
  CVE-2023-39353, CVE-2023-39354, CVE-2023-39356, CVE-2023-40181,
  CVE-2023-40186, CVE-2023-40188, CVE-2023-40567, CVE-2023-40569 and
  CVE-2023-40589).

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 František Zatloukal <fzatlouk@redhat.com> - 2:2.10.0-3
- Rebuilt for ICU 73.2

* Thu May 11 2023 Ondrej Holy <oholy@redhat.com> - 2:2.10.0-2
- Enable recommended FFmpeg support.

* Tue Feb 21 2023 Ondrej Holy <oholy@redhat.com> - 2:2.10.0-1
- Update to 2.10.0.

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Dec 31 2022 Pete Walter <pwalter@fedoraproject.org> - 2:2.9.0-2
- Rebuild for ICU 72

* Wed Nov 30 2022 Ondrej Holy <oholy@redhat.com> - 2:2.9.0-1
- Update to 2.9.0 (CVE-2022-39316, CVE-2022-39317, CVE-2022-39318,
CVE-2022-39319, CVE-2022-39320, CVE-2022-41877, CVE-2022-39347).

* Mon Nov 14 2022 Ondrej Holy <oholy@redhat.com> - 2:2.8.1-1
- Update to 2.8.1 (CVE-2022-39282, CVE-2022-39283).

* Mon Aug 15 2022 Simone Caronni <negativo17@gmail.com> - 2:2.8.0-1
- Update to 2.8.0.

* Wed Aug 03 2022 Ondrej Holy <oholy@redhat.com> - 2:2.7.0-4
- Enable server support in ELN.

* Mon Aug 01 2022 Frantisek Zatloukal <fzatlouk@redhat.com> - 2:2.7.0-3
- Rebuilt for ICU 71.1

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Apr 25 2022 Ondrej Holy <oholy@redhat.com> - 2:2.7.0-1
- Update to 2.7.0.

* Fri Mar 11 2022 Ondrej Holy <oholy@redhat.com> - 2:2.6.1-1
- Update to 2.6.1.

* Thu Feb 03 2022 Ondrej Holy <oholy@redhat.com> - 2:2.5.0-1
- Update to 2.5.0.

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Nov 26 2021 Ondrej Holy <oholy@redhat.com> - 2:2.4.1-2
- Fix datatype mismatch / big-endian breakage
- Load legacy provider when initializing OpenSSL 3.0

* Wed Nov 10 2021 Ondrej Holy <oholy@redhat.com> - 2:2.4.1-1
- Update to 2.4.1 (CVE-2021-41159, CVE-2021-41160).

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 2:2.4.0-3
- Rebuilt with OpenSSL 3.0.0

* Wed Aug 11 2021 Ondrej Holy <oholy@redhat.com> - 2:2.4.0-2
- Preparation for OpenSSL 3.0

* Thu Jul 29 2021 Ondrej Holy <oholy@redhat.com> - 2:2.4.0-1
- Update to 2.4.0.

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed May 19 2021 Pete Walter <pwalter@fedoraproject.org> - 2:2.3.2-2
- Rebuild for ICU 69

* Thu Apr 15 2021 Simone Caronni <negativo17@gmail.com> - 2:2.3.2-1
- Update to 2.3.2.

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
