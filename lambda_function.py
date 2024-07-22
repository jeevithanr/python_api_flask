import json
import boto3

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')  

# Lambda handler function
def lambda_handler(event, context):
    try:
        # Extract HTTP method and path from the event
        http_method = event.get('httpMethod')
        path = event.get('path')

        if not http_method:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'HTTP method not provided in event'})
            }

        # Routing based on HTTP method and path
        if http_method == 'GET' and path == '/student':
            return get_students(event)
        elif http_method == 'GET' and path.startswith('/student/'):
            student_id = path.split('/')[-1]
            return get_student(student_id)
        elif http_method == 'POST' and path == '/student':
            return create_student(event)
        elif http_method == 'PUT' and path == '/student':
            return update_student(event)
        elif http_method == 'DELETE' and path == '/student':
            return delete_student(event)
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Endpoint not found'})
            }
    except KeyError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

# Helper functions for handling API requests

def get_students(event):
    try:
        # Example: Fetch all items from DynamoDB table
        response = table.scan()
        return {
            'statusCode': 200,
            'body': json.dumps(response['Items'])
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def get_student(student_id):
    try:
        # Example: Fetch item from DynamoDB by student_id
        response = table.get_item(Key={'studentid': student_id})
        if 'Item' in response:
            return {
                'statusCode': 200,
                'body': json.dumps(response['Item'])
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Student not found'})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def create_student(event):
    try:
        data = json.loads(event['body'])
        required_fields = ['studentid', 'fname', 'lname', 'contact', 'email']

        for field in required_fields:
            if field not in data:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': f'Missing required field: {field}'})
                }

        # Example: Insert item into DynamoDB table
        table.put_item(Item=data)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Student field created successfully', 'student': data})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def update_student(event):
    try:
        student_id = event['queryStringParameters']['studentid']
        data = json.loads(event['body'])
        required_fields = ['fname', 'lname', 'contact', 'email']

        for field in required_fields:
            if field not in data:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': f'Missing required field: {field}'})
                }

        # Example: Update item in DynamoDB table
        table.update_item(
            Key={'studentid': student_id},
            UpdateExpression='SET fname = :f, lname = :l, contact = :c, email = :e',
            ExpressionAttributeValues={
                ':f': data['fname'],
                ':l': data['lname'],
                ':c': data['contact'],
                ':e': data['email']
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Student updated successfully', 'studentid': student_id, 'updated_fields': data})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def delete_student(event):
    try:
        student_id = event['queryStringParameters']['studentid']
        # Example: Delete item from DynamoDB table
        table.delete_item(Key={'studentid': student_id})

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Student deleted successfully', 'studentid': student_id})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
