import json
from asyncio.events import get_event_loop
from asyncio.futures import Future
from functools import partial
import asyncio
import simplejson
import threading
import websockets
import ccloud_lib

from confluent_kafka import DeserializingConsumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.schema_registry.json_schema import JSONDeserializer



def run_consumer(shutdown_flag, clients, lock, topic):
    print("Starting Kafka Consumer.")
    args = ccloud_lib.parse_args()
    config_file = args.config_file
    conf = ccloud_lib.read_ccloud_config(config_file)

    schema_registry_client = SchemaRegistryClient(
        {"url": conf.get("schema.registry.url"),
         "basic.auth.user.info": conf.get("basic.auth.user.info")})

    #deserializer = JSONDeserializer()

    # conf["value.deserializer"] = deserializer
    conf = ccloud_lib.pop_schema_registry_params_from_config(conf)
    consumer = DeserializingConsumer(conf)
    consumer.subscribe([topic])

    while not shutdown_flag.done():
        msg = consumer.poll(0.2)

        if msg is None:
            print("Waiting...")
        elif msg.error():
            print(f"ERROR: {msg.error()}")
        else:
            value = msg.value()
            formatted = simplejson.dumps(value)
            print(type(formatted))
            print(f"Sending {formatted} to {clients}")

            with lock:
                websockets.broadcast(clients, formatted)

    print("Closing Kafka Consumer")
    consumer.close()

async def handle_connection(clients, lock, connection, path):
    with lock:
        clients.add(connection)

    await connection.wait_closed()

    with lock:
        clients.remove(connection)


async def main():
    shutdown_flag = Future()
    clients = set()
    lock = threading.Lock()
    args = ccloud_lib.parse_args()
    topic = args.topic

    get_event_loop().run_in_executor(None, run_consumer, shutdown_flag,
                                     clients, lock, topic)

    print("Starting WebSocket Server.")
    try:
        async with websockets.serve(partial(handle_connection, clients, lock),
                                    "0.0.0.0", 8080):
            await Future()
    finally:
        shutdown_flag.set_result(True)


asyncio.run(main())