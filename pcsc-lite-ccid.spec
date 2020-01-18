%global dropdir %(pkg-config libpcsclite --variable usbdropdir 2>/dev/null)
%global pcsc_lite_ver 1.8.3
%global upstream_build 3897

Name:           pcsc-lite-ccid
Version:        1.4.10
Release:        14%{?dist}
Summary:        Generic USB CCID smart card reader driver

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://pcsclite.alioth.debian.org/ccid.html
Source0:        http://alioth.debian.org/download.php/%{upstream_build}/ccid-%{version}.tar.bz2
Patch1:         ccid-1.4.10-voltage.patch
Patch2:		ccid-1.4.10-omnikey-3121.patch
Patch3:		ccid-1.4.10-maxreaders.patch
Patch4:		ccid-1.4.10-yubikey.patch
Patch5:		ccid-readers-3.4.20.patch
Patch6:		ccid-1.4.10-max-cpu-bug.patch
Patch7:		ccid-1.4.10-broadcom.patch
Patch8:		ccid-1.4.10-add-1.4.29-readers.patch
Patch9:		ccid-1.4.10-coverity.patch

BuildRequires:  libusb1-devel
BuildRequires:  pcsc-lite-devel >= %{pcsc_lite_ver}
Requires(post): systemd
Requires(postun): systemd
Requires:       pcsc-lite >= %{pcsc_lite_ver}
Provides:       pcsc-ifd-handler
# Provide upgrade path from 'ccid' package
Obsoletes:      ccid < 1.4.0-3
Provides:       ccid = %{version}-%{release}

%description
Generic USB CCID (Chip/Smart Card Interface Devices) driver for use with the
PC/SC Lite daemon.


%prep
%setup -q -n ccid-%{version}
%patch1 -b .voltage 
%patch2 -b .omnikey
%patch3 -b .maxreaders
%patch4 -b .yubikey
%patch5 -b .yubikey_2
%patch6 -b .max_cpu_bug
%patch7 -b .broadcom
%patch8 -b .add_1_4_29_readers
%patch9 -b .coverity


%build
%configure --enable-twinserial
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT
cp -p src/openct/LICENSE LICENSE.openct
rm -rf $RPM_BUILD_ROOT/%{_sysconfdir}/reader.conf.d


%post
/bin/systemctl try-restart pcscd.service >/dev/null 2>&1 || :

%postun
/bin/systemctl try-restart pcscd.service >/dev/null 2>&1 || :


%files
%doc AUTHORS ChangeLog COPYING LICENSE.openct README
%{dropdir}/ifd-ccid.bundle/
%{dropdir}/serial/


%changelog
* Wed May 23 2018 Robert Relyea <rrelyea@redhat.com - 1.4.10-14
- fix coverity issues. Fixes are already upstream

* Mon May 21 2018 Robert Relyea <rrelyea@redhat.com - 1.4.10-13.1
- Add support for 1.4.29 readers

* Tue Sep 5 2017 Robert Relyea <rrelyea@redhat.com - 1.4.10-13
- Add support for missing readers (broadcom, cherry).
- mark deprecated readers as unsupported and needing an update

* Thu Jun 23 2016 Robert Relyea <rrelyea@redhat.com - 1.4.10-12
- Fix cpu busy waiting if the last USB device has been removed.

* Thu Jun 23 2016 Robert Relyea <rrelyea@redhat.com - 1.4.10-11
- Add support for missing readers (mostly yubikey 4)

* Mon Jul 6 2015 Robert Relyea <rrelyea@redhat.com - 1.4.10-10
- fix corrupted patch

* Mon Jul 6 2015 Robert Relyea <rrelyea@redhat.com - 1.4.10-9
- Add support for YubiKey

* Mon Jul 6 2015 Robert Relyea <rrelyea@redhat.com - 1.4.10-8
- Allow more access to more readers.

* Thu Sep 25 2014 Robert Relyea <rrelyea@redhat.com - 1.4.10-7
- Allow longer apdu messages on omnikey.

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.4.10-5
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.4.10-4
- Mass rebuild 2013-12-27

* Tue Nov 26 2013 Robert Relyea <rrelyea@redat.com> - 1.4.10-3
- bring in voltage patch

* Thu Oct 24 2013 Robert Relyea <rrelyea@redat.com> - 1.4.10-2
- rpmdiff cleanups

* Wed Apr 17 2013 Kalev Lember <kalevlember@gmail.com> - 1.4.10-1
- Update to 1.4.10

* Thu Feb 28 2013 Kalev Lember <kalevlember@gmail.com> - 1.4.9-1
- Update to 1.4.9

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Oct 07 2012 Kalev Lember <kalevlember@gmail.com> - 1.4.8-1
- Update to 1.4.8

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 26 2012 Kalev Lember <kalevlember@gmail.com> - 1.4.7-1
- Update to 1.4.7

* Sat Apr 07 2012 Kalev Lember <kalevlember@gmail.com> - 1.4.6-1
- Update to 1.4.6

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 14 2011 Kalev Lember <kalevlember@gmail.com> - 1.4.5-1
- Update to 1.4.5
- Switch to systemctl for restarting pcscd after upgrade now that it is using
  native systemd unit files.

