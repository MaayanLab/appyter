# Example Production Deployment

```bash
# use appyter from source
alias appyter="PYTHONPATH=$(pwd)/.. python -m appyter"

# obtain versions
APPYTER_VERSION=$(jq -r '.version' appyter.json)
LIBRARY_VERSION=$(appyter --version | awk '{print $3}')
DOCKER_TAG=maayanlab/appyter-$(jq -r '.name' appyter.json):${APPYTER_VERSION}-${LIBRARY_VERSION}

# setup docker
appyter dockerize example.ipynb > Dockerfile
docker build --build-arg "appyter_version=appyter[production]@git+https://github.com/Maayanlab/appyter@v${LIBRARY_VERSION}" -t $DOCKER_TAG .
docker push $DOCKER_TAG

docker run \
  -p 5000:5000 \
  -it $DOCKER_TAG \
  appyter --profile=biojupies example.ipynb

```

## With CAVATICA
```bash
# setup cwl
appyter nbinspect cwl -i appyter.json example.ipynb | jq '.' > example.cwl

# rebuild to include cwl in image
docker build --build-arg "appyter_version=appyter[production]@git+https://github.com/Maayanlab/appyter@v${LIBRARY_VERSION}" -t $DOCKER_TAG .
docker push $DOCKER_TAG


# prepare env 
# see https://cavatica.sbgenomics.com/developer/token
export CAVATICA_API_KEY=
# e.g. danieljbclarkemssm/appyters-in-cavatica
export CAVATICA_PROJECT=

export APPYTER_DATA_DIR="sbfs://${CAVATICA_PROJECT}/?api_endpoint=https://cavatica-api.sbgenomics.com&auth_token=${CAVATICA_API_KEY}"
export APPYTER_EXECUTOR="cavatica?cwl=example.cwl&project=${CAVATICA_PROJECT}&auth_token=${CAVATICA_API_KEY}"

docker run \
  -e APPYTER_DATA_DIR \
  -e APPYTER_EXECUTOR \
  -p 5000:5000 \
  -it $DOCKER_TAG \
  appyter --profile=biojupies example.ipynb

```
