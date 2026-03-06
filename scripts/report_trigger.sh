#!/bin/bash
# AI SaaS Lab Daily Report Trigger
# Run at 09:00 and 21:00

cd /root/.openclaw/workspace

# AM Report - 09:00
if [ "$(date +%H)" = "09" ]; then
    echo "AM Report Time - $(date)" >> /tmp/saas_lab.log
fi

# PM Report - 21:00
if [ "$(date +%H)" = "21" ]; then
    echo "PM Report Time - $(date)" >> /tmp/saas_lab.log
fi
