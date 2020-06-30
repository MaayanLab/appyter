#!/usr/bin/sh

echo "-----------------------------------------"
echo "Try it out at http://0.0.0.0:5000/example/"
echo "http://0.0.0.0:5000/example/testblueprint/"
echo "-----------------------------------------"
echo ""

BASE_PATH=$(realpath "$(dirname $0)/..")

cd ${BASE_PATH} && HOST=0.0.0.0 PORT=5000 PREFIX=/example/ python3 -m appyter \
  --profile=biojupies \
  --cwd=${BASE_PATH}/example \
  example.ipynb
