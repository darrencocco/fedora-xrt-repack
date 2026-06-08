spec := xrt.spec
outdir := ./

MAKEFILE_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
SPEC_FILENAME := $(notdir $(spec))
VERSION := $(firstword $(shell rpmspec --query --queryformat="%{VERSION} " $(spec)))
ifeq ($(SPEC_FILENAME), xrt.spec)
	GIT_REPO := https://github.com/Xilinx/XRT.git
else
	GIT_REPO := https://github.com/amd/xdna-driver.git
endif
GIT_DIR := $(subst .spec,,${SPEC_FILENAME})-$(VERSION)
ARCHIVE := $(GIT_DIR).tar.gz
GIT_COMMIT := $(lastword $(shell grep "%global gitcommit" $(spec)))

srpm: prepare-srpm
	rpmbuild --undefine dist -bs rpmbuild/SPECS/$(SPEC_FILENAME)
	cp rpmbuild/SRPMS/* $(outdir)

prepare-srpm: compress-source
	mkdir -p rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
	cp $(ARCHIVE) rpmbuild/SOURCES/
	cp $(spec) rpmbuild/SPECS/

download:
	dnf install -y git jq wget
	git clone --recursive --revision $(GIT_COMMIT) $(GIT_REPO) $(GIT_DIR)

compress-source: download prepare-kmod-archive prepare-xrt-plugin-archive
	tar -czf $(ARCHIVE) $(GIT_DIR)

download-npu-firmware:
ifeq ($(SPEC_FILENAME),amdxdna-kmod.spec)
	chmod ugo+x $(MAKEFILE_DIR)/download-firmware.sh
	cd $(GIT_DIR) && $(MAKEFILE_DIR)/download-firmware.sh
endif

prepare-kmod-archive: download-npu-firmware
ifeq ($(SPEC_FILENAME),amdxdna-kmod.spec)
	mv $(GIT_DIR) $(GIT_DIR).old

	mkdir -p $(GIT_DIR)/{legacy,upstream,firmware,config}
	mkdir -p $(GIT_DIR)/legacy/{driver,include,tools}
	mkdir -p $(GIT_DIR)/upstream/{driver,include,tools}
	mkdir -p $(GIT_DIR)/legacy/driver/amdxdna
	mkdir -p $(GIT_DIR)/upstream/driver/amdxdna

	cp -rf $(GIT_DIR).old/drivers/accel/amdxdna/* $(GIT_DIR)/upstream/driver/amdxdna
	cp -rf $(GIT_DIR).old/drivers/accel/tools/* $(GIT_DIR)/upstream/tools
	cp -rf $(GIT_DIR).old/include/* $(GIT_DIR)/upstream/include

	cp -rf $(GIT_DIR).old/src/driver/amdxdna/* $(GIT_DIR)/legacy/driver/amdxdna
	cp -rf $(GIT_DIR).old/src/driver/tools/* $(GIT_DIR)/legacy/tools
	cp -rf $(GIT_DIR).old/src/include/* $(GIT_DIR)/legacy/include

	cp -rf $(GIT_DIR).old/amdxdna_bins/firmware/* $(GIT_DIR)/firmware

	cp -rf $(MAKEFILE_DIR)../akmod/* $(GIT_DIR)/config

	cp -f $(GIT_DIR).old/LICENSE.amdnpu $(GIT_DIR)

	rm -rf $(GIT_DIR).old
endif

prepare-xrt-plugin-archive:
ifeq ($(SPEC_FILENAME),xrt-plugin-amdxdna.spec)
	mkdir -p $(GIT_DIR)/additional_config
	cp $(MAKEFILE_DIR)../xrt-plugin/* $(GIT_DIR)/additional_config
endif

clean :
	rm -f $(ARCHIVE)
	rm -rf $(GIT_DIR)
	rm -rf rpmbuild/