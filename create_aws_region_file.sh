#!/bin/bash
AWS_REGION="$1"
USER_SUBNET_ID="$2"
USER_VPC_ID="$3"
USE_PRIVATE_IP="$4"
UI_TFVARS_FILE="$5"
AWS_PROFILE="$6"
SECURITY_GROUP_ID="$7"
NAC_SCHEDULER_NAME="$8"
SERVICE_NAME="com.amazonaws.$AWS_REGION.execute-api"
# Get VPC Endpoint using AWS CLI command
VPC_ENDPOINT_ID=`aws ec2 describe-vpc-endpoints --profile $AWS_PROFILE --region $AWS_REGION | jq -r '.VpcEndpoints[]|select(.VpcId == '\"$USER_VPC_ID\"' and .ServiceName=='\"$SERVICE_NAME\"') | {VpcEndpointId}' | jq -r '.VpcEndpointId'`
echo "VPC_ENDPOINT_ID $VPC_ENDPOINT_ID"
echo "region="\"$AWS_REGION\" >$UI_TFVARS_FILE
echo "user_subnet_id="\"$USER_SUBNET_ID\" >> $UI_TFVARS_FILE
echo "user_vpc_id="\"$USER_VPC_ID\" >> $UI_TFVARS_FILE
echo "vpc_endpoint_id="\"$VPC_ENDPOINT_ID\" >> $UI_TFVARS_FILE
echo "use_private_ip="\"$USE_PRIVATE_IP\" >> $UI_TFVARS_FILE
echo "nac_es_securitygroup_id="\"$SECURITY_GROUP_ID\" >> $UI_TFVARS_FILE
echo "nac_scheduler_name="\"$NAC_SCHEDULER_NAME\" >> $UI_TFVARS_FILE
echo "" >> $UI_TFVARS_FILE
# End creation of TFVARS file 
