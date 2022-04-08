import boto3
import json
import logging
import numpy as np

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodbTableName = 'DNA-database'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodbTableName)

getMethod = 'GET'
postMethod = 'POST'
mutantPath = '/mutant'
statsPath = '/stats'

def lambda_handler(event, context):
    logger.info(event)
    httpMethod = event['httpMethod']
    path = event['path']
    if httpMethod == getMethod and path == statsPath:
        response = getStats()
        #response = getStats(event['queryStringParameters']['DNA_ID'])
    elif httpMethod == postMethod and path == mutantPath:
        response = saveADN(json.loads(event['body']))
    else:
        response = buildResponse(404, 'Not Found')

    return response

def getStats():
    try:
        response = table.scan()
        result = response['Items']

        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStarKey=response['LastEvaluatedKey'])
            result.extend(response['Items'])

        dna_count = len(result)
        body = {
            'dna_count': dna_count,
            'DNAs': result
        }
        return buildResponse(200, body)
    except:
        logger.exception('Do your custom error handling')

"""def getStats(DNA_ID):
    try:
        response = table.get_item(
            Key={
                'DNA_ID': DNA_ID
            }
        )
        if 'Item' in response:
            return buildResponse(200, response['Item'])
        else:
            return buildResponse(404, {'Message': 'DNA_ID: %s not found' % DNA_ID})
    except:
        logger.exception('Do your custom error handling')"""

def saveADN(requestBody):
    requestBody['DNA_ID'] = "1"
    requestBody['isMutant'] = isMutant(requestBody['DNA'])
    try:
        table.put_item(Item=requestBody)
        body = {
            'Operation': 'SAVE',
            'Message': 'SUCCESS',
            'Item': requestBody
        }
        if requestBody['isMutant'] == True:
            return buildResponse(200, body)
        else:
            return buildResponse(403, body)
    except:
        logger.exception('Do your custom error handling')

def buildResponse(statusCode, body=None):
    response = {
        'statusCode': statusCode,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    if body is not None:
        response['body'] = json.dumps(body)
    return response

def isMutant (dna) :
    count = 0
    n = len(dna)

    dna_matrix =[]
    for row in dna :
        row = list(row)
        dna_matrix.append(row)

    dna_mirror =[]
    for row in dna_matrix :
        row = row[::-1]
        dna_mirror.append(row)

    dna_trans = []
    for i in range(n) :
        l = []
        for j in range(n) :
            l.append(dna[j][i])
        dna_trans.append(l)

    for row in dna :
        for i in range(n - 3) :
            s = set(row[i:i + 4])
            if len(s) == 1 :
                count += 1
                if count == 2 : 
                    return True

    for row in dna_trans :
        for i in range(n - 3) :
            s = set(row[i:i + 4])
            if len(s) == 1 :
                count += 1
                if count == 2 : 
                    return True

    for i in range(1-n,n,1) :
        diag = list(np.diag(dna_matrix, i))
        if len(diag) >= 4 :
            for j in range(len(diag) - 3) :
                s = set(diag[j:j + 4])
                if len(s) == 1 :
                    count += 1
                    if count == 2 : 
                        return True

    for i in range(1-n,n,1) :
        diag = list(np.diag(dna_mirror, i))
        if len(diag) >= 4 :
            for j in range(len(diag) - 3) :
                s = set(diag[j:j + 4])
                if len(s) == 1 :
                    count += 1
                    if count == 2 : 
                        return True

    return False
