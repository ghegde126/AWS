import json
import boto3
import logging
import os
import botocore

logger = logging.getLogger()
logger.setLevel(os.getenv('logging_level'))

dynamoDB_table_name = os.getenv('dynamoDB_table_name')
dynamoDBClient = boto3.client('dynamodb')

# Main Function
def lambda_handler(event, context):
    print(event)
    if 'httpMethod' in event:
        return process_event(event['httpMethod'], event['path'], event['body'])

    else:
        return responseMakerWithMessage(400, "Invalid request, request must include parameters httpMethod and path")


# Event processing function, based on API Request, it calls the sub functions
def process_event(APIMethod, path, eventBody):

    if (APIMethod == 'GET' and path == '/healthCheck'):
        return responseMakerWithMessage(200, "Connection is working...")

    elif len(eventBody) == 0 or 'CustomerId' not in eventBody:
        return responseMakerWithMessage(400, "Please provide necessary values in request body")

    elif (APIMethod == 'POST' and path == '/getCustomer'):
        return getCustomerDetails(json.loads(jsonCleaner(eventBody)))

    elif (APIMethod == 'POST' and path == '/createCustomer'):
        return createCustomer(json.loads(jsonCleaner(eventBody)))

    elif (APIMethod == 'POST' and path == '/updateCustomer'):
        return updateCustomer(json.loads(jsonCleaner(eventBody)))

    elif (APIMethod == 'POST' and path == '/updateCustomerEmail'):
        return updateCustomerEmail(json.loads(jsonCleaner(eventBody)))
    
    else:
        return responseMakerWithMessage(400, "Invalid Request")


# This function puts a Customer Item in DynamoDB Table
def createCustomer(eventBody):
    try:
        dynamoDBClient.put_item(
            TableName = dynamoDB_table_name,
            Item = eventBody
        )
        return responseMakerWithMessage(200, "{} saved successfully.".format(eventBody['CustomerId']['S']))
    
    except Exception as exception:
        logger.error(str(exception))
        return responseMakerWithMessage(400, "Unable to process the request")
    

# This function gets a Customer Item from DynamoDB Table
def getCustomerDetails(eventBody):
    try:
        response = dynamoDBClient.get_item(
            TableName = dynamoDB_table_name,
            Key = { 'CustomerId' : eventBody['CustomerId'] }
            )

        if 'Item' in response:
            return responseMakerWithMessage(200, json.dumps(response['Item']))

        else:
            return responseMakerWithMessage(200, "Customer ID {} does not exists".format(eventBody['CustomerId']['S']))
    
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'ResourceNotFoundException':
            return responseMakerWithMessage(200, "Customer ID {} does not exists".format(eventBody['CustomerId']['S']))
        else:
            return responseMakerWithMessage(400, "Unable to process the get customer details request botocore")

    except Exception as exception:
        logger.error(str(exception))
        print(str(exception))
        print(exception)
        return responseMakerWithMessage(400, "Unable to process the get customer details request")
    

# This function updates entire Item
def updateCustomer(eventBody):
    try:
        dynamoDBClient.put_item(
            TableName = dynamoDB_table_name,
            Item = eventBody
        )
        return responseMakerWithMessage(200, "{} updated successfully.".format(eventBody['CustomerId']['S']))
    
    except Exception as exception:
        logger.error(str(exception))
        return responseMakerWithMessage(400, "Unable to process the update request")


# This function updates only Email of Customer Item
def updateCustomerEmail(eventBody):
    try:
        dynamoDBClient.update_item(
            TableName = dynamoDB_table_name,
            Key = { 'CustomerId' : eventBody['CustomerId']},
            ExpressionAttributeValues = { ':newEmail' : eventBody['Email'] },
            UpdateExpression = 'SET Email = :newEmail'
        )
        return responseMakerWithMessage(200, "{} updated successfully.".format(eventBody['CustomerId']['S']))

    except Exception as exception:
        logger.error(str(exception))
        return responseMakerWithMessage(400, "Unable to process the update request")
    

# This function cleans the given JSON by removing some escape characters
def jsonCleaner(data):
    return data.replace("\\r\\n","")


#This function creates a response 
def responseMakerWithMessage(statusCode, message):
    return {
            "statusCode" : statusCode,
            "headers" : {
                "Content-Type": "application/json"
            },
            "body" : message
        }