* Fri May 27 2011 Kalev Lember <kalev@smartlink.ee> - 1.4.4-1
- Update to 1.4.4
- Clean up the spec file for modern rpmbuild

* Sat Apr 02 2011 Kalev Lember <kalev@smartlink.ee> - 1.4.3-1
- Update to 1.4.3
- GPLv2+ licensed RSA_SecurID no longer gets installed, which changes
  the license of the binary RPM from 'LGPLv2+ and GPLv2+' to 'LGPLv2+'.

* Tue Mar 29 2011 Kalev Lember <kalev@smartlink.ee> - 1.4.2-2
- Don't install the udev rules

* Fri Feb 25 2011 Kalev Lember <kalev@smartlink.ee> - 1.4.2-1
- Update to 1.4.2

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 13 2010 Kalev Lember <kalev@smartlink.ee> - 1.4.1-1
- Update to 1.4.1

* Thu Dec 09 2010 Kalev Lember <kalev@smartlink.ee> - 1.4.0-4
- Install src/openct/LICENSE file as LICENSE.openct in docs (#660600)
- Added 'and GPLv2+' to license tag to cover RSA_SecurID (#660600)

* Tue Dec 07 2010 Kalev Lember <kalev@smartlink.ee> - 1.4.0-3
- Renamed ccid package to pcsc-lite-ccid (#654377)
- Mark files under reader.conf.d as config(noreplace)
- Don't mark udev rules as config

* Tue Dec 07 2010 Kalev Lember <kalev@smartlink.ee> - 1.4.0-2
- Removed ExcludeArch: s390 s390x as these arches now have libusb1
- Updated description

* Wed Aug 04 2010 Kalev Lember <kalev@smartlink.ee> - 1.4.0-1
- Update to 1.4.0
- Build against libusb1 instead of libusb 0.1
- Install libccidtwin configuration file
- Spec file clean up

* Sun Jul 04 2010 Kalev Lember <kalev@smartlink.ee> - 1.3.13-1
- Update to 1.3.13

* Thu Nov 19 2009 Kalev Lember <kalev@smartlink.ee> - 1.3.11-1
- Updated to ccid 1.3.11
- Removed iso-8859-1 to utf-8 conversion as the files are in utf-8 now

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Bob Relyea <rrelyea@redhat.com> - 1.3.9-1
- update to ccid 1.3.9

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Aug 26 2008 Bob Relyea <rrelyea@redhat.com> - 1.3.8-1
- update to ccid 1.3.8

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.1-4
- Autorebuild for GCC 4.3

* Tue Aug 21 2007 Bob Relyea <rrelyea@redhat.com> - 1.2.1-3
- Update License description to the new Fedora standard

* Mon Apr 30 2007 Bob Relyea <rrelyea@redhat.com> - 1.2.1-2
- Fix the missed use of the version macro

* Tue Feb 06 2007 Bob Relyea <rrelyea@redhat.com> - 1.2.1-1
- Pick up ccid 1.2.1
- use pcscd 'hotplug' feature instead of restarting the daemon
- add enable_udev

* Mon Nov 06 2006 Bob Relyea <rrelyea@redhat.com> - 1.1.0-2
- Fix version macro to remove '-'

* Thu Nov 02 2006 Bob Relyea <rrelyea@redhat.com> - 1.1.0-1
- Pickup ccid 1.1.0

* Wed Jul 19 2006 Florian La Roche <laroche@redhat.com> - 1.0.1-5
- require initscripts for post/postun

* Sun Jul 16 2006 Florian La Roche <laroche@redhat.com> - 1.0.1-4
- fix excludearch line

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.0.1-3.1
- rebuild

* Mon Jul 10 2006 Bob Relyea <rrelyea@redhat.com> - 1.0.1-3
- remove s390 from the build

* Mon Jun  5 2006 Bob Relyea <rrelyea@redhat.com> - 1.0.1-2
- Move to Fedora Core, removed %%{_dist}.

* Sat Apr 22 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.0.1-1
- 1.0.1.

* Mon Mar  6 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.0.0-1
- 1.0.0, license changed to LGPL.

* Wed Feb 15 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.4.1-7
- Rebuild.

* Thu Nov  3 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.4.1-6
- Clean up build dependencies.
- Convert docs to UTF-8.

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.4.1-5
- rebuilt

* Fri Feb 25 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.4.1-4
- Drop Epoch: 0.
- Improve summary.
- Build with dependency tracking disabled.

* Thu Jul  1 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.4.1-0.fdr.3
- Restart pcscd in post(un)install phase if it's available and running.

* Thu May 13 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.4.1-0.fdr.2
- Provide pcsc-ifd-handler (idea from Debian).

* Sat Feb 14 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.4.1-0.fdr.1
- Update to 0.4.1.

* Fri Feb 13 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.4.0-0.fdr.1
- Update to 0.4.0.

* Wed Nov  5 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.3.2-0.fdr.1
- Update to 0.3.2.
- Update URL.

* Thu Oct 16 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.3.1-0.fdr.1
- Update to 0.3.1.

* Wed Sep 10 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.3.0-0.fdr.1
- Update to 0.3.0.

* Wed Aug 27 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.2.0-0.fdr.1
- Update to 0.2.0.

* Tue Aug 19 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.1.0-0.fdr.1
- First build.
