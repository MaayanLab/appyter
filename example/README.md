# Example Production Deployment

```bash
# use appyter from source
alias appyter="PYTHONPATH=$(pwd)/.. python -m appyter"

# obtain versions
APPYTER_VERSION=$(jq -r '.version' appyter.json)
LIBRARY_VERSION=$(appyter --version | awk '{print $3}')

# obtain versions
appyter dockerize example.ipynb > Dockerfile
DOCKER_TAG=maayanlab/appyter-$(jq -r '.name' appyter.json):${APPYTER_VERSION}-${LIBRARY_VERSION}
docker build -t $DOCKER_TAG .
docker push $DOCKER_TAG

docker run \
  -p 5000:5000 \
  -it $DOCKER_TAG \
  appyter --profile=biojupies example.ipynb

```
