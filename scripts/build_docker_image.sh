DOCKERHUB_USER="samscientist"
IMAGE_NAME="keynote-nlp-custom-api"
TAG="test"

docker buildx build --platform linux/amd64 -f Dockerfile_custom_api -t $DOCKERHUB_USER/$IMAGE_NAME:$TAG --push .