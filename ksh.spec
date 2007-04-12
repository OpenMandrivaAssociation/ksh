Summary:	The real AT&T version of the Korn shell
Name:		ksh
Version:	93q
Release:	1mdk
License:	Common Public License
Group:		Shells
URL:		http://kornshell.com
Source:		%{name}-%{version}.tar.bz2
BuildRoot:	%_tmppath/%name-%version-root
Prereq:		coreutils, grep, rpm-helper >= 0.7

%description
Ksh is a UNIX command interpreter (shell) that is intended for both
interactive and shell script use. Its command language is a superset of
the sh(1) shell language.

The 1993 version adds a number of new, mostly scripting related,
features over the 1988 version that is typically distributed with
commercial UNIX variants. For example, it has lexical scoping, compound
variables, associative arrays, named references and floating point
math.

%prep
%setup -q


%build
bin/package make CCFLAGS="\"%{optflags}\""
cp lib/package/LICENSES/ast cpl1.0.txt

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT{/bin,%_bindir,%_mandir/man1}

install -s -c -m755 arch/*/bin/ok/ksh $RPM_BUILD_ROOT/bin/ksh93
install -c -m644 arch/*/man/man1/sh.1 $RPM_BUILD_ROOT%_mandir/man1/ksh93.1


%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/share/rpm-helper/add-shell %name $1 /bin/ksh93

%postun
/usr/share/rpm-helper/del-shell %name $1 /bin/ksh93

%files
%defattr(-,root,root)
%doc README cpl1.0.txt
/bin/*
%_mandir/*/*

