%global gitcommit 5e16db0493278b4d778ac3e7c1c5c8a0fe018bf3
%global gitshortcommit %(c=%{gitcommit}; echo ${c:0:7})
%global gitsnapinfo git20260708.%{gitshortcommit}
%global debug_package %{nil}

Name: xrt-base
Version: 2.26.0^%{gitsnapinfo}
Release: 1%{?dist}
Summary: AMD Flexible Runtime base
Group: System Environment/Libraries
License: Apache-2.0
URL: https://github.com/Xilinx/XRT

Source: xrt-%{version}.tar.gz

ExclusiveArch: x86_64
ExclusiveArch: aarch64

Requires: ocl-icd >= 2.2
Requires: python3 >= %{python3_version}

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

%description
AMD Flexible Runtime 2026.20 (formerly Xilinx Runtime) provides an abstracted runtime software interface for AMD NPUs and AMD FPGAs.

It supports the following product lines Ryzen AI, Versal, Alveo and Zynq UltraScale+.

%package -n xrt-base-devel
Summary: AMD Flexible Runtime development headers

Requires: libuuid-devel >= 2.23.2
Requires: ocl-icd-devel >= 2.2
Requires: xrt-base = %{version}

%description -n xrt-base-devel
AMD Flexible Runtime (XRT) development files.

%package -n xrt-npu
Summary: AMD Ryzen AI specific extensions

Requires: xrt-base = %{version}

ExclusiveArch: x86_64

%description -n xrt-npu
NPU specific extensions to the AMD Flexible Runtime for Ryzen AI.

%prep
%autosetup -n xrt-%{version}

%build
mkdir localbin
ln -s $(which cmake) localbin/cmake3
cd build
PATH="$(pwd)/../localbin:$PATH" ./build.sh \
  -opt \
  -disable-werror \
  -hip \
  -npu \
  -install_prefix /usr

%install
tar -xf build/Release/xrt*-base.tar.gz -C %{buildroot}
tar -xf build/Release/xrt*-base-devel.tar.gz -C %{buildroot}
tar -xf build/Release/xrt*-npu.tar.gz -C %{buildroot}

rm -f %{buildroot}/usr/versions
rm -f %{buildroot}/usr/share/completions/xbutil-csh-completion-wrapper
rm -f %{buildroot}/usr/version.json

mkdir -p %{buildroot}/etc/profile.d/
mkdir -p %{buildroot}%{bash_completions_dir}

mv %{buildroot}/usr/share/completions/xbutil-csh-completion %{buildroot}/etc/profile.d/xbutil.csh
mv %{buildroot}/usr/share/completions/xbutil-bash-completion %{buildroot}%{bash_completions_dir}/xbutil

%files
/etc/OpenCL/vendors/xilinx.icd

/usr/bin/aiebu-asm
/usr/bin/aiebu-dump
/usr/bin/aiebu-transform
/usr/bin/xclbinutil
/usr/bin/xrt-runner
/usr/bin/xrt-smi
/usr/bin/xrt-capture
/usr/bin/xrt-replay

/usr/lib64/libxilinxopencl.so.2
/usr/lib64/libxilinxopencl.so.2.26.0
/usr/lib64/libxrt++.so.2
/usr/lib64/libxrt++.so.2.26.0
/usr/lib64/libxrt_core.so.2
/usr/lib64/libxrt_core.so.2.26.0
/usr/lib64/libxrt_coreutil.so.2
/usr/lib64/libxrt_coreutil.so.2.26.0
/usr/lib64/libxrt_hip.so.2
/usr/lib64/libxrt_hip.so.2.26.0
# Need to work out how to dynamically place these because python version might change
%{python3_sitearch}/pyxrt.cpython-%{python3_version_nodots}-x86_64-linux-gnu.so
%{python3_sitearch}/pyxrt.pyi

/etc/profile.d/xbutil.csh
%{bash_completions_dir}/xbutil

%doc /usr/share/doc/CHANGELOG.rst
%doc /usr/share/doc/CONTRIBUTING.rst
%doc /usr/share/doc/NOTICE

%license /usr/license/LICENSE


%files -n xrt-base-devel
/usr/include/CL/cl_ext_xilinx.h

%dir /usr/include/aiebu
/usr/include/aiebu/aiebu.h
/usr/include/aiebu/aiebu_assembler.h
/usr/include/aiebu/aiebu_error.h

%dir /usr/include/hip/
/usr/include/hip/hip_xrt.h

