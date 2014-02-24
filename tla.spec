%define __noautoreq '.*/bin/awk|.*/bin/gawk'
%define Werror_cflags	%nil
%define name	tla
%define version 1.3.5
%define release  7

Name:		%name
Version:	%version
Release:	%release
Summary:	Revision control system
License:	GPL
Group:		Development/Other
URL:		http://www.gnu.org/software/gnu-arch/
# Source: 	ftp://ftp.gnu.org/gnu/gnu-arch/%{name}-%{version}.tar.gz
# Source:	http://releases.gnuarch.org/tla/%{name}-%{version}.tar.gz
Source0: 	%{name}-%{version}.tar.bz2
#gw libneon needs some better provides
BuildRequires:	pkgconfig(neon)
Requires:	gawk tar gzip patch diffutils

%description
Also known as GNU Arch.
A modern replacement for CVS, specifically designed for the distributed 
development needs of open source projects. It has uniquely good support 
for development on branches (especially good merging tools), distributed 
repositories (every developer can have branches in their own repository), 
changeset-oriented project management (arch commits changes to multiple 
files at once), and, of course, file and directory renaming.

%prep
%setup -q -n %{name}-%{version}
# remove id files we don't want to distribute
find src/docs-tla -name .arch-ids | xargs rm -fr
# don't want to use embedded libneon (see also Patch0)
rm -rf src/tla/libneon

echo "%{name}-%{version} (%{name}-%{version}-%{release})" > \=RELEASE-ID 
#sed -i 's/-Wformat//g' src/libneon/configure src/libneon/macros/neon.m4

%build
mkdir \=build
cd \=build
export CFLAGS="${RPM_OPT_FLAGS}"
../src/configure --prefix=%{_prefix} --destdir=%{buildroot} 

make

%check
cd \=build
make test

%install
cd \=build
make install destdir=%{buildroot}

cd ..
#cp -r src/docs-tla/html html
#cp -r src/docs-tla/ps ps
#cp -r src/docs-tla/texi texi

sed 's,^#![[:space:]]*/.*$,#! /usr/bin/gawk -f,' src/tla/\=gpg-check.awk > %{buildroot}/%{_prefix}/bin/tla-gpg-check
chmod 0755 %{buildroot}/%{_prefix}/bin/tla-gpg-check

%files
%doc src/docs-tla/COPYING* src/docs-tla/ChangeLog 
%{_bindir}/*
