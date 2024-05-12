import pika
from pysnmp.hlapi import *
from influxdb import InfluxDBClient
import random

# Connect to RabbitMQ
def connect_to_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    return channel

# Connect to InfluxDB
def connect_to_influxdb():
    client = InfluxDBClient(host='127.0.0.1', port=8086, database='DataBase_NP')
    return client

# Function to process messages from RabbitMQ
def process_messages(channel, influxdb_client):
    def callback(ch, method, properties, body):
        print(f"Received message: {body.decode()}")
        switch_id = extract_switch_id(body)
        temperature = retrieve_temperature_from_switch(switch_id)
        if temperature is not None:
            write_to_influxdb(influxdb_client, switch_id, temperature)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_queue', on_message_callback=callback)
    print("Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()

# Function to extract switch ID from the message
def extract_switch_id(message):
    # Assuming the message format is "Collect data for switch [switch_name] ([switch_id])"
    parts = message.decode().split("(")
    return parts[-1].split(")")[0]

# Generates a random temperature between 22.1°C and 59.9°C
def generate_random_temperature():
    return round(random.uniform(22.1, 59.9), 2)
    
# Function to retrieve temperature from the switch using SNMP (dummy implementation)
def retrieve_temperature_from_switch(switch_id):
    # Dummy implementation: Replace with actual SNMP query to retrieve temperature
    random_temperature = generate_random_temperature()
    return random_temperature

# Function to write data to InfluxDB
def write_to_influxdb(client, switch_id, temperature):
    data = [
        {
            "measurement": "temperature",
            "tags": {
                "switch_id": switch_id
            },
            "fields": {
                "value": temperature
            }
        }
    ]
    client.write_points(data)

# Main function
def main():
    try:
        # Connect to RabbitMQ
        rabbitmq_channel = connect_to_rabbitmq()

        # Connect to InfluxDB
        influxdb_client = connect_to_influxdb()

        # Process messages from RabbitMQ
        process_messages(rabbitmq_channel, influxdb_client)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

