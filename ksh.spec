Summary:	The real AT&T version of the Korn shell
Name:		ksh
Version:	93t
Release:	%mkrel 3
License:	CPLv1
Group:		Shells
URL:		http://kornshell.com
Source0:	http://www.research.att.com/~gsf/download/tgz/INIT.2008-06-24.tar.bz2
Source1:	http://www.research.att.com/~gsf/download/tgz/ast-base.2008-06-24.tar.bz2
Patch0:		ast_ksh_20080624_getenv_link_fix.diff
Requires(post): coreutils, grep, rpm-helper >= 0.7
Requires(postun): rpm-helper >= 0.7
Requires(pre): coreutils, grep, rpm-helper >= 0.7
BuildRequires:	chrpath
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
%patch0 -p0

%build
bin/package make CCFLAGS="%{optflags} -fPIC"

%install
rm -rf %{buildroot}

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

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README CPL1.0.txt
/bin/ksh93
%{_mandir}/man1/ksh93.1*
