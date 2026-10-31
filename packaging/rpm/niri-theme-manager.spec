Name:           niri-theme-manager
Version:        0.1.0
Release:        1%{?dist}
Summary:        Desktop theme switcher for the Niri compositor
License:        MIT
URL:            https://github.com/Spruhantom/Tomos-niritheme-manager
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-tkinter
Requires:       python3 >= 3.10
%if 0%{?suse_version}
Requires:       python3-tk
%else
Requires:       python3-tkinter
%endif
Recommends:     niri

%description
A small Python/Tkinter desktop application for switching between Neon Blue,
Dark, and Light themes for the Niri Wayland compositor.

%prep
%autosetup -n %{name}-%{version}

%build
# Pure Python application; nothing to compile.

%install
install -Dpm0755 niri-theme-manager %{buildroot}%{_bindir}/niri-theme-manager
install -Dpm0644 niri_theme_manager.py %{buildroot}%{_datadir}/niri-theme-manager/niri_theme_manager.py
install -Dpm0644 niri-theme-manager.desktop %{buildroot}%{_datadir}/applications/niri-theme-manager.desktop
install -Dpm0644 LICENSE %{buildroot}%{_licensedir}/%{name}/LICENSE
install -Dpm0644 README.md %{buildroot}%{_docdir}/%{name}/README.md

%check
python3 -m py_compile niri_theme_manager.py
python3 -m unittest discover -s tests -v

%files
%{_bindir}/niri-theme-manager
%{_datadir}/niri-theme-manager/niri_theme_manager.py
%{_datadir}/applications/niri-theme-manager.desktop
%license %{_licensedir}/%{name}/LICENSE
%doc %{_docdir}/%{name}/README.md

%changelog
* Sat Oct 31 2026 Tom's Tech Support <tom@tomserver.co.uk> - 0.1.0-1
- Initial RPM package.
