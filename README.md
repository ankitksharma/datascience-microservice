# Data Science Micro-Service (DSMS)

![Gunicorn + Falcon + Python](https://i.imgur.com/5RycsTo.jpg)

Boilerplate code for Data Science project microservice in Python

[Gunicorn](http://gunicorn.org/) & [Falcon](https://falconframework.org/) based server which is all you'll need to expose your awesome Data Science project as microservice with your peers.

There is a [Docker](https://www.docker.com/) file also added to dockerize you code which can then easily be put on Kubernetes or other container management service. 

## Setup
### Install using Docker
```
# 1. Setup by running `setup.sh` file
./setup.sh

# 2. Run Docker image
docker run -p 9000:9000 -t <docker_username>/dsms1:1.0.0

# 3. Run bash
docker run -it <docker_username>/dsms1:1.0.0 /bin/bash
```

### Install from scratch
```
# Create virtual environment (optional)
conda create -n dsms python=2.7
source activate dsms

# Install dependencies
pip install -r basepy/py/pip_requirements.txt

# Run the service
./run.sh
```

## Usage
`curl -X POST http://0.0.0.0:9000/`

`curl -X POST http://0.0.0.0:9000/update -d '{"text":"Some text to be sent."}'`
