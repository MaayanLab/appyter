#!/usr/bin/sh

echo "-----------------------------------------"
echo "Try it out at http://0.0.0.0:5000/example/"
echo "http://0.0.0.0:5000/example/testblueprint/"
echo "-----------------------------------------"
echo ""

BASE_PATH=$(realpath "$(dirname $0)/..")

cd ${BASE_PATH} && python3 -m appyter \
  --debug=false \
  --prefix=/example/ \
  --host=0.0.0.0 \
  --port=5000 \
  --profile=biojupies \
  --extras=toc \
  --cwd=${BASE_PATH}/example \
  example.ipynb
