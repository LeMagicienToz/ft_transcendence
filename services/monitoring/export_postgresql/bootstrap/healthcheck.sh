#!/bin/sh
curl -Ls "http://${T_SELF_NAME}:${T_PORT_INTERN_METRICS}/${T_ENDPOINT_METRICS}" -w "%{http_code}" -o "/dev/null" | grep -q "200"