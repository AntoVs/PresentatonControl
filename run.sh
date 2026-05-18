#!/bin/bash

source venv/bin/activate

export QT_QPA_PLATFORM=xcb
export YDOTOOL_SOCKET=/tmp/.ydotool_socket

python app.py
