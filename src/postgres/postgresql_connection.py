from sqlalchemy import create_engine, text
from flask import Flask, jsonify
from sqlalchemy.orm import sessionmaker
import psycopg2
import pandas as pd

filePath = "D:\\SampleData\\uk_cities.csv"
myTableName = "UKCityMaster"
username = "consultants"
password = "WelcomeItc%402022" #WelcomeItc@2022
host = "18.132.73.146"
databaseName = "testdb"
port = 5432

app = Flask(__name__)

def connect_to_postgres():
    try:
        # Create an engine to connect to PostgreSQL
        # engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{databaseName}')
        engine = create_engine('postgresql://{username}:{password}@{host}:{port}/{databaseName}'.format(
            username=username,
            password=password,
            host=host,
            port=port,
            databaseName=databaseName
        ))
        print("Connection to PostgreSQL established successfully.")
        return engine
    except Exception as error:
        print("Error while connecting to PostgreSQL: {error}".format(error=error))
        return None

def read_csv_file(file_path):
    try:
        df = pd.read_csv(file_path)
        print("CSV file read successfully from {file_path}".format(filePath = file_path))
        return df
    except Exception as error:
        print("Error while reading CSV file: {error}")
        return None

def write_to_postgres(engine, df, table_name, if_exists='replace'):
    try:
        # Write the DataFrame to the PostgreSQL table
        df.to_sql(table_name, engine, if_exists=if_exists, index=False)
        print("Data written to {table_name} successfully.")
    except Exception as error:
        print("Error while writing data to PostgreSQL: {error}")

def close_connection(engine):
    if engine:
        engine.dispose()
        print("PostgreSQL connection is closed.")

# Route to fetch data from PostgreSQL database
@app.route('/get_data', methods=['GET'])
def get_data():
    # Connect to the database
    engine = connect_to_postgres()
    if engine is None:
        return jsonify({"error": "Failed to connect to the database"}), 500

    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Example: Querying a table (replace 'your_table' with your actual table name)
        result = session.execute(text('SELECT * FROM "UKCityMaster" LIMIT 10;'))
        data = result.fetchall()

        # Convert the query result into a list of dictionaries
        print(f"Print {data.head()}")
        result_list = [dict(zip(result.keys(), row)) for row in data]

        # Return the result as JSON
        return jsonify(result_list)

    except Exception as error:
        return jsonify({"error": "Error querying the database: error"}), 500
    finally:
        session.close()

def main():
    engine = connect_to_postgres()
    # if engine is not None:
    #     df = read_csv_file(filePath)
    #     if df is not None:
    #         table_name = myTableName
    #         write_to_postgres(engine, df, table_name)
    #     close_connection(engine)

if __name__ == "__main__":
    main()
    #this is comment
    app.run(host="0.0.0.0",debug=True, port=5001)
