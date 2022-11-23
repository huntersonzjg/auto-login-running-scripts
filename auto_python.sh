#!/bin/bash
rm -f /root/run.log
python3  /root/autologin.py  >> /root/run.log 2>&1
