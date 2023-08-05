#!/bin/bash
docker rm -f web_pollution
docker build -t web_pollution . 
docker run --name=web_pollution --rm -p4137:1337 -it web_pollution
