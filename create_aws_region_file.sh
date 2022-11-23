#!/bin/bash
AWS_REGION="$1"
UI_TFVARS_FILE="$2"
echo "region="\"$AWS_REGION\" >$UI_TFVARS_FILE