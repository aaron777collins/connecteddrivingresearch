#!/bin/sh
python -m venv connecteddrivingresearchvenv
source connecteddrivingresearchvenv/bin/activate | source connecteddrivingresearchvenv/Scripts/activate
pip install -r requirements.txt
