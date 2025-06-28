import configparser
import asyncio
import time
import uuid

from crud import Crud
from GenerateWorkload import generate_create, generate_workloads
from abstract_driver import AbstractDriver
from drivers.asyncpg_driver import AsyncpgDriver
from drivers.psycopg2_driver import Psycopg2Driver
from drivers.pg8000_driver import Pg8000
from drivers.sqlalchemy_driver import SqlalchemyDriver

async def main():
    config = configparser.ConfigParser()
    config.read('config.cfg')
    seed = int(config.get('workload', 'SEED'))
    amount = int(config.get('workload', 'AMOUNT'))
    insert_per_column_size = int(config.get('workload', 'INSERT_PER_COLUMN_SIZE'))
    benchmark_id = uuid.uuid4()
    insert_wl, read_wl, update_wl, delete_wl = generate_workloads(benchmark_id, seed, amount, insert_per_column_size)
    await perform_driver_benchmark(config, [insert_wl, read_wl, update_wl, delete_wl])

async def perform_driver_benchmark(config, operation_workloads):
    for driver_class in AbstractDriver.__subclasses__():
        for operation_workload in operation_workloads:
            driver = driver_class(config, operation_workload)
            await driver.connect()

            start_time = time.perf_counter()
            await driver.handle_workload()
            end_time = time.perf_counter() - start_time
            print(f"handled operation in {driver_class.__name__} in {end_time:.4f} seconds")

            await driver.close_connection()

asyncio.run(main())

