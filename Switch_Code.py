import mysql.connector

# Function to connect to the database
def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="NP_User",
            password="1234",
            database="NP_Data"
        )
        print("Connected to the database successfully!")
        return conn
    except mysql.connector.Error as e:
        print(f"An error occurred while connecting to the database: {e}")
        return None
# Function to add a switch to the database
def add_switch(conn, name, ip_address, port):
    cursor = conn.cursor()
    insert_query = "INSERT INTO Switch (name, ip_address, port) VALUES (%s, %s, %s)"
    switch_data = (name, ip_address, port)
    cursor.execute(insert_query, switch_data)
    conn.commit()
    cursor.close()

# Function to retrieve switches from the database
def get_switches(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Switch")
    switches = cursor.fetchall()
    cursor.close()
    return switches

# Main function
def main():
    # Connect to the database
    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        # Add switches to the database
        switches_to_add = [
            {"name": "Switch1", "ip_address": "192.168.1.1", "port": 8080},
            {"name": "Switch2", "ip_address": "192.168.1.2", "port": 8080},
            {"name": "Switch3", "ip_address": "192.168.1.3", "port": 8080},
            {"name": "Switch4", "ip_address": "192.168.1.4", "port": 8080},
            {"name": "Switch5", "ip_address": "192.168.1.5", "port": 8080},
            # Add more switches as needed
        ]
        for switch in switches_to_add:
            add_switch(conn, switch["name"], switch["ip_address"], switch["port"])

            # Retrieve switches from the database and print the information
            switches = get_switches(conn)
            print("Switches added to the database:")
        for switch in switches:
            print(f"Name: {switch[1]}, IP Address: {switch[2]}, Port: {switch[3]}")

    # Close the database connection
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
