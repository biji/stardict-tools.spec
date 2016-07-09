#
# spec file for package stardict-tools
#
# Copyright (c) 2011 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

# norootforbuild

# modified by biji for fedora

Name:           stardict-tools
Summary:        StarDict Editor
Version:        3.0.1
Release:        81.1.4
License:        GPL-2.0+
Url:            http://stardict.sourceforge.net
Group:          Productivity/Office/Dictionary
Source:         %{name}-%{version}.tar.bz2
Source1:        %{name}.README.SuSE
Source2:        stardict-editor.png
Source3:        stardict-tools-rpmlintrc
Patch1:         stardict-tools-3.0.1-includes.patch
Patch2:         stardict-tools-3.0.1-destbufferoverflow.patch
Patch3:         stardict-tools-3.0.1-gcc44.patch
#BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  gtk2-devel >= 2.6.0
BuildRequires:  pkgconfig
BuildRequires:  mariadb-devel
BuildRequires:  gcc-c++ pcre-devel
BuildRequires:  dos2unix
BuildRequires:  automake libtool
BuildRequires:  desktop-file-utils
Requires:  dictd-server

%description
This package contains the dictionary conversion tools which can convert
dictionaries of DICT, wquick, mova and pydict to stardict format.



Authors:
--------
    Hu Zheng

%prep
%setup -q
%patch1 -p1
%patch2
%patch3

%build
sed -i 's/ ec50/ /g' src/Makefile.am
sed -i 's/\-L\/usr\/lib\/mysql/\-L\/usr\/lib\/mysql \-L\/usr\/lib64\/mysql /g' src/Makefile.am
autoreconf -fiv
%configure --with-pic --disable-static
LDFLAGS="-L/usr/lib64/mysql -L/usr/lib64/mysql" %{__make} %{?jobs:-j%jobs}

%install
%{makeinstall}
%{__install} -d -m755 %buildroot/%{_libdir}/%{name}
%{__install} -d -m755 %buildroot/%{_datadir}/{%{name},pixmaps,applications}
%{__install} -d -m755 %buildroot/%{_defaultdocdir}/%{name}
pushd src 1>/dev/null
# install noinst_PROGRAMS in libdir
for file in $(grep noinst_PROGRAMS Makefile.am | sed -e 's/noinst_PROGRAMS = //'); do 
	if test -x $file; then 
		if [[ $file == *.exe ]]; then 
			continue; 
		else 
			%{__install} -m755 $file %buildroot/%{_libdir}/%{name}/
		fi; 
	fi
done
# install scripts in sharedir
for file in uyghur2dict.py mkguangyunst.py stmerge.py KangXiZiDian-djvu2tiff.py; do
	#echo '#!/usr/bin/python' > "${file}.tmp"
	#cat "$file" >> "${file}.tmp"
	#mv -f "${file}.tmp" "$file"
    sed -i 's%.*\#\!/usr/bin/python%\#\!/usr/bin/python%' "$file"
	chmod 755 "$file"
done
for file in *.py *.pl *.perl; do
  dos2unix -q -n $file %buildroot/%{_datadir}/%{name}/$file
  sed -i 's|^#!/usr/bin/env python.*|#!/usr/bin/python|' %buildroot/%{_datadir}/%{name}/$file
  chmod 755 %buildroot/%{_datadir}/%{name}/$file
done
popd 1>/dev/null
# install documentation
sed -e "s#__LIBDIR__#%{_libdir}#g" %{SOURCE1} > %buildroot/%{_defaultdocdir}/%{name}/README.SuSE
%{__install} -m644 AUTHORS ChangeLog COPYING README %buildroot/%{_defaultdocdir}/%{name}/
# install desktop entry
%{__install} -m644 %{SOURCE2} %buildroot/%{_datadir}/pixmaps/
#%suse_update_desktop_file -c stardict-editor "Stardict Dictionary Editor" "Editor for stardict dictionaries" stardict-editor stardict-editor.png Office Dictionary

> $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop
desktop-file-edit --set-name='Stardict Editor' --set-icon=stardict-editor --set-key=Exec --set-value=stardict-editor --set-key=Type --set-value=Application $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop
desktop-file-install $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop


%clean
rm -rf %buildroot

%files
%defattr(-, root, root)
%doc %{_defaultdocdir}/%{name}
%{_bindir}/stardict-editor
%{_libdir}/%{name}
%{_datadir}/%{name}
%{_datadir}/pixmaps/stardict-editor.png
%{_datadir}/applications/%{name}.desktop

%changelog
* Sun Nov 20 2011 coolo@suse.com
- add libtool as buildrequire to avoid implicit dependency
* Sun Sep 25 2011 crrodriguez@opensuse.org
- Fix build by linking with libz as well.
* Fri Jun 19 2009 coolo@novell.com
- disable as-needed for this package as it fails to build with it
* Tue Jun  9 2009 coolo@novell.com
- fix build with glibc 2.10
* Fri Mar 20 2009 crrodriguez@suse.de
- fix build with gcc 44
* Wed Oct  8 2008 crrodriguez@suse.de
- fix buffer overflow
* Mon Apr 28 2008 lrupp@suse.de
- update to 3.0.1:
  + Network dictionaries support
  + Plugin system
  + Full-text translation
  + Preliminary WikiPedia dictionary support
  + More powerful dictionary management
  + Babylon dictionaries convertion
  + Many other changes
- fix some compiler issues with gcc4.3:
  stardict-tools-3.0.1-includes.patch
- fix scripts in sharedir
* Mon Jun 18 2007 lrupp@suse.de
- initial version 2.4.8: upstream splitted the tools from the
  main stardict package
