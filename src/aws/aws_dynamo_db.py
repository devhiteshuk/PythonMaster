import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

#This method used to connect dynamodb
def connect_to_dynamodb():
    """Establish a connection to DynamoDB."""
    try:
        dynamodb = boto3.resource('dynamodb')
        return dynamodb
    except (NoCredentialsError, PartialCredentialsError):
        print("AWS credentials not found. Please configure your AWS credentials.")
        return None

#This method create table
#@param dynamobd: Dynamobd
#@param table_name: Name of the table
def create_table(dynamodb, table_name):
    """Create a DynamoDB table."""
    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {'AttributeName': 'ID', 'KeyType': 'HASH'}  # Partition key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'ID', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print(f"Table {table_name} is being created...")
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
        print(f"Table {table_name} is ready.")
    except Exception as e:
        print(f"Error creating table: {e}")

def insert_record(dynamodb, table_name, item):
    """Insert a record into the DynamoDB table."""
    try:
        table = dynamodb.Table(table_name)
        table.put_item(Item=item)
        print(f"Record inserted: {item}")
    except Exception as e:
        print(f"Error inserting record: {e}")

def read_records(dynamodb, table_name):
    """Read all records from the DynamoDB table."""
    try:
        table = dynamodb.Table(table_name)
        response = table.scan()
        items = response.get('Items', [])
        print("Records in the table:")
        for item in items:
            print(item)
    except Exception as e:
        print(f"Error reading records: {e}")

def get_item(dynamodb, table_name, key):
    """Retrieve a specific item from the DynamoDB table."""
    try:
        table = dynamodb.Table(table_name)
        response = table.get_item(Key=key)
        item = response.get('Item', None)
        if item:
            print(f"Item retrieved: {item}")
        else:
            print("Item not found.")
    except Exception as e:
        print(f"Error retrieving item: {e}")

# Main function to demonstrate usage
def main():
    dynamodb = connect_to_dynamodb()
    if dynamodb is None:
        return

    table_name = "Employee_Demo"

    # Create table
    create_table(dynamodb, table_name)

    # Insert records
    insert_record(dynamodb, table_name, {'ID': '1', 'Name': 'Abcd', 'Age': 35,'Department':'BigData','Salary':4000, 'DOJ':'26 Nov 2024'})
    insert_record(dynamodb, table_name, {'ID': '2', 'Name': 'Efghi', 'Age': 34,'Department':'BigData','Salary':4000, 'DOJ':'26 Nov 2024'})
    insert_record(dynamodb, table_name, {'ID': '3', 'Name': 'Jklmno', 'Age': 31,'Department':'BigData','Salary':4000, 'DOJ':'26 Nov 2024'})
    insert_record(dynamodb, table_name, {'ID': '4', 'Name': 'Pqstvew', 'Age': 32,'Department':'BigData','Salary':4000, 'DOJ':'26 Nov 2024'})
    insert_record(dynamodb, table_name, {'ID': '5', 'Name': 'Ustvsv', 'Age': 33,'Department':'BigData','Salary':4000, 'DOJ':'26 Nov 2024'})

    # Read all records
    read_records(dynamodb, table_name)

    # Get a specific item
    get_item(dynamodb, table_name, {'ID': '1'})
    # Get records by name
    get_item(dynamodb, table_name, {'Name': 'Abcd'})

if __name__ == "__main__":
    main()
