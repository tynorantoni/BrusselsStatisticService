#!/usr/bin/env bash

mkdir -p ~/.aws

cat > ~/.aws/credentials << EOL
[default]
aws_access_key_id = []
aws_secret_access_key = []
EOL

