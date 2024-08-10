#!/bin/bash
# Go in the Bot section
cd BotTemplate

# Go in the Detector section
# cd DetectorTemplate

# Start the docker image and run the automation
docker-compose build
docker-compose up --abort-on-container-exit
