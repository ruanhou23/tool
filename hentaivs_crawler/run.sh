#!/usr/bin/env bash
# Runner script cho HentaiVS Crawler

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/crawler.py" "$@"
