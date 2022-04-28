from random import randint
from time import sleep
import psycopg2 as psycopg2
import os
from faker import Faker
import pandas as pd
from sqlalchemy import create_engine

def connect(port:int=5432):
    """
    :param port: The port postgres is advertised on
    :return: cursor - connection to the postgres DB - used for throttled inserts
    """
    password = os.getenv("POSTGRES_PASSWORD", "postgres")
    user = os.getenv("POSTGRES_USER", "postgres")
    database = os.getenv("POSTGRES_DB", "dummy")
    host = os.getenv("POSTGRES_HOST", "postgres_host")
    sleep(2)
    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        port=port
    )
    conn.autocommit = True
    cursor = conn.cursor()
    return cursor

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


def create_random_customers(number=10):
    fake = Faker()
    df = pd.DataFrame()
    for i in range(number):
        customer={"first_name": fake.first_name(),
                   "last_name": fake.last_name(),
                   "zipcode": fake.postcode(),
                   "country": fake.country(),
                   "address": fake.address()
        }
        df = df.append(customer, ignore_index=True)
    return df


def insert_random_customers(df, engine, tbl_name="customers"):
    df.to_sql(tbl_name, engine, method='multi', if_exists='append', index=False)
    print("successfully inserted")


def update_customers(cursor, engine, number=5):
    faker = Faker()
    customers = pd.read_sql("select * from customers", engine)
    customer_ids=list(customers.id.unique().astype(int))
    rands = [customer_ids[randint(1, len(customer_ids)-1)] for a in range(0, number)]
    for random_customer_index in rands:
        address = faker.address()
        cursor.execute(
            f"""UPDATE customers set address = %(address)s 
                    where id=%(random_customer_index)s;""",
            {'random_customer_index': int(random_customer_index),
             'address': address,
             }
            )
        print(f"successfully updated customer: {random_customer_index}")

def delete_customers(cursor, engine, number=3):
    customers = pd.read_sql("select * from customers", engine)
    customer_ids=list(customers.id.unique().astype(int))
    rands = [customer_ids[randint(1, len(customer_ids)-1)] for a in range(0, number)]
    for random_customer_index in rands:
        cursor.execute(
            f"""DELETE FROM customers  
                    where id=%(random_customer_index)s;""",
            {'random_customer_index': int(random_customer_index)
             }
            )
        print(f"successfully DELETED customer: {random_customer_index}")

if __name__ == "__main__":
    cursor = connect()
    engine = connect_to_postgres()
    df = create_random_customers(10)
    while True:
        insert_random_customers(df, engine, "customers")
        try:
            update_customers(cursor, engine, 2)
        except Exception as e:
            print(e)
        sleep(4)
        try:
            delete_customers(cursor, engine, 1)
        except Exception as e:
            print(e)
        sleep(4)
