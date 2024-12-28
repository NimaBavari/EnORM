#!/bin/bash
python3 -m unittest
find . -type d -name "__pycache__" -exec rm -rf {} +
