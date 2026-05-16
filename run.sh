#!/bin/bash

source venv/bin/activate

export QT_QPA_PLATFORM=xcb

python app.py
