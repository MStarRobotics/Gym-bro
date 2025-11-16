#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <path-to-keystore.jks>"
  exit 2
fi

JKS_PATH=$1
if [[ ! -f "$JKS_PATH" ]]; then
  echo "Keystore file not found: $JKS_PATH"
  exit 1
fi

base64 "$JKS_PATH"
