%global	debug_package %{nil}

# Don't provide or require internal libs
%global	_privatelibs libjack[.]so.*
%global	__provides_exclude ^(%{_privatelibs})$
%global	__requires_exclude ^(%{_privatelibs})$

%define	__python %{__python3}
%define	oname Carla

%define git 20251009

Summary:		An audio plugin host
Name:	carla
Version:		2.5.10 %dnl Please don't update to the next stable version 2.5.11 etc, but use git snapshot instead. At least until 2.6.0 is released. This is necessary for other applications to work.

Release:		1.%{git}
License:		GPLv2+
Group:	Sound
Url:	https://kxstudio.linuxaudio.org/Applications:Carla
#Source0:	https://github.com/falkTX/Carla/archive/%{oname}-%{version}.tar.gz
# Use git for now (needed by Zrythm) until 2.6.0 version is released
Source0:  Carla-%{version}-%{git}.tar.gz
Patch0:	carla-2.5.10-drop-rpath-from-pkgconfig-files.patch
BuildRequires:		chrpath
BuildRequires:		file
BuildRequires:		python-rdflib
BuildRequires:		python-sip-qt5
BuildRequires:		ffmpeg-devel
BuildRequires:		python-qt5-devel
BuildRequires:		pkgconfig(alsa)
BuildRequires:		pkgconfig(flac)
BuildRequires:		pkgconfig(libmagic)
BuildRequires:		pkgconfig(libpulse)
BuildRequires:		pkgconfig(python)
BuildRequires:		pkgconfig(Qt5Core)
BuildRequires:		pkgconfig(Qt5Gui)
BuildRequires:		pkgconfig(Qt5Network)
BuildRequires:		pkgconfig(Qt5Widgets)
BuildRequires:		pkgconfig(sdl)
BuildRequires:		pkgconfig(sdl2)
BuildRequires:		pkgconfig(sndfile)
BuildRequires:		pkgconfig(vorbisenc)
# For extra native plugins
BuildRequires:		pkgconfig(fftw3)
BuildRequires:		pkgconfig(fluidsynth)
BuildRequires:		pkgconfig(libprojectM)
# Not provided yet
#BuildRequires:	pkgconfig(ntk)
BuildRequires:		pkgconfig(zlib)
# For plugin GUIs
# In Extra
#BuildRequires:		juce
BuildRequires:		pkgconfig(gtk+-2.0)
BuildRequires:		pkgconfig(gtk+-3.0)
BuildRequires:		pkgconfig(x11)
BuildRequires:		pkgconfig(xcursor)
BuildRequires:		pkgconfig(xext)
# For extra samplers support
BuildRequires:		pkgconfig(gig)
BuildRequires:		pkgconfig(liblo)
BuildRequires:		pkgconfig(mxml4)
BuildRequires:		pkgconfig(pkg-config)

Requires:  python-qt5

%description
Carla is an audio plugin host, with support for many audio drivers and plugin
formats. It features automation of parameters via MIDI CC and full OSC
control. It currently supports LADSPA, DSSI, LV2, VST2/3 and AU plugin formats
plus GIG, SF2 and SFZ sounds banks.

%files
%doc INSTALL.md README.md doc
%{_bindir}/%{name}
%{_bindir}/%{name}-control
%{_bindir}/%{name}-database
%{_bindir}/%{name}-jack-multi
%{_bindir}/%{name}-jack-patchbayplugin
%{_bindir}/%{name}-jack-single
%{_bindir}/%{name}-patchbay
%{_bindir}/%{name}-rack
%{_bindir}/%{name}-settings
%{_bindir}/%{name}-single
%{_bindir}/%{name}-osc-gui
%{_libdir}/%{name}/
%{_libdir}/lv2/%{name}.lv2/
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/%{name}-control.desktop
%{_datadir}/applications/%{name}-jack-multi.desktop
%{_datadir}/applications/%{name}-jack-single.desktop
%{_datadir}/applications/%{name}-patchbay.desktop
%{_datadir}/applications/%{name}-rack.desktop
%{_datadir}/icons/hicolor/*x*/apps/%{name}*.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}*.svg
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/appdata/studio.kx.%{name}.appdata.xml

#--------------------------------------------------------------------

%package devel
Summary:		Header files to access Carla's API
Group:	Development/C++
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains header files needed when writing software using
Carla's several APIs.

%files devel
%{_includedir}/%{name}/
%{_libdir}/pkgconfig/%{name}-host-plugin.pc
%{_libdir}/pkgconfig/%{name}-native-plugin.pc
%{_libdir}/pkgconfig/%{name}-standalone.pc
%{_libdir}/pkgconfig/%{name}-utils.pc

#--------------------------------------------------------------------

%package vst
Summary:		CarlaRack and CarlaPatchbay VST plugins
Group:	Sound/Utilities
Requires:	%{name} = %{version}-%{release}

%description vst
This package contains Carla VST plugins, including CarlaPatchbayFX,
CarlaPatchbay, CarlaRackFX, and CarlaRack.

%files vst
%{_libdir}/vst/%{name}.vst/

#--------------------------------------------------------------------

%prep
%autosetup -p1 -n %{oname}-main

# Fix python shebangs
find . -name '*.py' | xargs sed -i '1s|^#!/usr/bin/env python3|#!%{__python}|'


%build
# Avoid "unknown argument" errors
export CC=gcc
export CXX=g++
%set_build_flags
make features
%make_build NOOPT=true


%install
%make_install  -- PREFIX="%{_prefix}" LIBDIR="%{_libdir}" PYVER="%{python3_version}"

# Fix perms
chmod +x %{buildroot}%{_datadir}/%{name}/widgets/*.py
chmod -x %{buildroot}%{_datadir}/%{name}/widgets/__init__.py
chmod +x %{buildroot}%{_datadir}/%{name}/patchcanvas/*.py
chmod -x %{buildroot}%{_datadir}/%{name}/modgui/__init__.py
chmod +x %{buildroot}%{_datadir}/%{name}/externalui.py
chmod +x %{buildroot}%{_datadir}/%{name}/ladspa_rdf.py
chmod +x %{buildroot}%{_datadir}/%{name}/%{name}
chmod +x %{buildroot}%{_datadir}/%{name}/%{name}_*
chmod +x %{buildroot}%{_datadir}/%{name}/%{name}-*

# Fix remaining env shebangs
sed -i '1 s,^#!/usr/bin/env python3,#!%{__python},' %{buildroot}%{_bindir}/carla-single
sed -i '1 s,^#!/usr/bin/env python3,#!%{__python},' %{buildroot}%{_datadir}/%{name}/carla
sed -i '1 s,^#!/usr/bin/env python3,#!%{__python},' %{buildroot}%{_datadir}/%{name}/carla-*
sed -i '1 s,^#!/usr/bin/env python3,#!%{__python},' %{buildroot}%{_datadir}/%{name}/resources/*-ui
sed -i '1 s,^#!/usr/bin/env python3,#!%{__python},' %{buildroot}%{_datadir}/%{name}/resources/carla-*
sed -i '1 s,^#!/usr/bin/env python,#!%{__python},' %{buildroot}%{_datadir}/%{name}/widgets/paramspinbox.py

# Fix rogue rpath
chrpath -d %{buildroot}%{_libdir}/%{name}/libcarla_standalone2.so
