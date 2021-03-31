#!/bin/bash

# Stop and remove any existing container instances
docker stop vacinefinder
docker rm vacinefinder

# Build the new image
docker build -t vacinefinder:latest -f Dockerfile .

# Run the container
docker run --rm -it --name vacinefinder vacinefinder:latest