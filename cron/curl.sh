#!/bin/sh

set -e

curl -X POST $CURL_URL -H "accept: application/json" -H "Content-Type: application/json" -d "$CURL_JSON"
