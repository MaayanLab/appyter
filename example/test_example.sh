#!/usr/bin/sh

echo "-----------------------------------------"
echo "Try it out at http://0.0.0.0:5000/"
echo "-----------------------------------------"
echo ""
cd .. && HOST=0.0.0.0 PORT=5000 PREFIX=/example/ python3 -m appyter \
  --profile=biojupies \
  --cwd=example \
  example/example.ipynb
