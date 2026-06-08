#!/bin/bash
# Lifted from build.sh in amdxdna
mkdir -p amdxdna_bins/firmware
firmware_dir=amdxdna_bins/firmware

jq -c '.firmwares[]' "tools/info.json" |
while IFS= read -r line; do
  device=$(echo $line | jq -r '.device')
  pci_dev_id=$(echo $line | jq -r '.pci_device_id')
  version=$(echo $line | jq -r '.version')
  fw_name=$(echo $line | jq -r '.fw_name')
  url=$(echo $line | jq -r '.url')
  pci_rev_id=$(echo $line | jq -r '.pci_revision_id')

  if [[ -z "$url" ]]; then
  echo "Empty URL for $device NPUFW, SKIP."
  continue
  fi

  echo "Download $device NPUFW version $version:"
  if [ -f "${firmware_dir}/${pci_dev_id}_${pci_rev_id}/$fw_name" ]; then
  rm -r ${firmware_dir}/${pci_dev_id}_${pci_rev_id}
  fi
  mkdir -p ${firmware_dir}/${pci_dev_id}_${pci_rev_id}
  wget -O "${firmware_dir}/${pci_dev_id}_${pci_rev_id}/$fw_name" "$url"
done