#Welcome to this demo
# Introduction
The project is meant to simulate a retailer's web-shop. Some customers come, register, they order something then a  shipping service picks their order up. The whole project is using Kafka, and Confluent Cloud for communication purposes. 
# Services
There are a number of services in this repo:
* **Postgres DB** - under postgres_start - this service starts a postgres_DB with configurations that are essential 
for a Debezium connector to connect. The postgresDB comes with a database named "dummy". There are two tables that get automatically created.Customers and Products.

| id      | first_name | last_name      | zipcode | country | address |
| ----------- | ----------- |------------ | ----------- | ------| -------|
| 1      | Michele       | York           | 6523        | France |  6523 Thompson Orchard Suite 073 Lake Dwaynehaven, NY 98293 |


| id      | product |
| ----------- | ----------- |
| 1      | toy       |
| 2   | phone      |
| 3 | table|
| 4 | chair |
***
* **Updater** - is responsible for generating a number of dummy customers and inserting them into the customer database table. To test the functionality of the connector every 4 seconds 10 customers are added 5 change their addresses, and 1 is deleted from the system.

* **Order Service** - This one keeps making calls to the postgresDB, it queries the customers, then the products  and generates dummy orders on behalf of them, the address of the customers is intentionally not included in the messages. As you can see in the `docker-compose.yml ` file it produces all these order into a topic called "customer_orders" 
* **Connect** - A base image for connect, the jars file folder contains the debezium jar, that is required for   the connector to start, under debezium_source_conn there are a number of parameters that are set up for the connector to work. Since the customers table is created in the dummy database, it produces the data into the `dummy.public.customers` topic. 
* **Websocket** - Creates a websocket and opens a port where it broadcast Kafka messages coming in from a topic 
* **Shipping service** - this service subsribes to what the order service publishes, and makes sure to "deliver"  to customers, therefore goes to ksqldb and asks the materialized table what is the latest address of the customer instead of going back to PostGres, thus representing Kafka's pluggable nature. 
* **Refill inventory** - this service is publishing into a topic which is called inventory_refills its sole purpose  is to order new quantitites for all the products that are in the products table, and refill the inventory

# Usage
Make sure you configure all the .config files correctly, with authentication info to confluent cloud.
`docker-compose up -d` should do the rest of the job. 