%dir /usr/include/xrt
%dir /usr/include/xrt/deprecated/
/usr/include/xrt/deprecated/xclerr.h
/usr/include/xrt/deprecated/xrt.h
%dir /usr/include/xrt/detail/
/usr/include/xrt/detail/abi.h
/usr/include/xrt/detail/any.h
/usr/include/xrt/detail/bitmask.h
/usr/include/xrt/detail/config.h
/usr/include/xrt/detail/ert.h
/usr/include/xrt/detail/param_traits.h
/usr/include/xrt/detail/pimpl.h
/usr/include/xrt/detail/span.h
/usr/include/xrt/detail/version-slim.h
/usr/include/xrt/detail/version.h
/usr/include/xrt/detail/xclbin.h
/usr/include/xrt/detail/xrt_error_code.h
/usr/include/xrt/detail/xrt_mem.h
%dir /usr/include/xrt/experimental/
/usr/include/xrt/experimental/xclbin_util.h
/usr/include/xrt/experimental/xrt-next.h
/usr/include/xrt/experimental/xrt_aie.h
/usr/include/xrt/experimental/xrt_bo.h
/usr/include/xrt/experimental/xrt_device.h
/usr/include/xrt/experimental/xrt_elf.h
/usr/include/xrt/experimental/xrt_error.h
/usr/include/xrt/experimental/xrt_exception.h
/usr/include/xrt/experimental/xrt_ext.h
/usr/include/xrt/experimental/xrt_fence.h
/usr/include/xrt/experimental/xrt_graph.h
/usr/include/xrt/experimental/xrt_hw_context.h
/usr/include/xrt/experimental/xrt_ini.h
/usr/include/xrt/experimental/xrt_ip.h
/usr/include/xrt/experimental/xrt_kernel.h
/usr/include/xrt/experimental/xrt_mailbox.h
/usr/include/xrt/experimental/xrt_message.h
/usr/include/xrt/experimental/xrt_module.h
/usr/include/xrt/experimental/xrt_profile.h
/usr/include/xrt/experimental/xrt_queue.h
/usr/include/xrt/experimental/xrt_system.h
/usr/include/xrt/experimental/xrt_uuid.h
/usr/include/xrt/experimental/xrt_version.h
/usr/include/xrt/experimental/xrt_xclbin.h
/usr/include/xrt/xrt_aie.h
/usr/include/xrt/xrt_bo.h
/usr/include/xrt/xrt_device.h
/usr/include/xrt/xrt_graph.h
/usr/include/xrt/xrt_hw_context.h
/usr/include/xrt/xrt_kernel.h
/usr/include/xrt/xrt_uuid.h

/usr/lib64/libaiebu.a
/usr/lib64/libcert_dtrace.a
/usr/lib64/libxilinxopencl.a
/usr/lib64/libxilinxopencl.so
/usr/lib64/libxrt++.a
/usr/lib64/libxrt++.so
/usr/lib64/libxrt_core.a
/usr/lib64/libxrt_core.so
/usr/lib64/libxrt_coreutil.a
/usr/lib64/libxrt_coreutil.so
/usr/lib64/libxrt_hip.so

/usr/lib64/pkgconfig/xrt.pc

%dir /usr/share/cmake/AIEBU/
/usr/share/cmake/AIEBU/aiebu-config-version.cmake
/usr/share/cmake/AIEBU/aiebu-config.cmake
/usr/share/cmake/AIEBU/aiebu-targets-release.cmake
/usr/share/cmake/AIEBU/aiebu-targets.cmake
%dir /usr/share/cmake/XRT/
/usr/share/cmake/XRT/xrt-config-version.cmake
/usr/share/cmake/XRT/xrt-config.cmake
/usr/share/cmake/XRT/xrt-targets-release.cmake
/usr/share/cmake/XRT/xrt-targets.cmake


%files -n xrt-npu
/usr/lib64/libxdp_core.so.2
/usr/lib64/libxdp_core.so.2.26.0
/usr/lib64/xrt/module/libxdp_aie_profile_plugin.so.2
/usr/lib64/xrt/module/libxdp_aie_profile_plugin.so.2.26.0
/usr/lib64/xrt/module/libxdp_aie_trace_plugin.so.2
/usr/lib64/xrt/module/libxdp_aie_trace_plugin.so.2.26.0
/usr/lib64/xrt/module/libxdp_ml_timeline_plugin.so.2
/usr/lib64/xrt/module/libxdp_ml_timeline_plugin.so.2.26.0
/usr/lib64/xrt/module/libxdp_native_plugin.so.2
/usr/lib64/xrt/module/libxdp_native_plugin.so.2.26.0
/usr/lib64/xrt/module/libxdp_user_plugin.so.2
/usr/lib64/xrt/module/libxdp_user_plugin.so.2.26.0



%changelog
* Wed Jul 08 2026 Darren Cocco <linux.fedora.packaging@darren.cocco.id.au> 2.26.0^git20260708.4d57b3d-1
- Updated to 2.26.0

* Mon Jun 15 2026 Darren Cocco <linux.fedora.packaging@darren.cocco.id.au> 2.25.23^git20260615.943586a-1
- Upgraded to 2.26.23

* Thu Jun 04 2026 Darren Cocco <linux.fedora.packaging@darren.cocco.id.au> 2.25.13^git20260602.c63dac0-1
- Initial release
