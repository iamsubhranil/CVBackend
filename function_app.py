import azure.functions as func
from azure.data.tables import TableServiceClient, UpdateMode
import os
import logging

app = func.FunctionApp()
CONN_STR = os.environ["CounterDBConnStr"]

# Learn more at aka.ms/pythonprogrammingmodel

# Get started by running the following code to create a function using a HTTP trigger.


@app.function_name("hit")
@app.route(route="api", auth_level=func.AuthLevel.ANONYMOUS)
def hit(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    table_service_client = TableServiceClient.from_connection_string(
        conn_str=CONN_STR)
    table_name = "Counter"
    table_client = table_service_client.get_table_client(table_name=table_name)
    curr_count = table_client.get_entity(partition_key="1", row_key="1")
    logging.info(curr_count)
    # timestamp = curr_count["Timestamp"]
    curr_count = curr_count["Count"]
    curr_count += 1
    table_client.update_entity(mode=UpdateMode.REPLACE, entity={
                               "PartitionKey": "1", "RowKey": "1", "Count": curr_count})
    return func.HttpResponse(
        str(curr_count),  # + ";" + str(timestamp),
        status_code=200
    )
