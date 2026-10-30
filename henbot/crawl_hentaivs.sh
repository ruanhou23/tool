#!/usr/bin/env bash
# Runner chuyển tiếp sang hentaivs_crawler

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../hentaivs_crawler" && pwd)"
python3 "$PROJECT_DIR/crawler.py" "$@"
