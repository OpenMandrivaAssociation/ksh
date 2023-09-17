#define beta beta.2

Summary:	The real AT&T version of the Korn shell
Name:		ksh
Version:	1.0.7
Release:	%{?beta:0.%{beta}.}1
License:	Eclipse Public License 1.0
Group:		Shells
URL:		http://kornshell.com
Source0:	https://github.com/ksh93/ksh/archive/refs/tags/v%{version}%{?beta:-%{beta}}.tar.gz
Patch0:		ksh-1.0.0-beta.2-work-around-float-types.patch
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
%autosetup -p1 -n ksh-%{version}%{?beta:-%{beta}}
#/dev/fd test does not work because of mock
sed -i 's|ls /dev/fd|ls /proc/self/fd|' src/cmd/ksh93/features/options

# disable register for debugging
sed -i 1i"#define register" src/lib/libast/include/ast.h

%build
sed -i -e 's,cd /tmp,cd "${TMPDIR:-/tmp}",' \
        bin/package src/cmd/INIT/package.sh || die

XTRAFLAGS=""
for f in -Wno-unknown-pragmas -Wno-missing-braces -Wno-unused-result -Wno-return-type -Wno-int-to-pointer-cast -Wno-parentheses -Wno-unused -Wno-unused-but-set-variable -Wno-cpp -Wno-maybe-uninitialized -Wno-lto-type-mismatch -P
do
  $CC $f -E - </dev/null >/dev/null 2>&1 && XTRAFLAGS="$XTRAFLAGS $f"
done
export CCFLAGS="$RPM_OPT_FLAGS $RPM_LD_FLAGS $XTRAFLAGS -fno-strict-aliasing"
./bin/package make

%install
install -d %{buildroot}/bin
install -d %{buildroot}%{_mandir}/man1

install -m0755 arch/*/bin/ksh %{buildroot}/bin/ksh93
install -m0644 arch/*/man/man1/sh.1 %{buildroot}%{_mandir}/man1/ksh93.1

# nuke rpath
chrpath -d %{buildroot}/bin/ksh93

%post
/usr/share/rpm-helper/add-shell %{name} $1 /bin/ksh93

%postun
/usr/share/rpm-helper/del-shell %{name} $1 /bin/ksh93

%files
%doc README.md LICENSE.md
/bin/ksh93
%{_mandir}/man1/ksh93.1*
