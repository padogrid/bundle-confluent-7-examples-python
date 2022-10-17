#!/usr/bin/env python

#=============================================================================
#
# Consume messages
# Using Confluent Python Client for Apache Kafka
# Reads Avro data, integration with Confluent Cloud Schema Registry
#
#=============================================================================

from confluent_kafka import DeserializingConsumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import StringDeserializer

import json
import ccloud_lib

if __name__ == '__main__':

    # Read arguments and configurations and initialize
    args = ccloud_lib.parse_args()
    config_file = args.config_file
    topic = args.topic
    conf = ccloud_lib.read_ccloud_config(config_file)

    schema_registry_conf = {
        'url': conf['schema.registry.url']}
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    key_deserializer = StringDeserializer()
    value_deserializer = AvroDeserializer(schema_registry_client = schema_registry_client)
    
    # for full list of configurations, see:
    #   https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html#pythonclient-consumer
    consumer_conf = ccloud_lib.pop_schema_registry_params_from_config(conf)
    consumer_conf['key.deserializer'] = key_deserializer
    consumer_conf['value.deserializer'] = value_deserializer
    consumer_conf['group.id'] = 'perf_test_python'
    consumer_conf['auto.offset.reset'] = 'latest'
    consumer = DeserializingConsumer(consumer_conf)

    # Subscribe to topic
    consumer.subscribe(['nw.customers', 'nw.orders'])

    # Process messages
    total_count = 0
    while True:
        try:
            msg = consumer.poll(1.0)
            if msg is None:
                # No message available within timeout.
                # Initial message consumption may take up to
                # `session.timeout.ms` for the consumer group to
                # rebalance and start consuming
                # print("Waiting for message or event/error in poll()")
                continue
            elif msg.error():
                print('error: {}'.format(msg.error()))
            else:
                key = msg.key()
                value = msg.value()
                print(key + ": " + json.dumps(value, indent=4, sort_keys=True))
        except KeyboardInterrupt:
            break
        except SerializerError as e:
            # Report malformed record, discard results, continue polling
            print("Message deserialization failed {}".format(e))
            pass

    # Leave group and commit final offsets
    consumer.close()