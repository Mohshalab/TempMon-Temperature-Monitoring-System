import mysql.connector
import pika

# Connect to MariaDB database
def connect_to_database():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="NP_User",
        password="1234",
        database="NP_Data"
    )
    return conn

# Retrieve list of switches from the database
def retrieve_switches(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Switch")
    switches = cursor.fetchall()
    cursor.close()
    return switches

# Connect to RabbitMQ
def connect_to_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    return channel

# Write collection tasks to RabbitMQ for each switch
def write_tasks_to_queue(channel, switches):
    for switch in switches:
        switch_id, switch_name = switch[0], switch[1]
        task = f"Collect data for switch {switch_name} ({switch_id})"
        channel.basic_publish(
            exchange='',
            routing_key='task_queue',
            body=task,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            )
        )
        print(f"Task '{task}' sent to the queue")

# Main function
def main():
    try:
        # Connect to MariaDB
        db_conn = connect_to_database()

        # Retrieve list of switches
        switches = retrieve_switches(db_conn)

        # Connect to RabbitMQ
        rabbitmq_channel = connect_to_rabbitmq()

        # Write collection tasks to RabbitMQ for each switch
        write_tasks_to_queue(rabbitmq_channel, switches)

        # Close database connection
        db_conn.close()

        # Close RabbitMQ connection
        rabbitmq_channel.close()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

