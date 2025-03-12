#!/bin/bash

# Script to remove all 'env' folders in the current directory tree
find . -type d -name "env" -exec rm -rf {} \; 2>/dev/null || true
