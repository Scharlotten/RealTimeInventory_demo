-- 1. Make sure your Debezium CDC connector is running and producing messages into Confluent Cloud the topic name should be: dummy.public.customers
-- Create table for customers - this table unfortunately won't be queryable so on top of this a new one needs to be created
CREATE TABLE customer_tbl(
  my_key STRUCT< id bigint> primary key,
  before STRUCT<id bigint>,
  after STRUCT<id bigint,
  						  first_name VARCHAR,
  						  last_name VARCHAR,

             	                  country varchar,
  								  address varchar>
  			,
            op varchar)

 WITH (KAFKA_TOPIC='dummy.public.customers',
       VALUE_FORMAT='JSON',
       KEY_FORMAT='JSON');
--------------------------------------------------------------------------
--2. This table will be queryable - this table will keep all the customers by key as the latest element in the materialized view, therefore
-- This can gurantee that we can source the latest address every time we query ksqldb

CREATE TABLE CUSTOMERS WITH (KAFKA_TOPIC='CUSTOMERS', PARTITIONS=6, REPLICAS=3) AS SELECT *
FROM CUSTOMER_TBL CUSTOMER_TBL
EMIT CHANGES;

--3. Create a stream on top of the inventory refills - this will be used in the next steps
	   CREATE STREAM refills_base(
  id int,
  product varchar,
  refill bigint)

 WITH (KAFKA_TOPIC='inventory_refills',
       VALUE_FORMAT='JSON',
       KEY_FORMAT='KAFKA');
-- 4. Create the table that will sum up the refills by product:
CREATE TABLE LATEST_INVENTORY WITH (KAFKA_TOPIC='LATEST_INVENTORY', PARTITIONS=6, REPLICAS=3) AS SELECT
  REFILLS_BASE.PRODUCT PRODUCT,
  SUM(REFILLS_BASE.REFILL) TOTAL_REFILLS
FROM REFILLS_BASE REFILLS_BASE
GROUP BY REFILLS_BASE.PRODUCT
EMIT CHANGES;
-- 5.
select ti.product, TI.TOTAL_REFILLS - TOK.TOTAL as moving_inventory from TEST_INVENTORY2 ti join TOTAL_ORDERS tok  on ti.product = tok.product_name emit changes;

