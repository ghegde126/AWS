import json
import boto3
import logging
import os

logger = logging.getLogger()
logger.setLevel(os.getenv('logging_level'))

dynamoDB_table_name = os.getenv('dynamoDB_table_name')

dynamoDBClient = boto3.client('dynamodb')


def lambda_handler(event, context):
    logger.info(event)
    if 'httpMethod' in event:
        return process_event(event['httpMethod'], event['path'], json.loads(event['body']))

    else:
        return responseMakerWithMessage(400, "Invalid request, request must include parameters httpMethod and path")


def process_event(APIMethod, path, body):
    print('inside process')
    print(APIMethod)
    print(path)
    print(body)
    if (APIMethod == 'GET' and path == '/healthCheck'):
        return responseMakerWithMessage(200, "Connection is working...")
    
    elif 'CustomerId' not in body:
        print('inside customer id not found')
        return responseMakerWithMessage(400, "CustomerId key is not present in the request, please provide this key.")

    elif (APIMethod == 'POST' and path == '/getCustomer'):
        return getCustomer(body)

    elif (APIMethod == 'POST' and path == '/createCustomer'):
        print('inside create customer ')
        return createCustomer(body)
    
    elif (APIMethod == 'POST' and path == '/updateCustomer'):
        return updateCustomer(body)

    elif (APIMethod == 'POST' and path == '/updateCustomerEmail'):
        return updateCustomerEmail(body)
    
    else:
        return responseMakerWithMessage(400, "Invalid Request")


def createCustomer(eventBody):
    print('here')
    try:
        dynamoDBClient.put_item(
            TableName = dynamoDB_table_name,
            Item = eventBody
        )
        print('done')
        return responseMakerWithMessage(200, "{} saved successfully.".format(eventBody['CustomerId']))
    
    except Exception as exception:
        logger.error(str(exception))
        return responseMakerWithMessage(400, "Unable to process the request")

    
def updateCustomer(eventBody):
    try:
        dynamoDBClient.put_item(
            TableName = dynamoDB_table_name,
            Item = eventBody
        )
        return responseMakerWithMessage(200, "{} updated successfully.".format(eventBody['CustomerId']))
    
    except Exception as exception:
        logger.error(str(exception))
        return responseMakerWithMessage(400, "Unable to process the update request")


def updateCustomerEmail(eventBody):
    try:
        dynamoDBClient.update_item(
            TableName = dynamoDB_table_name,
            Key = { 'CustomerId' : eventBody['CustomerId'] },
            ExpressionAttributeValues = { ':newEmail' : eventBody['c'] },
            UpdateExpression = 'SET UpdateExpression = :newEmail'
        )
        return responseMakerWithMessage(200, "{} updated successfully.".format(eventBody['CustomerId']))

    except Exception as exception:
        logger.error(str(exception))
        return responseMakerWithMessage(400, "Unable to process the update request")

def getCustomerDetails(eventBody):
    try:
        response = dynamoDBClient.get_item(
            TableName = dynamoDB_table_name,
            Key = { 'CustomerId' : eventBody['CustomerId'] }
            )

        if len(response['Item']) != 0:
            return responseMakerWithMessage(200, json.dumps(response['Item']))

        else:
            return responseMakerWithMessage(200, "Customer ID {} does not exists".format(eventBody['CustomerId']))

    except Exception as exception:
        logger.error(str(exception))
        return responseMakerWithMessage(400, "Unable to process the update request")



def responseMakerWithMessage(statusCode, message):
    return {
            "StatusCode" : statusCode,
            "headers" : {
                "Content-Type": "application/json"
            },
            "body" : json.dumps(message)
        }

