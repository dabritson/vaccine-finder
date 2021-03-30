#!/bash
docker build -t test:latest -f Dockerfile .
docker run -it --name vacinefinder vacinefinder:latest