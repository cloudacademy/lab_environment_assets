#/bin/bash

AUTH_TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")

LOCAL_IPV4=$(curl -s -H "X-aws-ec2-metadata-token: $AUTH_TOKEN" http://169.254.169.254/latest/meta-data/local-ipv4)

echo $LOCAL_IPV4