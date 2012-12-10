Summary:	The real AT&T version of the Korn shell
Name:		ksh
Version:	93.20110208
Release:	1
License:	CPLv1
Group:		Shells
URL:		http://kornshell.com
Source0:	http://www.research.att.com/~gsf/download/tgz/INIT.2012-01-01.tgz
Source1:	http://www.research.att.com/~gsf/download/tgz/ast-base.2011-02-08.tgz 
Requires(post): coreutils, grep, rpm-helper >= 0.7
Requires(postun): rpm-helper >= 0.7
Requires(pre): coreutils, grep, rpm-helper >= 0.7
BuildRequires:	chrpath

%description
Ksh is a UNIX command interpreter (shell) that is intended for both interactive
and shell script use. Its command language is a superset of the sh(1) shell
language.

The 1993 version adds a number of new, mostly scripting related, features over
the 1988 version that is typically distributed with commercial UNIX variants.
For example, it has lexical scoping, compound variables, associative arrays,
named references and floating point math.

%prep

%setup -q -c -a1

%build
sed -i -e 's,cd /tmp,cd "${TMPDIR:-/tmp}",' \
        bin/package src/cmd/INIT/package.sh || die

bin/package make CCFLAGS="%{optflags} -fPIC"

%install
install -d %{buildroot}/bin
install -d %{buildroot}%{_mandir}/man1

install -m0755 arch/*/bin/ok/ksh %{buildroot}/bin/ksh93
install -m0644 arch/*/man/man1/sh.1 %{buildroot}%{_mandir}/man1/ksh93.1

cp lib/package/LICENSES/ast CPL1.0.txt

# nuke rpath
chrpath -d %{buildroot}/bin/ksh93

%post
/usr/share/rpm-helper/add-shell %{name} $1 /bin/ksh93

%postun
/usr/share/rpm-helper/del-shell %{name} $1 /bin/ksh93

%files
%doc README CPL1.0.txt
/bin/ksh93
%{_mandir}/man1/ksh93.1*


%changelog
* Mon Feb 13 2012 Alexander Khrukin <akhrukin@mandriva.org> 93.20110208-1
+ Revision: 773747
- version update 2011-02-08

  + Sandro Cazzaniga <kharec@mandriva.org>
    - fix licence

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Wed Jul 23 2008 Oden Eriksson <oeriksson@mandriva.com> 93t-1mdv2009.0
+ Revision: 242358
- 93t (2008-06-24)
- package it the PLD way
- added P0 to make it build
- it requires -fPIC, make it so...
- nuke rpath with chrpath

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request
    - use %%mkrel

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

