%global gitcommit cd2494b38689a2d58ca365a09ab0386c706a5296
%global gitshortcommit %(c=%{gitcommit}; echo ${c:0:7})
%global gitsnapinfo git20260607.%{gitshortcommit}
%global debug_package %{nil}
%define buildforkernels akmod

%global modname amdxdna

Name: %{modname}-kmod
Version: 2.25.13^%{gitsnapinfo}
Release: 1%{?dist}
Summary: Kernel module for the AMD XDNA NPU driver
Group: System Environment/Libraries
License: GPL-2.0-only AND Redistributable, no modification, no reverse engineering
URL: https://github.com/amd/xdna-driver

Source: %{name}-%{version}.tar.gz

BuildRequires: gcc
BuildRequires: make
BuildRequires: kernel-devel
BuildRequires: kmodtool
Requires: kernel >= 6.10

ExclusiveArch: x86_64

# kmodtool magic
%{expand:%(kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null)}

%description
The kernel module for the AMD XDNA NPU accelerator driver.

%package -n %{modname}
Summary:        Firmware and headers for the AMD XDNA NPU driver
Provides:       %{modname}-kmod-common = %{version}
Requires:       %{modname}-kmod >= %{version}

%description -n %{modname}
Firmware and headers for the AMD XDNA NPU driver.

%prep
# Error out if kmodtool didn't define required macros
%{?kmodtool_check}

%autosetup -n %{name}-%{version}

# Replace version string in driver sources
find legacy/driver/amdxdna -name amdxdna_pci_drv.c -exec sed -i 's/MODULE_VERSION(".*")/MODULE_VERSION("%{version}%{release}")/' {} \;
find upstream/driver/amdxdna -name amdxdna_pci_drv.c -exec sed -i 's/MODULE_VERSION(".*")/MODULE_VERSION("%{version}%{release}")/' {} \;

# Extract driver sources into each per-kernel build directory
for kver in %{?kernel_versions}; do
    kernel_version=${kver%%___*}

    major_version=$(echo ${kernel_version} | cut -d. -f1)
    if [ ${major_version} -lt 7 ]; then
        driver_type="legacy"
    else
        driver_type="upstream"
    fi

    mkdir -p _kmod_build_${kernel_version}
    cp -rf firmware LICENSE.amdnpu _kmod_build_${kernel_version}/
    cp -rf ${driver_type}/driver _kmod_build_${kernel_version}/
    cp -rf ${driver_type}/include _kmod_build_${kernel_version}/

    # Generate kernel_config.h
    OUT=$(pwd)/_kmod_build_${kernel_version}/driver/amdxdna/config_kernel.h KERNEL_VER=${kernel_version} \
        $(pwd)/${driver_type}/tools/configure_kernel.sh
done

%build
for kver in %{?kernel_versions}; do
    # Compile module
    kernel_version=${kver%%___*}
    MODULE_VER_STR=%{version} \
        KERNEL_VER=${kernel_version} \
        KCFLAGS="-iquote%{_includedir}/amdxdna -iquote%{_includedir}/amdxdna/uapi -iquote%{_includedir}/amdxdna/trace/events" \
        make -C $(pwd)/_kmod_build_${kernel_version}/driver/amdxdna modules
done

%install
# Install userland components
# Firmware
mkdir -p %{buildroot}/usr/lib/firmware/amdnpu
cp -rf firmware/* %{buildroot}/usr/lib/firmware/amdnpu/
find %{buildroot}/usr/lib/firmware/amdnpu/ -type f -exec chmod -x {} \;

# Tools
install -D -m 755 legacy/tools/io_page_fault_flags %{buildroot}%{_bindir}/io_page_fault_flags-legacy
install -D -m 755 legacy/tools/npu_perf_analyze.sh %{buildroot}%{_bindir}/npu_perf_analyze-legacy.sh
install -D -m 755 legacy/tools/npu_perf_trace.sh %{buildroot}%{_bindir}/npu_perf_trace-legacy.sh
install -D -m 755 upstream/tools/io_page_fault_flags %{buildroot}%{_bindir}/io_page_fault_flags
install -D -m 755 upstream/tools/npu_perf_analyze.sh %{buildroot}%{_bindir}/npu_perf_analyze.sh
install -D -m 755 upstream/tools/npu_perf_trace.sh %{buildroot}%{_bindir}/npu_perf_trace.sh

# Headers
install -D -m 0644 legacy/include/uapi/drm_local/amdxdna_accel.h %{buildroot}%{_includedir}/amdxdna/uapi/drm_local/amdxdna_accel.h
install -D -m 0644 upstream/include/uapi/drm/amdxdna_accel.h %{buildroot}%{_includedir}/amdxdna/uapi/drm/amdxdna_accel.h
install -D -m 0644 upstream/include/trace/events/amdxdna.h %{buildroot}%{_includedir}/amdxdna/trace/events/amdxdna.h

# Configuration
install -D -m 0644 config/99-amdxdna.rules %{buildroot}/etc/udev/rules.d/99-amdxdna.rules
install -D -m 0644 config/amdxdna.dracut.conf %{buildroot}/etc/dracut.conf.d/amdxdna.dracut.conf
install -D -m 0644 config/amdxdna-blacklist.conf %{buildroot}/etc/modprobe.d/amdxdna-blacklist.conf

# Licenses & Docs
install -D -m 0644 LICENSE.amdnpu %{buildroot}%{_docdir}/%{modname}/LICENSE.amdnpu

# Install kernel modules
for kver in %{?kernel_versions}; do
    kernel_version=${kver%%___*}
    major_version=$(echo ${kernel_version} | cut -d. -f1)
    if [ ${major_version} -lt 7 ]; then
        driver_type="legacy"
    else
        driver_type="upstream"
    fi

    install -D -m 644 \
        _kmod_build_${kernel_version}/driver/amdxdna/amdxdna.ko \
        %{buildroot}/lib/modules/${kernel_version}/extra/amdxdna/amdxdna-${driver_type}.ko
done

%{?akmod_install}

%files -n %{modname}
%{_docdir}/%{modname}/
/usr/lib/firmware/amdnpu/
%{_includedir}/amdxdna/
%{_bindir}/io_page_fault_flags-legacy
%{_bindir}/npu_perf_analyze-legacy.sh
%{_bindir}/npu_perf_trace-legacy.sh
%{_bindir}/io_page_fault_flags
%{_bindir}/npu_perf_analyze.sh
%{_bindir}/npu_perf_trace.sh
/etc/udev/rules.d/99-amdxdna.rules
/etc/dracut.conf.d/amdxdna.dracut.conf
/etc/modprobe.d/amdxdna-blacklist.conf

%changelog
* Sun Jun 07 2026 Darren Cocco <linux.fedora.packaging@darren.cocco.id.au> 2.25.13^git20260607.cd2494b
- Initial release