#!/bin/bash

export FLASK_BASE_URL='YOUR BASE URL'
source ./.venv/bin/activate
export FLASK_APP=app.py
flask run --host=0.0.0.0
