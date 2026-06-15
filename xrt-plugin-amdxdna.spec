%global gitcommit 928ce6f6dcb20f5c6ed739ed9ccd129c18effd39
%global gitshortcommit %(c=%{gitcommit}; echo ${c:0:7})
%global gitsnapinfo git20260615.%{gitshortcommit}
%global debug_package %{nil}

Name: xrt-plugin-amdxdna
Version: 2.25.23^%{gitsnapinfo}
Release: 1%{?dist}
Summary: AMD Flexible Runtime XDNA2 shim
Group: System Environment/Libraries
License: Apache-2.0 AND Redistributable, no modification, no reverse engineering
URL: https://github.com/amd/xdna-driver

Source: xrt-plugin-amdxdna-%{version}.tar.gz

ExclusiveArch: x86_64

Requires: xrt-npu

BuildRequires: boost-devel
BuildRequires: boost-filesystem
BuildRequires: boost-program-options
BuildRequires: boost-static
BuildRequires: cmake
BuildRequires: cppcheck
BuildRequires: curl
BuildRequires: doxygen
BuildRequires: dmidecode
BuildRequires: elfutils-devel
BuildRequires: elfutils-libs
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: gdb
BuildRequires: git
BuildRequires: glibc-static
BuildRequires: gnuplot
BuildRequires: gnutls-devel
BuildRequires: gtest-devel
BuildRequires: json-glib-devel
BuildRequires: libcurl-devel
BuildRequires: libdrm-devel
BuildRequires: libffi-devel
BuildRequires: libjpeg-turbo-devel
BuildRequires: libpng12-devel
BuildRequires: libstdc++-static
BuildRequires: libtiff-devel
BuildRequires: libudev-devel
BuildRequires: libuuid-devel
BuildRequires: libyaml-devel
BuildRequires: lm_sensors
BuildRequires: make
BuildRequires: ncurses-devel
BuildRequires: ocl-icd
BuildRequires: ocl-icd-devel
BuildRequires: opencl-headers
BuildRequires: opencv
BuildRequires: openssl-devel
BuildRequires: pciutils
BuildRequires: perl
BuildRequires: pkgconf-pkg-config
BuildRequires: protobuf-compiler
BuildRequires: protobuf-devel
BuildRequires: python3
BuildRequires: python3-devel
BuildRequires: python3-pip
BuildRequires: python3-pybind11
BuildRequires: python3-sphinx
BuildRequires: redhat-lsb
BuildRequires: rapidjson-devel
BuildRequires: rocm-hip-devel
BuildRequires: rpm-build
BuildRequires: strace
BuildRequires: systemd-devel
BuildRequires: systemtap-sdt-devel
BuildRequires: unzip
BuildRequires: zlib-static

BuildRequires: jq
BuildRequires: wget

%description
Shim for supporting AMD XDNA2 NPU

Works with both in-tree Linux kernel module (>= v7.0) and
out of tree kernel module (>= v6.10, < v7.0).

%prep
%autosetup -n xrt-plugin-amdxdna-%{version}

%build
mkdir localbin
ln -s $(which cmake) localbin/cmake3
cd build
PATH="$(pwd)/../localbin:$PATH" ./build.sh \
  -release \
  -nokmod \
  -install_prefix /usr

%install
rpm2archive -n build/Release/xrt_plugin*.rpm | tar -x -C %{buildroot}
mkdir -p %{buildroor}/etc/security/limits.d
install -D -m 0644 additional_config/90-amdxdna-memlock.conf %{buildroot}/etc/security/limits.d/90-amdxdna-memlock.conf

%files
/usr/include/vaccel.h
/usr/lib64/libvxdna.so
/usr/lib64/libvxdna.so.1
/usr/lib64/libvxdna.so.1.0.0
/usr/lib64/libxrt_driver_xdna.so.2
/usr/lib64/libxrt_driver_xdna.so.2.25.0
/usr/lib64/pkgconfig/vxdna.pc
/usr/share/amdxdna/bins/xrt_smi_npu3.a
/usr/share/amdxdna/bins/xrt_smi_phx.a
/usr/share/amdxdna/bins/xrt_smi_strx.a
/etc/security/limits.d/90-amdxdna-memlock.conf


%changelog
* Mon Jun 15 2026 Darren Cocco <linux.fedora.packaging@darren.cocco.id.au> 2.25.23^git20260615.928ce6f
- Upgraded to commit 928ce6f6dcb20f5c6ed739ed9ccd129c18effd39

* Sun Jun 07 2026 Darren Cocco <linux.fedora.packaging@darren.cocco.id.au> 2.25.13^git20260607.cd2494b
- Initial release
