#!/usr/bin/env bash

nuitka \
  --standalone \
  --onefile \
  --output-dir=dist \
  --output-filename=thesis-genius \
  --nofollow-import-to=_tests \
  --nofollow-import-to=_examples \
  --include-data-files=app/config.py=app/config.py \
  cli/main.py

# --nofollow-import-to: Excludes unnecessary modules (e.g., test utilities, examples).
# --lto: Enables Link-Time Optimization (LTO) for faster execution.
# --remove-output: Reduces intermediate files to optimize runtime.
nuitka \
  --lto=yes \
  --remove-output \
  --standalone \
  --onefile \
  --output-dir=dist \
  --output-filename=thesis-genius \
  --nofollow-import-to=_tests \
  --nofollow-import-to=_examples \
  --include-data-files=app/config.py=app/config.py \
  cli/main.py
