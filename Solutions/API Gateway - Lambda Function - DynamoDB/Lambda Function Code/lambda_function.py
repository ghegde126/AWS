import json
import boto3
import logging
import os

logger = logging.getLogger()
logger.setLevel(os.getenv('logging_level'))

dynamoDB_table_name = os.getenv('dynamoDB_table_name')

dynamoDBClient = boto3.client('dynamodb')


def lambda_handler(event, context):
    if 'httpMethod','path' in event:

    else:
        return {
            "StatusCode" : 400,
            "headers" : {
                "Content-Type": "application/json"
            },
            "body" : "Invalid request, request must include parameters httpMethod and path"
        }


def process_event(APIMethod, path, body):
    if (APIMethod == 'GET' and path == 'healthCheck'):
        return {
            "StatusCode" : 200,
            "headers" : {
                "Content-Type": "application/json"
            },
            "body" : "Connection is working..."
        }
    
    elif (APIMethod == 'POST' and path == 'createCustomer'):

def createCustomer(eventBody):
    if 'CustomerId' in eventBody:
        try:
            dynamoDBClient.put_item(
                TableName = dynamoDB_table_name,
                Item = eventBody
            )
        
        except Exception as exception:
            log.error(str(exception))



    else:
        log.info(CustomerId + ' is not present in table '+ dynamoDB_table_name)
        return responseMakerWithMessage(400, "CustomerId key is not present in the request, please provide this key.")
    
def responseMakerWithMessage(statusCode, message):
    return {
            "StatusCode" : statusCode,
            "headers" : {
                "Content-Type": "application/json"
            },
            "body" : message
        }


def setup_logging():
    global log 
    log = logging.getLogger()
    log_levels = {'INFO':20, 'WARNING':30, 'ERROR':40}

    if 'logging_level' in os.environ:
        log_level = os.environ['logging_level'].upper()
        if log_level in log_levels:
            log.setLevel(log_levels[log_level])
        else:
            log.setLevel(log_levels['ERROR'])
            logger.error('As logging level is not set to INFO, ERROR or WARNING, logging level is set to ERROR'))
        
    else:
        log.setLevel(log_levels['ERROR'])
    log.info('Logging setup is complete - set to log level ' + str(log.getEffectiveLevel()))