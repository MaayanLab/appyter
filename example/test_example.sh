#!/usr/bin/sh

echo "-----------------------------------------"
echo "Try it out at http://0.0.0.0:5000/"
echo "-----------------------------------------"
echo ""
cd .. && HOST=0.0.0.0 PORT=5000 python3 -m jupyter_template \
  --profile=bootstrap \
  --cwd=example \
  example/example.ipynb
