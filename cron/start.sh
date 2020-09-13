#!/bin/sh

set -e

export OPTIONS=$OPTIONS

echo "$CRON_SCHEDULE /curl.sh" | crontab -u root -
crond -l 2 -f
