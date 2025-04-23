import base64
import os
import google.generativeai as genai
import pyodbc

def connect_to_mssql():
    # Connection parameters
    server = ''  # Replace with your server name or IP
    database = ''  # Replace with your database name
    username = ''  # Replace with your username
    password = ''  # Replace with your password

    # ODBC connection string
    connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"

    try:
        # Establish the connection
        connection = pyodbc.connect(connection_string)
        print("Successfully connected to MSSQL database!")
        return connection
    except Exception as e:
        print(f"Error: {e}")
        return None

def read_sql_file(file_path):
    """Reads the content of an SQL file."""
    with open(file_path, 'r') as file:
        sql_script = file.read()
    return sql_script

def main():
    sql_file = "AdventureWorksSchema.sql"  # Replace with your SQL file path
    sql_script = read_sql_file(sql_file)

    #client = genai.client(api_key="{api_key}")
    # response = client.models.generate_content(
    #    model="gemini-2.0-flash",
    #    contents="Explain how AI works in a few words"
    # )
    #
    genai.configure(api_key="{api_key}")
    prompt = ('you are an expert in constructing sql queries from a plain english text. For the schema '+ sql_script +
              ' user with id 29485 asked list of products that he has ordered. give only the query that can be executed in db to fetch the result. '
              'make sure query has only select statement but no delete or  update or insert. '
              'your response should contain only query no other explanation.' )
    model = genai.GenerativeModel(model_name='gemini-1.5-flash')
    response = model.generate_content(prompt)
    text = response.text.replace('```sql', '').replace('```', '')
    print('Script: ' + text)
    try:
        conn = connect_to_mssql()
        cursor = conn.cursor()
        cursor.execute(text)
        result = cursor.fetchall()
        for row in result:
            print(row)

        # Handle errors
    except Exception as e:
        print(f"An error occurred while fetching data: {e}")

    # Close DB Connection irrespective of success
    # or failure
    if conn:
       conn.close()
       print('SQLite Connection closed')

if __name__ == "__main__":
    main()
