import mysql.connector

try:
    # Establish a connection to the database
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="NP_User",
        password="1234",
        database="NP_Data"
    )

    if conn.is_connected():
        print("Connected to the database")

        # Perform database operations here...

except mysql.connector.Error as e:
    print(f"Error connecting to the database: {e}")

finally:
    # Close the database connection
    if 'conn' in locals() and conn.is_connected():
        conn.close()
        print("Connection to the database closed")

