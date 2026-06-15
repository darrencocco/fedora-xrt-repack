MAKEFILE_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

all: xrt xrt-plugin-amdxdna amdxdna-kmod

xrt: srpm-xrt build-xrt

xrt-plugin-amdxdna: srpm-xrt-plugin-amdxdna build-xrt-plugin-amdxdna

amdxdna-kmod: srpm-amdxdna-kmod build-amdxdna-kmod

srpm-xrt:
	$(MAKE) -f $(MAKEFILE_DIR)/.copr/Makefile clean spec=$(MAKEFILE_DIR)/xrt.spec
	$(MAKE) -f $(MAKEFILE_DIR)/.copr/Makefile srpm spec=$(MAKEFILE_DIR)/xrt.spec

srpm-xrt-plugin-amdxdna:
	$(MAKE) -f $(MAKEFILE_DIR)/.copr/Makefile clean spec=$(MAKEFILE_DIR)/xrt-plugin-amdxdna.spec
	$(MAKE) -f $(MAKEFILE_DIR)/.copr/Makefile srpm spec=$(MAKEFILE_DIR)/xrt-plugin-amdxdna.spec

srpm-amdxdna-kmod:
	$(MAKE) -f $(MAKEFILE_DIR)/.copr/Makefile clean spec=$(MAKEFILE_DIR)/amdxdna-kmod.spec
	$(MAKE) -f $(MAKEFILE_DIR)/.copr/Makefile srpm spec=$(MAKEFILE_DIR)/amdxdna-kmod.spec

build-xrt:
	dnf builddep -y xrt-base*.src.rpm
	rpmbuild -rb xrt-base*.src.rpm
	cp ~/rpmbuild/RPMS/*/* ./

build-xrt-plugin-amdxdna:
	dnf builddep -y xrt-plugin-amdxdna*.src.rpm xrt-base*.src.rpm
	rpmbuild -rb xrt-plugin-amdxdna*.src.rpm
	cp ~/rpmbuild/RPMS/*/* ./

build-amdxdna-kmod:
	dnf builddep -y amdxdna-kmod*.src.rpm
	rpmbuild -rb amdxdna-kmod*.src.rpm
	cp ~/rpmbuild/RPMS/*/* ./
