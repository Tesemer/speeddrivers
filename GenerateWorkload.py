import random

random.seed()

def generate_create(workload_name, table_prefix, amount):

    textfile = open(workload_name, 'w')

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

generate_create("W1", "tab", 100)