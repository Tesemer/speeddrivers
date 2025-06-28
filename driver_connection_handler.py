import configparser
import asyncio
import time
import uuid

from crud import Crud
from GenerateWorkload import generate_create, generate_workload
from abstract_driver import AbstractDriver
from drivers.asyncpg_driver import AsyncpgDriver
from drivers.psycopg2_driver import Psycopg2Driver
from drivers.pg8000_driver import Pg8000
from drivers.sqlalchemy_driver import SqlalchemyDriver

async def main():
    config = configparser.ConfigParser()
    config.read('config.cfg')
    amount = int(config.get('workload', 'AMOUNT'))
    insert_per_column_size = int(config.get('workload', 'INSERT_PER_COLUMN_SIZE'))
    benchmark_id = uuid.uuid4()
    for operation_type in Crud:
        workload = generate_workload(benchmark_id, operation_type, amount, insert_per_column_size)
        await perform_driver_benchmark(config, workload)

async def perform_driver_benchmark(config, workload):
    for driver_class in AbstractDriver.__subclasses__():
        driver = driver_class(config)
        start_time = time.perf_counter()
        await driver.connect()
        print(f"Connected to {driver_class.__name__} in {time.perf_counter() - start_time:.4f} seconds")
        await driver.handle_workload()
        await driver.close_connection()

asyncio.run(main())

def filter_workload(operation_type):
    return None

