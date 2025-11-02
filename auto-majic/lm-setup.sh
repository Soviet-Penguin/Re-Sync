#!/bin/bash

echo "======================================"
echo "AUTO MAJIC FOR LINUX AND MAC"
echo "======================================"

python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
echo ""
echo "Setup complete!"
echo ""
