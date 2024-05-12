from influxdb import InfluxDBClient

# Connect to InfluxDB
client = InfluxDBClient(host='127.0.0.1', port=8086, username='NP_User', password='1234', database='DataBase_NP')

# Define your delete query
delete_query = "DELETE FROM temperature WHERE time <= now()"

# Execute the delete query
client.query(delete_query)

