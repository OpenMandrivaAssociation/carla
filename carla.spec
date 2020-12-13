%global debug_package %{nil}
%define __python %{__python3}

# Dont provide or require internal libs. Using new rpm builtin filtering
%global _privatelibs libjack[.]so.*
%global __provides_exclude ^(%{_privatelibs})$
%global __requires_exclude ^(%{_privatelibs})$

Name:           carla
Version:        2.2.0
Release:        1
Summary:        An audio plugin host
License:        GPLv2+
Group:          Sound/Utilities
Url:            http://kxstudio.linuxaudio.org/Applications:Carla
Source0:        https://github.com/falkTX/Carla/archive/v%{version}/%{name}-%{version}.tar.gz
Patch0:         python-version.patch
Patch1:         desktop-categories.patch
Patch2:         carla-systemlibs.patch
Patch3:         carla-1.9.12-added-mxml-3.0-compatility-to-XMLwrapper.patch
Patch4:         0001-Add-missing-QPainterPath-include.patch

BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(python)
BuildRequires:  python3-qt5-devel
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(sndfile)
BuildRequires:  pkgconfig(flac)
BuildRequires:  pkgconfig(vorbisenc)

BuildRequires:  file
BuildRequires:  python3-rdflib

# for extra native plugins
BuildRequires:  pkgconfig(fftw3)
BuildRequires:  pkgconfig(fluidsynth)
BuildRequires:  pkgconfig(libprojectM)
BuildRequires:  pkgconfig(ntk)
BuildRequires:  pkgconfig(zlib)
# for plugin GUIs
BuildRequires:  qt4-devel
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(x11)
# for extra samplers support
BuildRequires:  pkgconfig(gig)
BuildRequires:  pkgconfig(liblo)
BuildRequires:  pkgconfig(mxml)
BuildRequires:  pkgconfig(pkg-config)

%description
Carla is an audio plugin host, with support for many audio drivers
and plugin formats. It features automation of parameters via MIDI CC
and full OSC control. It currently supports LADSPA, DSSI, LV2, VST2/3
and AU plugin formats, plus GIG, SF2 and SFZ sounds banks.
It further supports bridging Window plugins using Wine.

%files
%doc INSTALL.md README.md doc
%{_bindir}/carla
%{_bindir}/carla-control
%{_bindir}/carla-database
%{_bindir}/carla-jack-multi
%{_bindir}/carla-jack-single
%{_bindir}/carla-patchbay
%{_bindir}/carla-rack
%{_bindir}/carla-settings
%{_bindir}/carla-single
%{_libdir}/carla/
%{_libdir}/lv2/carla.lv2/
%{_datadir}/carla/
%{_datadir}/applications/carla.desktop
%{_datadir}/applications/carla-control.desktop
%{_datadir}/icons/hicolor/*/apps/carla*.*
%{_datadir}/mime/packages/carla.xml

#--------------------------------------------------------------------
%package devel
Summary:        Header files to access Carla's API
Group:          Development/C++
Requires:       carla = %{version}-%{release}

%description devel
This package contains header files needed when writing software using
Carla's several APIs.

%files devel
%{_includedir}/carla/
%{_libdir}/pkgconfig/carla-native-plugin.pc
%{_libdir}/pkgconfig/carla-standalone.pc
%{_libdir}/pkgconfig/carla-utils.pc

#--------------------------------------------------------------------
%package vst
Summary:        CarlaRack and CarlaPatchbay VST plugins
Group:          Sound/Utilities
Requires:       carla = %{version}-%{release}

%description vst
This package contains Carla VST plugins, including CarlaPatchbayFX,
CarlaPatchbay, CarlaRackFX, and CarlaRack.

%files vst
%{_libdir}/vst/carla.vst/


%prep
%setup -q -n Carla-1.9.14+git20190227.737a0b0f
%autopatch -p1
find . -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'

%build
%set_build_flags
make features
%make_build NOOPT=true

%install

%make_install  -- PREFIX="%{_prefix}" LIBDIR="%{_libdir}" PYVER="%{python3_version}"
# Move arch depended files (wrong installed)
mv %{buildroot}%{_datadir}/carla/resources/zynaddsubfx-ui %{buildroot}%{_libdir}/carla
ln -s %{_libdir}/carla/zynaddsubfx-ui %{buildroot}%{_datadir}/carla/resources/zynaddsubfx-ui
