#!/usr/bin/env bash
sudo docker-compose --env-file ./src/app/env/dev.env -f docker-compose.yml up --scale worker=2 --build
