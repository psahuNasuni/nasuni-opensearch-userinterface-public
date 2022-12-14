import base64
import json
import logging
import pprint
import subprocess

import elasticsearch
import os
import boto3
from datetime import *
from botocore.exceptions import ClientError
from elasticsearch.connection.http_requests import RequestsHttpConnection
from requests_aws4auth import AWS4Auth

from elasticsearch import Elasticsearch, helpers
import requests
from requests.auth import HTTPBasicAuth


def lambda_handler(event, context):
    print(context.invoked_function_arn)
    runtime_region = os.environ['AWS_REGION'] 
    context_arn=context.invoked_function_arn
    u_id=context_arn.split('-')[-1]
    print('u_id',u_id)
    account_id = boto3.client("sts").get_caller_identity()["Account"]
    role = 'arn:aws:iam::'+account_id+':role/nasuni-labs-exec_role-SearchUI-'+u_id
    
    secret_nct_nce_admin = get_secret('nasuni-labs-os-admin', runtime_region)

    
    username = secret_nct_nce_admin['nac_es_admin_user']
    secret_es_region = secret_nct_nce_admin['es_region']
    role_data = '{"backend_roles":["' +role + '"],"hosts": [],"users": ["'+username+'"]}'

    print(role_data)
    with open("/tmp/" + "/data.json", "w") as write_file:
        write_file.write(role_data)
    link = secret_nct_nce_admin['nac_kibana_url']
    link = link[:link.index('_')]

    password = secret_nct_nce_admin['nac_es_admin_password']
    data_file_obj = '/tmp/data.json'
    merge_link = '\"https://'+link+'_opendistro/_security/api/rolesmapping/all_access\"'
    url = 'https://' + link + '_opendistro/_security/api/rolesmapping/all_access/' 

    headers = {'content-type': 'application/json'}

    response = requests.put(url, auth=HTTPBasicAuth(username, password), headers=headers, data=role_data)
    print(response.text)
    es = launch_es(secret_nct_nce_admin['nac_es_url'], secret_es_region)
    resp = search(es)
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": '*'
        },
        "isBase64Encoded": False
    }
    response['body'] = json.dumps(resp)
    return response


def launch_es(link, region):
    # region = 'us-east-2'
    service = 'es'
    credentials = boto3.Session().get_credentials()
    print()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key,
                       region, service, session_token=credentials.token)
    es = Elasticsearch(hosts=[{'host': link, 'port': 443}], http_auth=awsauth, use_ssl=True, verify_certs=True,
                       connection_class=RequestsHttpConnection)
    return es


def search(es):
    vol_list=[]
    try:
        for elem in es.cat.indices(format="json"):
            query = {"query": {"match_all": {}}}
            resp = es.search(index=elem['index'], body=query)
            for i in resp['hits']['hits']:
                idx_content = i['_source'].get('content', 0)
                idx_object_key = i['_source'].get('object_key', 0)
                volume_name = i['_source'].get('volume_name', 0)
                
                if volume_name != 0: 
                    if not vol_list :
                        vol_list.append(volume_name)
                    elif volume_name not in vol_list:
                        vol_list.append(volume_name)
        print(vol_list)
        return vol_list
    except Exception as e:
        logging.error('ERROR: {0}'.format(str(e)))
        logging.error('ERROR: Unable to index line:"{0}"'.format(str(event)))
        print(e)


def get_secret(secret_name, region_name):
    secret = ''
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )

    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print("The requested secret " + secret_name + " was not found")
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            print("The request was invalid due to:", e)
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            print("The request had invalid params:", e)
        elif e.response['Error']['Code'] == 'DecryptionFailure':
            print(
                "The requested secret can't be decrypted using the provided KMS key:", e)
        elif e.response['Error']['Code'] == 'InternalServiceError':
            print("An error occurred on service side:", e)
    else:
        # Secrets Manager decrypts the secret value using the associated KMS CMK
        # Depending on whether the secret was a string or binary, only one of these fields will be populated
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            # print('text_secret_data',secret)
        else:
            secret = base64.b64decode(
                get_secret_value_response['SecretBinary'])
            # print('text_secret_data',secret)
    return json.loads(secret)


