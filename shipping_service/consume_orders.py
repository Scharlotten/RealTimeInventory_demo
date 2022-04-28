from confluent_kafka import Consumer
import ccloud_lib
from get_address import get_address
import json


if __name__ == '__main__':
    # Read arguments and configurations and initialize
    args = ccloud_lib.parse_args()
    config_file = args.config_file
    topic = args.topic
    conf = ccloud_lib.read_ccloud_config(config_file)
    print("I am setting up config")
    # Create Consumer instance
    # 'auto.offset.reset=earliest' to start reading from the beginning of the
    #   topic if no committed offsets exist
    consumer_conf = ccloud_lib.pop_schema_registry_params_from_config(conf)
    producer_conf = ccloud_lib.pop_schema_registry_params_from_config(conf)
    consumer_conf['group.id'] = 'shipping_service'
    consumer_conf['auto.offset.reset'] = 'earliest'
    consumer = Consumer(consumer_conf)

     # Subscribe to topic
    consumer.subscribe([topic])
    print("I could do config")
    # Process messages
    total_count = 0
    firm_dict = {}
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                print("Waiting for message or event/error in poll()")
                continue
            elif msg.error():
                print('error: {}'.format(msg.error()))
            else:
                # Check for Kafka message
                record_key = msg.key().decode("utf-8")
                record_value = json.loads(msg.value().decode("utf-8"))
                try:
                    address = get_address(record_key)
                except Exception as e:
                    print(e)
                    address = "No address found"
                print(f"shipping to {address}, customer order: {record_value}")
                print(record_key)
    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()
