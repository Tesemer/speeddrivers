import datetime
import random
import string
from enum import Enum
from crud import Crud
from schema import Datatable

def generate_workloads(benchmark_id, seed, amount, insert_per_column_size) -> list[list[str]]:
    random.seed(seed)
    workload_prefix = f'WL-{benchmark_id}-{seed}'
    return [generate_insert(f'{workload_prefix}{Crud.CREATE.value}', amount, insert_per_column_size),
            generate_read(f'{workload_prefix}{Crud.READ.value}'),
            generate_update(f'{workload_prefix}{Crud.UPDATE.value}', amount, insert_per_column_size),
            generate_delete(f'{workload_prefix}{Crud.DELETE.value}', amount)]

# Generates new random values amount-times with insert-per-column-size
def generate_insert(workload_name, amount, insert_per_column_size):
    textfile = open('benchmark_data/' + workload_name, 'x')
    insert_count = amount

    all_queries = []
    while insert_count > 0:
        id = amount - insert_count
        insert_query = insert_entry(id, insert_per_column_size)
        all_queries.append(insert_query)
        insert_count -= 1

    for query in all_queries:
        textfile.write(query + "\n")
    textfile.close()
    return all_queries

# creates one random insert entry to add one row
def insert_entry(id, insert_per_column_size):
    insert_values = []
    for i in range(10):
        insert_random_value = ''.join(random.choices(string.ascii_letters + string.digits, k=insert_per_column_size))
        insert_values.append(f"'{insert_random_value}'")

    insert_query = f'INSERT INTO datatable VALUES ({id}, {', '.join(insert_values)})'
    return insert_query

# For now READ-WL is: "select everything from table"
def generate_read(workload_name):
    query_values = []
    textfile = open('benchmark_data/' + workload_name, 'x')
    query = 'SELECT * FROM datatable'
    query_values.append(query)
    query_values.append(query)
    query = query + "\n" + query + "\n"
    textfile.write(query)
    textfile.close()
    return query_values

# updates every column with new random values with the same size, and "amount" of times
def generate_update(workload_name, amount, insert_per_column_size):
    textfile = open('benchmark_data/' + workload_name, 'x')
    update_count = amount

    all_queries = []
    while update_count > 0:
        update_query = update_entry(amount - update_count, insert_per_column_size)
        all_queries.append(update_query)
        update_count -= 1

    for query in all_queries:
        textfile.write(query + "\n")
    textfile.close()
    return all_queries

# creates one random update entry to update one row
def update_entry(id, insert_per_column_size):
    update_values = []
    for i in range(10):
        update_random_value = ''.join(random.choices(string.ascii_letters + string.digits, k=insert_per_column_size))
        update_values.append(f'field{i} = \'{update_random_value}\'')

    update_query = f'UPDATE datatable SET {', '.join(update_values)} WHERE id={id}'
    return update_query

# deletes every row, row by row
def generate_delete(workload_name, amount):
    textfile = open('benchmark_data/' + workload_name, 'x')
    delete_count = amount

    all_queries = []
    while delete_count > 0:
        delete_query = delete_entry(amount - delete_count)
        all_queries.append(delete_query)
        delete_count -= 1

    for query in all_queries:
        textfile.write(query + "\n")
    textfile.close()
    return all_queries

# deletes one row
def delete_entry(id):
    return f'DELETE FROM datatable WHERE id={id}'

def generate_create(workload_name, table_prefix, amount):

    textfile = open('benchmark_data/' + workload_name, 'w')

    create_count = amount
    drop_count = amount

    all_entries = []

    while create_count + drop_count > 0:

        if drop_count == 0:
            # Creating a creation entry
            create_sql = create_entry(table_prefix, amount - create_count)
            all_entries.append(create_sql)
            create_count -= 1
            continue
        elif create_count == 0:
            # Creating a drop entry
            drop_sql = drop_entry(table_prefix, amount - drop_count)
            all_entries.append(drop_sql)
            drop_count -= 1
            continue

        if drop_count > create_count and drop_count > 0 and random.randint(0, 1):

            # Creating a drop entry
            drop_sql = drop_entry(table_prefix, amount - drop_count)
            all_entries.append(drop_sql)
            drop_count -= 1

        elif create_count > 0:

            # Creating a creation entry
            create_sql = create_entry(table_prefix, amount - create_count)
            all_entries.append(create_sql)
            create_count -= 1

    # Putting the output in the file
    for entry in all_entries:
        textfile.write(entry + "\n")
    textfile.close()

def drop_entry(table_prefix, num):
    # Creating a drop entry
    table_name = table_prefix + str(num)
    drop_sql = "DROP TABLE IF EXISTS " + table_name + ";"
    return drop_sql


def create_entry(table_prefix, num):
    # Creating a creation entry
    table_name = table_prefix + str(num)
    create_sql = "CREATE TABLE " + table_name + (" (id INT SERIAL,"
                                                 "field0 VARCHAR(100),"
                                                 " field1 VARCHAR(100),"
                                                 " field2 VARCHAR(100),"
                                                 " field3 VARCHAR(100),"
                                                 " field4 VARCHAR(100),"
                                                 " field5 VARCHAR(100),"
                                                 " field6 VARCHAR(100),"
                                                 " field7 VARCHAR(100),"
                                                 " field8 VARCHAR(100),"
                                                 " field9 VARCHAR(100));")
    return create_sql

#generate_create("W1", "tab", 100)