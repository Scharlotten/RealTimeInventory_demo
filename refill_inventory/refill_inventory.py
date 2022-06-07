import pandas as pd
from sqlalchemy import create_engine
import os
from random import randint
from time import sleep
import ccloud_lib
from confluent_kafka import Producer, KafkaError
import json


def connect_to_postgres():
    """
    :return:engine this function returns an engine object that is needed for the pandas dataframe to be sent to postgres
    """
    password = os.getenv("POSTGRES_PASSWORD", "postgres")
    username = os.getenv("POSTGRES_USER", "postgres")
    database = os.getenv("POSTGRES_DB", "dummy")
    host = os.getenv("POSTGRES_HOST", "postgres_host")
    engine = create_engine(f'postgresql://{username}:{password}@{host}:5432/{database}')
    print("Connection created")
    return engine


def refill_inventory():
    products = pd.read_sql("select * from products", engine)
    products["refill"] = 1000
    prod_dict = products.to_dict(orient="records")
    for product in prod_dict:
        if product:
            output = product
            print(output)
            yield output, output.get("id")

def acked(err, msg):
    global delivered_records
    """Delivery report handler called on
    successful or failed delivery of message
    """
    if err is not None:
        print("Failed to deliver message: {}".format(err))
    else:
        delivered_records += 1
        print("Produced record to topic {} partition [{}] @ offset {}"
              .format(msg.topic(), msg.partition(), msg.offset()))


if __name__ == "__main__":
    engine = connect_to_postgres()

    args = ccloud_lib.parse_args()
    config_file = args.config_file
    topic = args.topic
    conf = ccloud_lib.read_ccloud_config(config_file)

    # Create Producer instance
    producer_conf = ccloud_lib.pop_schema_registry_params_from_config(conf)
    producer = Producer(producer_conf)

    # Create topic if needed
    ccloud_lib.create_topic(conf, topic)


    sleep(20)
    while True:
        for msgvalue, msg_key in refill_inventory():
            record_key = msg_key
            record_value = msgvalue

            print("Producing record: {}\t{}".format(record_key, record_value))
            producer.produce(topic, key=str(record_key), value=json.dumps(record_value), on_delivery=acked)
            sleep(1.5)