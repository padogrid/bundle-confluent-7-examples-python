#!/usr/bin/env python

#=============================================================================
#
# Produce Customer messages
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
import customer
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

    file = open('etc/avro/customer.avsc', 'r')
    customer_schema = file.read()
    print(customer_schema)
    file.close()
    
    key_serializer = AvroSerializer(schema_registry_client = schema_registry_client,
                                          schema_str = ccloud_lib.name_schema,
                                          to_dict = ccloud_lib.Name.name_to_dict)
    value_serializer = AvroSerializer(schema_registry_client = schema_registry_client,
                                     schema_str =  customer_schema,
                                     to_dict = customer.Customer.customer_to_dict)

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
        customer_object = customer.Customer()
        customer_object.createdOnMillis = round(time.time()*1000)
        customer_object.updatedOnMillis = round(time.time()*1000)
        customer_object.customerId = name_object.name
        customer_object.companyName = "Effertz, Jaskolski and Bartell"
        customer_object.contactName = "Gutmann"
        customer_object.contactTitle = "Central Manufacturing Strategist"
        customer_object.address = "30739 Wendolyn Mews, Jeromyfurt, NY 57521"
        customer_object.city = "North Archie"
        customer_object.region="KS"
        customer_object.postalCode = "67871"
        customer_object.country = "Trinidad and Tobago"
        customer_object.phone = "80-318-1768 x768"
        customer_object.fax = "1-135-010-7160"
        
        print(customer_object)
        
        print("Producing Avro record: {}\t{}".format(name_object.name, customer_object.customerId))
        
        print(customer_object.to_dict())
        
        producer.produce(topic=topic, key=name_object, value=customer_object, on_delivery=acked)
        producer.poll(0)

    producer.flush()

    print("{} messages were produced to topic {}!".format(delivered_records, topic))
