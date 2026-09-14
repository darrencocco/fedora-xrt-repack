#!/bin/bash
# Sync firmware from WHENCE manifest using upstream sync_from_whence.py

python3 tools/sync_from_whence.py firmware \
    --whence tools/WHENCE \
    --out amdxdna_bins/firmware \
    --commit-file amdxdna_bins/firmware/.whence_commit