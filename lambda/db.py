import boto3
from boto3.dynamodb.conditions import Key
from ask_sdk_dynamodb.adapter import DynamoDbAdapter
import os
import string
import random
import json


ddb_region = os.environ.get('DYNAMODB_PERSISTENCE_REGION')
ddb_table_name = os.environ.get('DYNAMODB_PERSISTENCE_TABLE_NAME')

ddb_resource = boto3.resource('dynamodb', region_name=ddb_region)
dynamodb_adapter = DynamoDbAdapter(
    table_name=ddb_table_name, create_table=False, dynamodb_resource=ddb_resource)

class DynamoDBLayer:

    def putAppointment(doctor, sessionAttributes, appointment_time):
        id = getRandomId(doctor)
        dynamodb = boto3.client('dynamodb')
        result = dynamodb.put_item(
            TableName=ddb_table_name, 
            Item = {
                    'id': {
                        'S': id 
                    },
                    'doctor': {
                        'S': doctor
                    },
                    'user_name' : {
                        'S': sessionAttributes['user_name']
                    },
                    'age' : {
                        'S': str(sessionAttributes['user_age'])
                    },
                    'height' : {
                        'S': str(sessionAttributes['user_height'])
                    },
                    'weight' : {
                        'S': str(sessionAttributes['user_weight'])
                    },
                    'temperature' : {
                        'S': str(sessionAttributes['user_temperature'])
                    },
                    'complain' : {
                        'S': sessionAttributes['complain']
                    },
                    'appointment_time' : {
                        'S': str(appointment_time)
                    }
                }
            ),
        return result

def getRandomId(doctor):
    N = 7
    res = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = N))
    randId = doctor +'_'+ str(res)
    return randId
       