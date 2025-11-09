#!/usr/bin/env bash

REPO_URL="https://github.com/DepthPixels/LC3Assembler.git"
REPO_DIR="LC3Assembler"

if [ -d "$REPO_DIR" ]; then
  cd "$REPO_DIR"
  git pull
  cd ..
else
  git clone "$REPO_URL"
fi

python3 $REPO_DIR/main.py "$@"
