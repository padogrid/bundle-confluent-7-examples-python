#!/usr/bin/env python

#=============================================================================
#
# Produce messages
# Using Confluent Python Client for Apache Kafka
# Writes Avro data, integration with Confluent Cloud Schema Registry
#
# =============================================================================
from confluent_kafka import SerializingProducer
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

import json
import ccloud_lib
import order
import time

if __name__ == '__main__':

    # Read arguments and configurations and initialize
    args = ccloud_lib.parse_args()
    config_file = args.config_file
    topic = args.topic
    conf = ccloud_lib.read_ccloud_config(config_file)

    # Create topic if needed
    ccloud_lib.create_topic(conf, topic)

    # for full list of configurations, see:
    #  https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html#pythonclient-producer
    schema_registry_conf = {
        'url': conf['schema.registry.url']}

    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    file = open('etc/avro/order.avsc', 'r')
    order_schema = file.read()
    print(order_schema)
    file.close()
    
    key_serializer = AvroSerializer(schema_registry_client = schema_registry_client,
                                          schema_str = ccloud_lib.name_schema,
                                          to_dict = ccloud_lib.Name.name_to_dict)
    value_serializer = AvroSerializer(schema_registry_client = schema_registry_client,
                                     schema_str =  order_schema,
                                     to_dict = order.Order.order_to_dict)

    # for full list of configurations, see:
    #  https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html#pythonclient-producer
    producer_conf = ccloud_lib.pop_schema_registry_params_from_config(conf)
    producer_conf['key.serializer'] = key_serializer
    producer_conf['value.serializer'] = value_serializer
    producer = SerializingProducer(producer_conf)

    delivered_records = 0

    # Optional per-message on_delivery handler (triggered by poll() or flush())
    # when a message has been successfully delivered or
    # permanently failed delivery (after retries).
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

    for n in range(10):
        name_object = ccloud_lib.Name()
        name_object.name = "k" + str(n)
        name_object.name = "k" + str(n)
        order_object = order.Order()
        order_object.createdOnMillis = round(time.time()*1000)
        order_object.updatedOnMillis = round(time.time()*1000)
        order_object.orderId = name_object.name
        order_object.customerId = "744165-5231"
        order_object.employeeId = "421037+7957"
        order_object.orderDateMillis = round(time.time()*1000)
        order_object.requiredDateMillis = round(time.time()*1000)
        order_object.shippedDateMillis = round(time.time()*1000)
        order_object.shipVia = "1"
        order_object.freight = 88.05
        order_object.shipName = "Reichel, Paucek and Crist"
        order_object.shipAddress = "Apt. 141 39353 Nan Prairie, East Manual, MI 28345-5295"
        order_object.shipCity = "Marilouburgh"
        order_object.shipRegion = "MN"
        order_object.shipPostalCode = "66935"
        order_object.shipCountry = "Zambia"

        print(order_object)
        
        print("Producing Avro record: {}\t{}\trequiredDateMillis={}".format(name_object.name, order_object.orderId, order_object.requiredDateMillis))
        
        print(order_object.to_dict())
        
        producer.produce(topic=topic, key=name_object, value=order_object, on_delivery=acked)
        producer.poll(0)

    producer.flush()

    print("{} messages were produced to topic {}!".format(delivered_records, topic))
