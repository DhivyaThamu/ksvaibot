#!/bin/sh

if [ -z "$PORT"]
then
  PORT=5055
fi

rasa run actions --port $PORT
