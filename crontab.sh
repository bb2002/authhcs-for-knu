#!/bin/sh

today=$(date "+%Y%m%d")

source venv/bin/activate

python3 main.py > "autohcs_${today}.log"
